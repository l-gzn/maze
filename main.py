import pygame

from classes import Grid

pygame.init()


WIDTH = 300
HEIGHT = 300
ROWS, COLS = 4, 4


CELL_SIZE = WIDTH // COLS
WIN = pygame.display.set_mode((WIDTH + 2, HEIGHT + 2))
pygame.display.set_caption("Maze")
clock = pygame.time.Clock()
running = True


grid = Grid(ROWS, COLS, CELL_SIZE, WIN)


Maze_done = False
draw_edges = False
draw_line = False


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    while grid.current_cell:
        grid.draw()
        grid.maze_gen()
        pygame.time.delay(0)

    if not Maze_done:
        grid.adjacency_list = grid.get_adjacency_list()
        print(grid.adjacency_list)
        Maze_done = True

    if not draw_edges:
        grid.draw_nodes()
        grid.draw_green_lines()
        draw_edges = True
    
    pygame.display.update()
    clock.tick(120)

pygame.quit()
