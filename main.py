import pygame

from classes import Grid

pygame.init()


WIDTH = 400
HEIGHT = 400
ROWS, COLS = 10,10


CELL_SIZE = WIDTH // COLS
WIN = pygame.display.set_mode((WIDTH + 2, HEIGHT + 2))
pygame.display.set_caption("Maze")
clock = pygame.time.Clock()
running = True


grid = Grid(ROWS, COLS, CELL_SIZE, WIN)

grid_printed = False
Maze_done = False
draw_edges = False
draw_line = False
draw_red_lines = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    while grid.current_cell:
        grid.draw()
        grid.maze_gen()
        pygame.time.delay(0)

    if not Maze_done:
        print(grid.get_cell_and_neighbors_list_in_num_coords())
        Maze_done = True

    if not draw_edges:
        grid.draw_nodes()
        grid.draw_green_lines()
        show_edges = True
    
    pygame.display.update()
    clock.tick(120)
    # if not grid_printed:
    #      print(grid.grid_with_walls)
    #      grid_printed = True

pygame.quit()
