import pygame
from classes import Grid

pygame.init()


WIDTH = 650
HEIGHT = 650
ROWS, COLS = 4, 4


CELL_SIZE = WIDTH // COLS
WIN = pygame.display.set_mode((WIDTH + 2, HEIGHT + 2))
pygame.display.set_caption("Maze")
clock = pygame.time.Clock()
running = True


grid = Grid(ROWS, COLS, CELL_SIZE, WIN)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    while grid.current_cell:
        grid.draw()
        grid.maze_gen()
        pygame.time.delay(0)



    clock.tick(120)


print(grid.get_graph())
pygame.quit()