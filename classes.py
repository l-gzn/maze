import random
import time
from collections import deque

import pygame
from heapdict import heapdict

from utils import handle_quit


class Cell:
    def __init__(self, row, col, cell_size):
        self.row = row
        self.col = col
        self.cell_size = cell_size
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False
        self.obstacle = False

    def remove_wall(self, other, direction):
        if direction == "top":
            self.walls["top"] = False
            other.walls["bottom"] = False
        elif direction == "right":
            self.walls["right"] = False
            other.walls["left"] = False
        elif direction == "bottom":
            self.walls["bottom"] = False
            other.walls["top"] = False
        elif direction == "left":
            self.walls["left"] = False
            other.walls["right"] = False

    def draw(self, win, wall_color="white", background_color="purple", line_width=1, force=False):
        x = self.col * self.cell_size
        y = self.row * self.cell_size

        if self.visited or force:
            pygame.draw.rect(win, background_color, (x, y, self.cell_size, self.cell_size))
        if self.walls["top"]:
            pygame.draw.line(win, wall_color, (x, y), (x + self.cell_size, y), line_width)
        if self.walls["right"]:
            pygame.draw.line(win, wall_color, (x + self.cell_size, y), (x + self.cell_size, y + self.cell_size), line_width)
        if self.walls["bottom"]:
            pygame.draw.line(win, wall_color, (x + self.cell_size, y + self.cell_size), (x, y + self.cell_size), line_width)
        if self.walls["left"]:
            pygame.draw.line(win, wall_color, (x, y + self.cell_size), (x, y), line_width)


