import random
from collections import deque
import pygame

class Cell:
    def __init__(self, row, col, cell_size):
        self.row = row
        self.col = col
        self.cell_size = cell_size
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False


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

    def draw(self, win):
        """
        dessine les murs du labyrinthes et background
        """
        x = self.col * self.cell_size
        y = self.row * self.cell_size
        color_of_walls = 'white'
        color_of_background = 'purple'
        if self.visited:
            pygame.draw.rect(win, color_of_background, (x, y, self.cell_size, self.cell_size))

        if self.walls["top"]:
            pygame.draw.line(win, color_of_walls, (x, y), (x+self.cell_size, y), 2)
        if self.walls["right"]:
            pygame.draw.line(win, color_of_walls, (x+self.cell_size, y), (x+self.cell_size, y+self.cell_size), 2)
        if self.walls["bottom"]:
            pygame.draw.line(win, color_of_walls, (x+self.cell_size, y+self.cell_size), (x, y+self.cell_size), 2)
        if self.walls["left"]:
            pygame.draw.line(win, color_of_walls, (x, y+self.cell_size), (x, y), 2)

    def highlight(self, win):
        x = self.col * self.cell_size
        y = self.row * self.cell_size
        pygame.draw.rect(win, "red", (x, y , self.cell_size, self.cell_size))

