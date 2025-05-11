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

nrows = 40 # Taille du dernier labyrinthe
n = 1 # Nombre de labyrinthes par dimensions Rows x Rows
jump = 2 # Augmentation de la taille des labyrinthes

dfs = np.zeros((nrows, n))
a_star = np.zeros((nrows, n))
dijkstra = np.zeros((nrows, n))
bfs = np.zeros((nrows, n))
while ROWS < nrows + 1:
    for i in range(n):

        grid = Grid(ROWS, ROWS, CELL_SIZE, WIN, seed=i)
        Maze_done = False

        while grid.current_cell:
            grid.maze_gen(loops=False, skip=True)

        if not Maze_done:
            grid.adjacency_list = grid.get_adjacency_list()
            # path, bfs[ROWS, i] = grid.bfs()
            path, dfs[ROWS, i] = grid.dfs()
            # path, a_star[ROWS, i] = grid.a_star(dijkstra=False)
            # path, dijkstra[ROWS, i] = grid.a_star(dijkstra=True)
            Maze_done = True
    
    print(f"Taille:{ROWS}X{ROWS}")
    ROWS += jump




dfs_mean = np.mean(dfs, axis=1)
a_star_mean = np.mean(a_star, axis=1)
dijkstra_mean = np.mean(dijkstra, axis=1)
bfs_mean = np.mean(bfs, axis=1)


dfs3 = np.std(dfs, axis=1)
x = np.arange(0, nrows, jump)
plt.plot(x, dfs_mean[::jump])
# plt.plot(x, a_star_mean[::jump])
# plt.plot(x, dijkstra_mean[::jump])
# plt.plot(x, bfs_mean[::jump])


plt.plot(x, dfs[::jump] + dfs3[::jump], "r--", label="std")
plt.plot(x, dfs[::jump] - dfs3[::jump], "r--")
plt.show()

