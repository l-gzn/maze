import pygame
from classes import Grid

pygame.init()


WIDTH = 650
HEIGHT = 650
ROWS, COLS = 10,10

CELL_SIZE = WIDTH // COLS
WIN = pygame.display.set_mode((WIDTH + 2, HEIGHT + 2))
pygame.display.set_caption("Maze")
clock = pygame.time.Clock()
running = True


grid = Grid(ROWS, COLS, CELL_SIZE, WIN)

grid_printed = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    while grid.current_cell:
        grid.draw()
        grid.maze_gen()
    


    clock.tick(120)
    if not grid_printed:
        print(grid.grid_with_walls)
        grid_printed = True
pygame.quit()