class Grid:
    """
    forme une liste 2D d'objets cell
    """
    
    def __init__(self, rows, cols, cell_size, win):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.win = win
        self.grid = [[Cell(row, col, cell_size) for col in range(cols)] for row in range(rows)]
        
        # For maze gen
        self.stack = deque()
        self.current_cell = self.grid[random.randint(0, rows-1)][random.randint(0, cols-1)]
        self.current_cell.visited = True
        self.stack.append(self.current_cell)

        # For maze solve
        self.adjacency_list = None
        self.current = 1 # Starting cell
        self.end = self.rows*self.cols
        self.visited = set()
        self.visited.add(self.current)
        
        

        

    def get_cell(self, row, col):
        # access each cell in the grid
        if 0 <= row <= self.rows and 0 <= col <= self.cols:
            return self.grid[row][col]
        else:
            return None

    # returns dict of a cell's neighbors
    def get_neighbors(self, row, col):
        neighbors = {}
        if (top:= self.get_cell(row-1, col)):
            neighbors["top"] = top
        if col != self.cols-1:
            if (right:= self.get_cell(row, col+1)):
                neighbors["right"] = right
        if row != self.rows-1:
            if (bottom:= self.get_cell(row+1, col)):
                neighbors["bottom"] = bottom
        if (left:= self.get_cell(row, col-1)):
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
                


    # Draws grid and current cell to pygame window
    def draw(self, current_cell=None):
        self.win.fill("black")

        for row in self.grid:
            for cell in row:
                if cell.visited:
                    cell.draw(self.win)

        if self.current_cell and self.stack:
            self.current_cell.highlight(self.win)

        pygame.display.update()


    
    def maze_gen(self, loops=False):
        """Algo for maze gen"""
        if self.stack:
            self.current_cell = self.stack.pop()
            self.current_cell.visited = True
            neighbors = self.get_neighbors(self.current_cell.row, self.current_cell.col)
            unvisited_cells = [cell for cell in neighbors.values() if not cell.visited]

            # Small chance to remove additional walls, creating more loops
            if loops and random.random() < 0.25:
                loops  = [cell for cell in neighbors.values() if cell.visited]
                if loops:
                    chosen_cell = random.choice(loops)
                    self.remove_wall_between(self.current_cell, chosen_cell)

            if unvisited_cells:
                self.stack.append(self.current_cell)
                chosen_cell = random.choice(unvisited_cells)
                self.remove_wall_between(self.current_cell, chosen_cell)
                self.stack.append(chosen_cell)

        else:
            self.current_cell = None

    def ij_to_num(self, row, col):
        """(i,j) to num"""
        return row * self.cols + col + 1
        

    
    def num_to_ij(self, num):
        """num to (i,j)"""
        row = (num-1) // self.cols
        col = (num-1) - (row * self.cols)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
        return row, col
    
    def get_accessible_neighbors(self, row, col):
        """
        
        """
        free_neighbors = {}
        neighbors = self.get_neighbors(row, col)
        cell = self.get_cell(row, col)

        for direction in cell.walls:
            if not cell.walls[direction]:
                free_neighbors[direction] = neighbors[direction]
                
        return free_neighbors

    def get_adjacency_list(self, weights=True):
        """
        Returns an adjacency list of the maze with each cell in numeric coordinates.

        Format: {start_cell: [(neighbor_cell, weight), ...]}
        """
        adjacency_list = {}

        for row in self.grid:
            for cell in row:
                start_cell = self.ij_to_num(cell.row, cell.col)
                free_neighbors = self.get_accessible_neighbors(cell.row, cell.col)

                if start_cell not in adjacency_list:
                    adjacency_list[start_cell] = []

                for neighbor in free_neighbors.values():
                    neighbor_cell = self.ij_to_num(neighbor.row, neighbor.col)
                    
                    # Add the connection (undirected graph)
                    if weights:
                        adjacency_list[start_cell].append((neighbor_cell, 1))
                    else:
                        adjacency_list[start_cell].append(neighbor_cell)

        self.adjacency_list = adjacency_list
        return adjacency_list

    def draw_nodes(self):
        """
        Draws nodes at each cell position in the maze
        """
        adjacency_list = self.get_adjacency_list()
        width = self.cell_size / 10
        

        for node in adjacency_list.keys():  # Iterate through node keys (numeric cell coordinates)
            row, col = self.num_to_ij(node)  # Convert numeric ID back to (row, col)
            (x, y) = self.from_row_col_coords_to_pygame_coords(row, col)

            pygame.draw.circle(self.win, 'green', (x, y), width)
    
    def draw_green_lines(self):
        """
        Draws green lines between connected nodes using the adjacency list.
        Ensures each edge is drawn only once.
        """
        adjacency_list = self.get_adjacency_list()

        drawn_edges = set()  # To prevent drawing duplicate edges

        for start_cell, neighbors in adjacency_list.items():
            start_cell_py_coords = self.from_num_coords_to_pygame_coords(start_cell)

            for neighbor_cell, _ in neighbors:  # (neighbor, weight)
                if (neighbor_cell, start_cell) in drawn_edges:
                    continue  # Skip if already drawn (prevents duplicates)

                neighbor_cell_py_coords = self.from_num_coords_to_pygame_coords(neighbor_cell)
                pygame.draw.line(self.win, 'green', start_cell_py_coords, neighbor_cell_py_coords, 2)
                drawn_edges.add((start_cell, neighbor_cell))  # Mark as drawn

            pygame.display.update()  # Refresh the display


    def from_row_col_coords_to_pygame_coords(self, row, col):
        """
        
        """
        x = self.cell_size*col + self.cell_size/2
        y = self.cell_size*row + self.cell_size/2
        return (x, y)
    
    def from_num_coords_to_pygame_coords(self, num_coord):
        """
        
        """
        (row, col) = self.num_to_ij(num_coord)
        x = self.cell_size*col + self.cell_size/2
        y = self.cell_size*row + self.cell_size/2
        return (x, y)


    def is_node(self, n):
        """
        returns true if a cell is either start, end, dead end or crossroad
        """

        if n == 1 or n == self.rows*self.cols:
            return True

        row, col = self.num_to_ij(n)
        cell = self.get_cell(row, col)
        counter = 0

        for direction in cell.walls:
            if cell.walls[direction]:
                counter += 1

        if counter != 2:
            return True
        else:
            return False
            
    def get_list_of_nodes(self):
        """
        returns a list of the nodes
        """
        list = []
        for row in self.grid:
            for cell in row:
                if self.is_node(self.ij_to_num(cell.row, cell.col)):
                    list.append(self.ij_to_num(cell.row, cell.col))
        return list
    

    def get_path_2_nodes(self, start, end):
        """
        returns the shortest path between 2 nodes
        """
        

    def get_reduced_adjacency_list(self):
        ...
        

    def dfs(self):
        self.stack.append(self.current)

        if self.end not in self.visited:
            a = 0
            b = len(self.adjacency_list[self.current])
            
            while a < b:
                neighbor = self.adjacency_list[self.current][a][0]
                if neighbor not in self.visited: 
                    self.stack.append(neighbor)
                    self.visited.add(neighbor)
                    self.current = neighbor
                else:
                    a += 1
                
                    

            
            



            


    def dijkstra(self):
        ...

    def a_star(self):
        ...
