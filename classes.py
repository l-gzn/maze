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
        x = self.col * self.cell_size
        y = self.row * self.cell_size

        if self.visited:
            pygame.draw.rect(win, "purple", (x, y, self.cell_size, self.cell_size))

        if self.walls["top"]:
            pygame.draw.line(win, "white", (x, y), (x+self.cell_size, y), 2)
        if self.walls["right"]:
            pygame.draw.line(win, "white", (x+self.cell_size, y), (x+self.cell_size, y+self.cell_size), 2)
        if self.walls["bottom"]:
            pygame.draw.line(win, "white", (x+self.cell_size, y+self.cell_size), (x, y+self.cell_size), 2)
        if self.walls["left"]:
            pygame.draw.line(win, "white", (x, y+self.cell_size), (x, y), 2)

    def highlight(self, win):
        x = self.col * self.cell_size
        y = self.row * self.cell_size
        pygame.draw.rect(win, "red", (x, y , self.cell_size, self.cell_size))

class Grid:
    # forme une liste 2D d'objets cell
    def __init__(self, rows, cols, cell_size, win):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.win = win
        self.grid = [[Cell(row, col, cell_size) for col in range(cols)] for row in range(rows)]
        self.grid_with_walls = [[1 for col in range(2*cols-1)] for row in range(2*rows-1)] # 0 == no wall 1 == wall
        for i in range(2*rows-1):
            for j in range(2*cols-1):
                if i%2==0 and j%2==0:
                    self.grid_with_walls[i][j] = 0 

        # For maze gen
        self.stack = deque()
        self.current_cell = self.grid[random.randint(0, rows-1)][random.randint(0, cols-1)]
        self.current_cell.visited = True
        self.stack.append(self.current_cell)


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
                self.grid_with_walls[2*cell1.row][2*(cell1.col+1)-1] = 0 # 0 == no wall 1 == wall
            else:
                cell1.remove_wall(cell2, "left")
                self.grid_with_walls[2*cell2.row][2*(cell2.col+1)-1] = 0
        elif cell1.col == cell2.col:
            if cell1.row < cell2.row:
                cell1.remove_wall(cell2, "bottom")
                self.grid_with_walls[2*(cell1.row+1)-1][2*cell1.col] = 0
            else:
                cell1.remove_wall(cell2, "top")
                self.grid_with_walls[2*(cell2.row+1)-1][2*cell2.col] = 0


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


    # Algo for maze gen
    def maze_gen(self, loops=False):
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
        return row * self.cols + col + 1
    
    def num_to_ij(self, num):
        row = (num-1) // self.cols
        col = (num-1) % self.cols
        return row, col
    
    def get_accessible_neighbors(self, row, col):
        free_neighbors = {}
        neighbors = self.get_neighbors(row, col)
        cell = self.get_cell(row, col)

        for direction in cell.walls:
            if not cell.walls[direction]:
                free_neighbors[direction] = neighbors[direction]
                
        return free_neighbors


    def get_edge_list(self):
        list = []

        for row in self.grid:
            for cell in row:
                free_neighbors = self.get_accessible_neighbors(cell.row, cell.col)
                for neighbor in free_neighbors.values():
                    c = self.ij_to_num(cell.row, cell.col)
                    n = self.ij_to_num(neighbor.row, neighbor.col)
                    if [n, c, 1] not in list:
                        list.append([c, n, 1])
                    
        return list

    def draw_edges(self):
        ...
            
            
    def dfs(self):
        ...


    def dijkstra(self):
        ...

    def a_star(self):
        ...

