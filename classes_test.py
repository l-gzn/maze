import random
import pygame
from collections import deque


class Cell:
    def init(self, row, col, cell_size):
        self.row = row
        self.col = col
        self.cell_size = cell_size
        self.visited = False
    
    def draw(self, win):
        x = self.col * self.cell_size
        y = self.row * self.cell_size
        
        if self.visited:
            pygame.draw.rect(win, "purple", (x, y, self.cell_size, self.cell_size))

    def highlight(self, win):
        x = self.col * self.cell_size
        y = self.row * self.cell_size
        pygame.draw.rect(win, "red", (x, y , self.cell_size, self.cell_size))


class Grid:
    def __init__(self, rows, cols, cell_size, win):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.win = win
        self.grid = [[1 for col in range(2*cols-1)] for row in range(2*rows-1)]
        for i in range(2*rows-1):
            for j in range(2*cols-1):
                if i % 2 == 0 and j % 2 == 0:
                    self.grid[i][j] = 0
        
        

        # For maze gen
        self.stack = deque()
        self.current_cell = self.grid[random.randint(0, 2*rows-1)][random.randint(0, 2*cols-1)]



    def get_cell(self, row, col):
        if 0 <= row < self.rows*2-1 and 0 <= col < self.cols*2-1:
            return self.grid[row][col]
        


    def get_neighbors(self, row, col):
        neighbors = {}
        top = self.get_cell(row-1, col)
        right = self.get_cell(row, col+1)
        bottom = self.get_cell(row+1, col)
        left = self.get_cell(row, col-1)
    
        if top == 1:
            neighbors["top"] = top
        elif top == 0:
            neighbors["top"] = 0

        if col != self.cols-1:
            if right == 1:
                neighbors["right"] = right
            elif right == 0:
                neighbors["right"] = 0

        if row != self.rows-1:
            if bottom == 1:
                neighbors["bottom"] = bottom
            elif bottom == 0:
                neighbors["bottom"] = 0

        if left == 1:
            neighbors["left"] = left
        elif left == 0:
            neighbors["left"] = 0
        
        return neighbors

    def convert_wall(self, cell_1, cell_2):
        if cell_1.row == cell_2.row:
            if cell_1.col < cell_2.col:
                self.grid[2*cell_1.row][2*(cell_1.col+1)-1] = 0 # 0 == no wall 1 == wall
            else:
                self.grid[2*cell_2.row][2*(cell_2.col+1)-1] = 0

        elif cell_1.col == cell_2.col:
            if cell_1.row < cell_2.row:
                self.grid[2*(cell_1.row+1)-1][2*cell_1.col] = 0
            else:
                self.grid[2*(cell_2.row+1)-1][2*cell_2.col] = 0

    def draw(self, current_cell=None):
        self.win.fill("black")

        for row in self.grid:
            for cell in row:
                if cell.visited:
                    cell.draw(self.win)

        if self.current_cell and self.stack:
            self.current_cell.highlight(self.win)

        pygame.display.update()


grid = Grid(4, 4, 50, None)

print(grid.grid)
print(grid.current_cell)