class Grid:
    def __init__(self, rows, cols, cell_size, win, seed=None):
        if seed is not None:
            random.seed(seed) 

        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.win = win
        self.grid = [
            [Cell(row, col, cell_size) for col in range(cols)] for row in range(rows)
        ]

        # for maze generation
        self.stack = deque()
        # starting cell
        self.current_cell = self.grid[random.randint(0, rows - 1)][
            random.randint(0, cols - 1)
        ]
        self.current_cell.visited = True
        self.stack.append(self.current_cell)

        # For maze solve
        self.adjacency_list = None
        self.current = 1 
        self.end = self.rows * self.cols
        self.visited = set()
        self.visited.add(self.current)

    # access each cell in the grid
    def get_cell(self, row, col):
        if 0 <= row <= self.rows and 0 <= col <= self.cols:
            return self.grid[row][col]
        else:
            return None

    # returns dict of a cell's neighbors
    def get_neighbors(self, row, col):
        neighbors = {}
        if top := self.get_cell(row - 1, col):
            neighbors["top"] = top
        if col != self.cols - 1:
            if right := self.get_cell(row, col + 1):
                neighbors["right"] = right
        if row != self.rows - 1:
            if bottom := self.get_cell(row + 1, col):
                neighbors["bottom"] = bottom
        if left := self.get_cell(row, col - 1):
            neighbors["left"] = left

        return neighbors

    # remove wall of 2 adjacent cells
    def remove_wall_between(self, cell1, cell2):
        if cell1.row == cell2.row:
            if cell1.col < cell2.col:
                cell1.remove_wall(cell2, "right")
            else:
                cell1.remove_wall(cell2, "left")

        elif cell1.col == cell2.col:
            if cell1.row < cell2.row:
                cell1.remove_wall(cell2, "bottom")
            else:
                cell1.remove_wall(cell2, "top")
                
    # shortcut for drawing
    def draw_square(self, row, col, wall_col="white", background_col="purple", surface=None):
        if surface is None:
            surface = self.win
        Cell.draw(self.grid[row][col], surface, wall_color=wall_col, background_color=background_col, force=True)
        x, y = (col - 1) * self.cell_size, (row - 1) * self.cell_size
        # update a small region on the surface instead of whole screen (optimization)
        pygame.display.update((x, y, self.cell_size * 3, self.cell_size * 3))

    def maze_gen(self, loops=False, obstacles=False):
        # must be placed inside a while loop in the main file to see the maze being generated
    
        if not self.current_cell.obstacle:
            self.draw_square(self.current_cell.row, self.current_cell.col, background_col="purple")
        else:
            self.draw_square(self.current_cell.row, self.current_cell.col, background_col="black")

        if self.stack:
            self.current_cell = self.stack.pop()
            self.current_cell.visited = True

            neighbors = self.get_neighbors(self.current_cell.row, self.current_cell.col)
            unvisited_cells = [cell for cell in neighbors.values() if not cell.visited]

            # small chance to remove additional walls, creating more loops
            if loops and random.random() < 0.25:
                loops = [cell for cell in neighbors.values() if cell.visited]
                if loops:
                    chosen_cell = random.choice(loops)
                    self.remove_wall_between(self.current_cell, chosen_cell)

            if unvisited_cells:
                self.stack.append(self.current_cell)
                chosen_cell = random.choice(unvisited_cells)

                if obstacles and random.random() < 0.15:
                    chosen_cell.obstacle = True

                self.remove_wall_between(self.current_cell, chosen_cell)
                self.stack.append(chosen_cell)

        else:
            self.current_cell = None

        
        if self.current_cell:
            self.draw_square(self.current_cell.row, self.current_cell.col, background_col="red")

    def ij_to_num(self, row, col):
        return row * self.cols + col + 1

    def num_to_ij(self, num):
        row = (num - 1) // self.cols
        col = (num - 1) - (row * self.cols)
        return row, col

    # used in get_adjacency_list
    def get_accessible_neighbors(self, row, col):
        
        free_neighbors = {}
        neighbors = self.get_neighbors(row, col)
        cell = self.get_cell(row, col)

        for direction in cell.walls:
            if not cell.walls[direction]:
                free_neighbors[direction] = neighbors[direction]

        return free_neighbors

    # graph representation for the algorithms to operate on
    def get_adjacency_list(self, weights=True):
        # format: {start_cell: [(neighbor_cell, weight), ...]}
        
        adjacency_list = {}

        for row in self.grid:
            for cell in row:
                start_cell = self.ij_to_num(cell.row, cell.col)
                free_neighbors = self.get_accessible_neighbors(cell.row, cell.col)

                if start_cell not in adjacency_list:
                    adjacency_list[start_cell] = []

                for neighbor in free_neighbors.values():
                    neighbor_cell = self.ij_to_num(neighbor.row, neighbor.col)

                    # add the connection
                    if weights:
                        weight = 1000 if cell.obstacle or neighbor.obstacle else 1

                        # add the connection only if it doesn't already exist
                        if (neighbor_cell, weight) not in adjacency_list[start_cell]:
                            adjacency_list[start_cell].append((neighbor_cell, weight))

                    else:
                        # add the connection only if it doesn't already exist
                        if neighbor_cell not in adjacency_list[start_cell]:
                            adjacency_list[start_cell].append(neighbor_cell)

                        # ensure the reverse connection also exists
                        if neighbor_cell not in adjacency_list:
                            adjacency_list[neighbor_cell] = []
                        if start_cell not in adjacency_list[neighbor_cell]:
                            adjacency_list[neighbor_cell].append(start_cell)

        self.adjacency_list = adjacency_list
        return adjacency_list


    def from_row_col_coords_to_pygame_coords(self, row, col):
        x = self.cell_size * col + self.cell_size / 2
        y = self.cell_size * row + self.cell_size / 2
        return (x, y)

    def from_num_coords_to_pygame_coords(self, num_coord, for_nodes=True):
        if for_nodes:
            (row, col) = self.num_to_ij(num_coord)
            x = self.cell_size * col + self.cell_size / 2
            y = self.cell_size * row + self.cell_size / 2
            return (int(x), int(y))
        else:
            (row, col) = self.num_to_ij(num_coord)
            x = self.cell_size * col
            y = self.cell_size * row
            return (int(x), int(y))


    def dfs(self, end_cell=None, sleep=0):
        if end_cell is None:
            end_cell = self.end 

        operations = 0
        self.visited = {self.current}
        stack = deque()
        stack.append(self.current)

        while end_cell not in self.visited:
            handle_quit()
            row, col = self.num_to_ij(self.current)
            self.draw_square(row, col, background_col="orange")
            operations += 1

            neighbors = self.adjacency_list[self.current]
            unvisited = [n[0] for n in neighbors if n[0] not in self.visited]

            if unvisited:
                chosen_neighbor = random.choice(unvisited)
                stack.append(chosen_neighbor)
                self.visited.add(chosen_neighbor)
                self.current = chosen_neighbor
            else:
                stack.pop()
                self.current = stack[-1]

        
        x, y = self.from_num_coords_to_pygame_coords(end_cell, for_nodes=False)
        pygame.draw.rect(self.win, "orange", (x, y, self.cell_size, self.cell_size))
        

        
        for cell in stack:
            row, col = self.num_to_ij(cell)
            self.draw_square(row, col, background_col="red")
            time.sleep(sleep)

        return list(stack), operations

    # heuristic
    def h(self, n, null=False):
        # set null = True for dijkstra
        
        if null:
            return 0
        
        # manhattan distance
        row, col = self.num_to_ij(n)
        end_row, end_col = self.num_to_ij(self.end)
        return abs(row - end_row) + abs(col - end_col)
    

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def a_star(self, dijkstra=False, end_cell=None, h_mult=1, sleep=0):
        # set to True to use Dijkstra

        if end_cell is None:
            end_cell = self.end    
        
        came_from = {}
        open_heap = heapdict()
        
        g_score = {
            spot: float("inf") 
            for row in self.grid 
            for spot in [self.ij_to_num(cell.row, cell.col) 
            for cell in row]
        }
        g_score[self.current] = 0
        f_score = {
            spot: float("inf")
            for row in self.grid
            for spot in [self.ij_to_num(cell.row, cell.col) for cell in row]
        }

        f_score[self.current] = self.h(self.current, null=dijkstra)
        open_heap[self.current] = f_score[self.current]


        row, col = self.num_to_ij(self.current)
        self.draw_square(row, col, background_col="orange")
        last_current = self.current  

        while open_heap:
            handle_quit()
            current, _ = open_heap.popitem()

           
            if last_current is not None and last_current != current:
                row, col = self.num_to_ij(last_current)
                self.draw_square(row, col, background_col="orange")
                time.sleep(sleep)


        
            if current == end_cell:
                row, col = self.num_to_ij(end_cell)
                self.draw_square(row, col, background_col="orange")

                
                path = self.reconstruct_path(came_from, current)
                for cell in path:
                    row, col = self.num_to_ij(cell)
                    self.draw_square(row, col, background_col="red")
                    time.sleep(sleep)
                return path

            # process neighbors
            for neighbor, weight in self.adjacency_list[current]:
                temp_g_score = g_score[current] + weight
                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + h_mult*self.h(neighbor, null=dijkstra)
                    
                    open_heap[neighbor] = f_score[neighbor] 
                    row, col = self.num_to_ij(neighbor)
                    self.draw_square(row, col, background_col="orange")
                    
                 
                    row, col = self.num_to_ij(neighbor)
                    self.draw_square(row, col, background_col="orange")
                        
            last_current = current

        return None

    def bfs(self, end_cell=None, find_deepest=False, sleep=0):
        if end_cell is None:
            end_cell = self.end  

        
        self.visited = {self.current}
        # queue stores (current_cell, path_so_far)
        queue = [ (self.current, [self.current]) ]  
        path = None

        while queue:
            handle_quit()
            current, path = queue.pop(0)

            if not find_deepest and current == end_cell:
                path = path  
                break

            elif find_deepest:
                path = path

            self.visited.add(current)

            
            if not find_deepest:
                row, col = self.num_to_ij(current)
                self.draw_square(row, col, background_col="orange")
                time.sleep(sleep)

            
            for neighbor_tuple in self.adjacency_list[current]:
                neighbor = (
                    neighbor_tuple[0]
                    if isinstance(neighbor_tuple, tuple)
                    else neighbor_tuple
                )
                if neighbor not in self.visited and neighbor not in [c for c, _ in queue]:
                    queue.append((neighbor, path + [neighbor]))

        
        if path and not find_deepest:
            for cell in path:
                row, col = self.num_to_ij(cell)
                self.draw_square(row, col, background_col="red")
            return path

        elif find_deepest:
            return path[-1]

    # redraw final path with obstacles in it
    def redraw_obstacles(self, path=None):
        if path:
            for row in self.grid:
                for cell in row:
                    if cell.visited and self.ij_to_num(cell.row, cell.col) not in path:
                        self.draw_square(cell.row, cell.col, background_col="purple", wall_col="white")
        
        for row in self.grid:
            for cell in row:
                if cell.obstacle:
                    self.draw_square(cell.row, cell.col, background_col="black", wall_col="white")
        if path:
            for cell in path:
                row, col = self.num_to_ij(cell)
                cell = self.get_cell(row, col)
                if cell.obstacle:
                    self.draw_square(cell.row, cell.col, background_col="green", wall_col="white")

    def count_obstacles(self, path):
        counter = 0
        for cell in path:
            row, col = self.num_to_ij(cell)
            cell = self.get_cell(row, col)
            if cell.obstacle:
                counter += 1
        print(f"Obstacles: {counter}")
    

    # clean  maze before solving again
    def new_solve(self, deepest=None, obs=False):
        for row in self.grid:
            for cell in row:
                self.draw_square(cell.row, cell.col)

        if obs:
            self.redraw_obstacles()

        
        if deepest:
            deep_row, deep_col = self.num_to_ij(deepest)
            self.draw_square(deep_row, deep_col, background_col="green")

        self.current = self.ij_to_num(0,0)
        self.visited = {self.current}


class Button():
    def __init__(self, x, y, image, scale=1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self, surface):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action