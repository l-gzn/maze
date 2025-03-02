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

    def get_cell_and_neighbors_list_in_num_coords(self):
        """
        
        """
        list = []

        for row in self.grid:
            for cell in row:
                free_neighbors = self.get_accessible_neighbors(cell.row, cell.col)
                for neighbor in free_neighbors.values():
                    start_cell = None
                    neighbor_cell = None
                    
                    start_cell = self.ij_to_num(cell.row, cell.col)
                    neighbor_cell = self.ij_to_num(neighbor.row, neighbor.col)
                    
                    if [neighbor_cell, start_cell, 1] not in list:
                        list.append([start_cell, neighbor_cell, 1])
                    
        return list

    def draw_nodes(self):
        """
        
        """
        width = self.cell_size / 10
        for row in self.grid:
            for cell in row:
                (x, y) = self.from_row_col_coords_to_pygame_coords(cell.row, cell.col)

                pygame.draw.circle(self.win, 'green', (x, y), width)
    # def draw_green_lines(self):
    #     """
    #     largeur_de_la_ligne = self.cell_size / 20
    #     """
    #     list = []

    #     for row in self.grid:
    #         for cell in row:
    #             free_neighbors = self.get_accessible_neighbors(cell.row, cell.col)
    #             for neighbor in free_neighbors.values():
    #                 start_cell = self.from_row_col_coords_to_pygame_coords(cell.row, cell.col)
    #                 neighbor_cell = self.from_row_col_coords_to_pygame_coords(neighbor.row, neighbor.col)
    #                 if [start_cell, neighbor_cell, 1] not in list:
    #                     list.append([start_cell, neighbor_cell, 1])
    #                     pygame.draw.line(self.win, 'green',start_cell, neighbor_cell, 2)
    
    def draw_green_lines(self):
        cell_and_neighbors_list = self.get_cell_and_neighbors_list_in_num_coords()
        for i in cell_and_neighbors_list:
            #get coords in num
            start_cell = i[0]
            neighbor_cell = i[1]
            #convert from num to pygame cords
            start_cell_py_coords = self.from_num_coords_to_pygame_coords(start_cell)
            neighbor_cell_py_coords = self.from_num_coords_to_pygame_coords(neighbor_cell)
            pygame.draw.line(self.win, 'green',start_cell_py_coords, neighbor_cell_py_coords, 2)


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


    def draw_edges(self): 
        ...
            
            
    def dfs(self):
        ...


    def dijkstra(self):
        ...

    def a_star(self):
        ...
