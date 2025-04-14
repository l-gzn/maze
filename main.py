import pygame
import random
from classes import Grid


pygame.init()

WIDTH = 600
HEIGHT = 600
ROWS, COLS = 5, 5

CELL_SIZE = WIDTH // COLS
WIN = pygame.display.set_mode((WIDTH + 2, HEIGHT + 2))
pygame.display.set_caption("Maze")
clock = pygame.time.Clock()
running = True


random_seed = random.randint(0, 1000)
grid = Grid(ROWS, COLS, CELL_SIZE, WIN, seed=random_seed)
Maze_done = False


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    while grid.current_cell:
        grid.maze_gen(loops=False, skip=False)
        # pygame.time.delay(90)

    if not Maze_done:
        grid.adjacency_list = grid.get_adjacency_list()
        path = grid.dfs()
        # path = grid.a_star(dijkstra=False)
        # path = grid.bfs()

        Maze_done = True
    

pygame.quit()