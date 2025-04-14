# For testing time taken to run the algorithm
import os
import random

import matplotlib.pyplot as plt
import numpy as np
import pygame

from classes import Grid

os.environ["SDL_VIDEODRIVER"] = "dummy"  # Set the SDL video driver to dummy
# from timeit import default_timer as timer

# pygame.init()


WIDTH = 600
HEIGHT = 600
ROWS, COLS = 4, 4


CELL_SIZE = WIDTH // COLS
WIN = pygame.display.set_mode((WIDTH + 2, HEIGHT + 2))
pygame.display.set_caption("Maze")
clock = pygame.time.Clock()
running = True

random_seed = random.randint(0, 1000)

nrows = 21
n = 20
dfs = np.zeros((nrows, n))

while ROWS < nrows:
    moyenne = 0
    for i in range(n):

        grid = Grid(ROWS, ROWS, CELL_SIZE, WIN, seed=i)
        Maze_done = False

        while grid.current_cell:
            grid.maze_gen(loops=True, skip=True)

        if not Maze_done:
            grid.adjacency_list = grid.get_adjacency_list()
            # start = timer()
            path, dfs[ROWS, i], visited = grid.dfs()
            # path, operations, visited = grid.a_star(dijkstra=False)
            # path, operations, visited = grid.a_star(dijkstra=True)
            # path, operations, visited = grid.bfs()
            # end = timer()
            # moyenne += operations
            Maze_done = True
    print(f"Taille:{ROWS}X{ROWS} , {moyenne/n} Mouvements, Chemin : {len(path)}")
    ROWS += 2

grid = Grid(ROWS, COLS, CELL_SIZE, WIN, seed=892)
Maze_done = False
draw_edges = False
draw_line = False

dfs2 = np.mean(dfs, axis=1)
dfs3 = np.std(dfs, axis=1)
x = np.arange(4, nrows + 4, 2)
plt.plot(x, dfs2[::2])
plt.plot(x, dfs2[::2] + dfs3[::2], "r--", label="std")
plt.plot(x, dfs2[::2] - dfs3[::2], "r--")
plt.show()


# while grid.current_cell:
#     grid.maze_gen(loops=True, skip=False)
#     # pygame.time.delay(90)

# if not Maze_done:
#     grid.adjacency_list = grid.get_adjacency_list()
#     start = timer()
#     # path, operations = grid.dfs()
#     path = grid.a_star(dijkstra=True)
#     end = timer()
#     # print(f"Time :{end - start} seconds")
#     # print(f"Number of moves: {operations}")
#     # moyenne += operations
#     Maze_done = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if not draw_edges:
    #     grid.draw_nodes()
    #     grid.draw_green_lines()
    #     draw_edges = True

    pygame.display.update()

pygame.quit()
