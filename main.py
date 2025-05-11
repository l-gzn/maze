import random
import pygame
from classes import Grid, Button

pygame.init()

HEIGHT = 600
WIDTH = HEIGHT + 200
ROWS, COLS = 50, 50

CELL_SIZE = HEIGHT // COLS
WIN = pygame.display.set_mode((WIDTH + 2, HEIGHT + 2))
pygame.display.set_caption("Maze")
clock = pygame.time.Clock()

grid = Grid(ROWS, COLS, CELL_SIZE, WIN)
Maze_done = False
Solved = False
deepest = None
obs = False

# Button images
perfect_img = pygame.image.load("Buttons/Perfect.png").convert_alpha()
non_perfect_img = pygame.image.load("Buttons/Non_perfect.png").convert_alpha()
deepest_img = pygame.image.load("Buttons/Deepest.png").convert_alpha()
bottom_right_img = pygame.image.load("Buttons/Bottom_right.png").convert_alpha()
obstacles_img = pygame.image.load("Buttons/Obstacles.png").convert_alpha()
no_obstacles_img = pygame.image.load("Buttons/No_obstacles.png").convert_alpha()
dfs_img = pygame.image.load("Buttons/DFS.png").convert_alpha()
bfs_img = pygame.image.load("Buttons/BFS.png").convert_alpha()
astar_img = pygame.image.load("Buttons/Astar.png").convert_alpha()
dijkstra_img = pygame.image.load("Buttons/Dijkstra.png").convert_alpha()

# Create button instances
perfect_button = Button(605, 0, perfect_img, scale=0.95)
non_perfect_button = Button(605, 50, non_perfect_img, scale=0.95) 
deepest_button = Button(605, 100, deepest_img, scale=0.95)
bottom_right_button = Button(605, 150, bottom_right_img, scale=0.95)
obstacles_button = Button(605, 200, obstacles_img, scale=0.95)
no_obstacles_button = Button(605, 250, no_obstacles_img, scale=0.95)
dfs_button = Button(605, 300, dfs_img, scale=0.95)
bfs_button = Button(605, 350, bfs_img, scale=0.95)
astar_button = Button(605, 400, astar_img, scale=0.95)
dijkstra_button = Button(605, 450, dijkstra_img, scale=0.95)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    if obstacles_button.draw(WIN):
        obs = True
        
    if no_obstacles_button.draw(WIN):
        obs = False

    if obs:
        WIN.fill("black", rect=((605, 200), (200, 50)))

    if not obs:
        WIN.fill("black", rect=((605, 250), (200, 50)))
        

    if perfect_button.draw(WIN):
        Maze_done = False
        WIN.fill("black", ((0,0), (WIDTH - 200, HEIGHT)))
        pygame.display.update()
        random_seed = random.randint(0, 1000)
        print(f"Seed:{random_seed}")
        grid = Grid(ROWS, COLS, CELL_SIZE, WIN, seed=random_seed)

        # Maze Generation
        while grid.current_cell:
            grid.maze_gen(loops=False,skip=False, obstacles=obs)
            # pygame.time.delay(90)

        # Creates the adjacency list
        grid.adjacency_list = grid.get_adjacency_list()

        # Using BFS to find the deepest cell in the maze
        deepest = grid.bfs(find_deepest=True)
        # Colors the deepest cell
        deep_row, deep_col = grid.num_to_ij(deepest)
        grid.draw_square(deep_row, deep_col, background_col="cyan")

        Maze_done = True
        Solved = False


    if non_perfect_button.draw(WIN):
        Maze_done = False
        WIN.fill("black", rect=((0,0), (WIDTH - 200, HEIGHT)))
        pygame.display.update()
        random_seed = random.randint(0, 1000)
        print(f"Seed:{random_seed}")
        grid = Grid(ROWS, COLS, CELL_SIZE, WIN, seed=random_seed)

        # Maze Generation
        while grid.current_cell:
            grid.maze_gen(loops=True,skip=False, obstacles=obs)
            # pygame.time.delay(90)

        # Creates the adjacency list
        grid.adjacency_list = grid.get_adjacency_list()

        # Using BFS to find the deepest cell in the maze
        deepest = grid.bfs(find_deepest=True)
        # Colors the deepest cell
        deep_row, deep_col = grid.num_to_ij(deepest)
        grid.draw_square(deep_row, deep_col, background_col="cyan")

        Maze_done = True
        Solved = False

    if deepest_button.draw(WIN):
        grid.end = deepest
        
    
    if bottom_right_button.draw(WIN):
        grid.end = ROWS * COLS

    if grid.end == ROWS * COLS:
        WIN.fill("black", rect=((605, 150), (200, 50)))
    else:
        WIN.blit(bottom_right_button.image, bottom_right_button.rect)

    if grid.end == deepest:
        WIN.fill("black", rect=((605, 100), (200, 50)))
    else:
        WIN.blit(deepest_button.image, deepest_button.rect)


    if dfs_button.draw(WIN):
        if Maze_done:
            if not Solved:
                path, ops = grid.dfs(end_cell=grid.end, sleep=0)
                if obs:
                    grid.redraw_obstacles(path)
                Solved = True
            else:
                grid.new_solve(deepest, obs)
                path, ops = grid.dfs(end_cell=grid.end, sleep=0)
                if obs:
                    grid.redraw_obstacles(path)

                Solved = True

    if bfs_button.draw(WIN):
        if Maze_done:
            if not Solved:
                path, ops = grid.bfs(end_cell=grid.end, sleep=0)
                if obs:
                    grid.redraw_obstacles(path)
                Solved = True
            else:
                grid.new_solve(deepest, obs)
                path, ops = grid.bfs(end_cell=grid.end, sleep=0)
                if obs:
                    grid.redraw_obstacles(path)
                Solved = True


    if astar_button.draw(WIN):
        if Maze_done:
            if not Solved:
                path, ops = grid.a_star(end_cell=grid.end, sleep=0)
                if obs:
                    grid.redraw_obstacles(path)
                Solved = True
            else:
                grid.new_solve(deepest, obs)
                path, ops = grid.a_star(end_cell=grid.end, sleep=0)
                if obs:
                    grid.redraw_obstacles(path)
                Solved = True
    
    if dijkstra_button.draw(WIN):
        if Maze_done:
            if not Solved:
                path, ops = grid.a_star(dijkstra=True, end_cell=grid.end, sleep=0)
                if obs:
                    grid.redraw_obstacles(path)
                Solved = True
            else:
                grid.new_solve(deepest, obs)
                path, ops = grid.a_star(dijkstra=True, end_cell=grid.end, sleep=0)
                if obs:
                    grid.redraw_obstacles(path)
                Solved = True

        
    pygame.display.update()

pygame.quit()
