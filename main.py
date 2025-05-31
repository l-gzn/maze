import os
import random

import pygame
from classes import Grid, Button
from utils import handle_quit, update_layout

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BUTTONS_DIR = os.path.join(BASE_DIR, "Buttons")


pygame.init()


HEIGHT = 600
WIDTH = HEIGHT + 200
ROWS, COLS = 200,200
H_MULT = 1
DELAY = 0


UI_WIDTH = 200 
BUTTON_X = WIDTH - UI_WIDTH + 5  # X position where buttons start
BASE_HEIGHT = 600 
SCALE_FACTOR = HEIGHT / BASE_HEIGHT  # for scaling buttons
UI_WIDTH_SCALED = 200

CELL_SIZE = HEIGHT // COLS
WIN = pygame.display.set_mode((WIDTH + 2, HEIGHT + 2), pygame.RESIZABLE)
pygame.display.set_caption("Maze")
clock = pygame.time.Clock()

grid = Grid(ROWS, COLS, CELL_SIZE, WIN)
Maze_done = False
Solved = False
deepest = None
obs = False


# Button images
perfect_img = pygame.image.load(os.path.join(BUTTONS_DIR, "Perfect.png")).convert_alpha()
non_perfect_img = pygame.image.load(os.path.join(BUTTONS_DIR, "Non_perfect.png")).convert_alpha()
deepest_img = pygame.image.load(os.path.join(BUTTONS_DIR, "Deepest.png")).convert_alpha()
bottom_right_img = pygame.image.load(os.path.join(BUTTONS_DIR, "Bottom_right.png")).convert_alpha()
obstacles_img = pygame.image.load(os.path.join(BUTTONS_DIR, "Obstacles.png")).convert_alpha()
no_obstacles_img = pygame.image.load(os.path.join(BUTTONS_DIR, "No_obstacles.png")).convert_alpha()
dfs_img = pygame.image.load(os.path.join(BUTTONS_DIR, "DFS.png")).convert_alpha()
bfs_img = pygame.image.load(os.path.join(BUTTONS_DIR, "BFS.png")).convert_alpha()
astar_img = pygame.image.load(os.path.join(BUTTONS_DIR, "Astar.png")).convert_alpha()
dijkstra_img = pygame.image.load(os.path.join(BUTTONS_DIR, "Dijkstra.png")).convert_alpha()


# Create button instances
perfect_button = Button(BUTTON_X, int(0 * SCALE_FACTOR), perfect_img, scale=0.95)
non_perfect_button = Button(BUTTON_X, int(50 * SCALE_FACTOR), non_perfect_img, scale=0.95)
deepest_button = Button(BUTTON_X, int(100 * SCALE_FACTOR), deepest_img, scale=0.95)
bottom_right_button = Button(BUTTON_X, int(150 * SCALE_FACTOR), bottom_right_img, scale=0.95)
obstacles_button = Button(BUTTON_X, int(200 * SCALE_FACTOR), obstacles_img, scale=0.95)
no_obstacles_button = Button(BUTTON_X, int(250 * SCALE_FACTOR), no_obstacles_img, scale=0.95)
dfs_button = Button(BUTTON_X, int(300 * SCALE_FACTOR), dfs_img, scale=0.95)
bfs_button = Button(BUTTON_X, int(350 * SCALE_FACTOR), bfs_img, scale=0.95)
astar_button = Button(BUTTON_X, int(400 * SCALE_FACTOR), astar_img, scale=0.95)
dijkstra_button = Button(BUTTON_X, int(450 * SCALE_FACTOR), dijkstra_img, scale=0.95)


def create_buttons(button_x, scale):
    return {
        "perfect": Button(button_x, int(0 * 50 * scale), perfect_img, scale=0.95 * scale),
        "non_perfect": Button(button_x, int(1 * 50 * scale), non_perfect_img, scale=0.95 * scale),
        "deepest": Button(button_x, int(2 * 50 * scale), deepest_img, scale=0.95 * scale),
        "bottom_right": Button( button_x, int(3 * 50 * scale), bottom_right_img, scale=0.95 * scale),
        "obstacles": Button(button_x, int(4 * 50 * scale), obstacles_img, scale=0.95 * scale),
        "no_obstacles": Button(button_x, int(5 * 50 * scale), no_obstacles_img, scale=0.95 * scale),
        "dfs": Button(button_x, int(6 * 50 * scale), dfs_img, scale=0.95 * scale),
        "bfs": Button(button_x, int(7 * 50 * scale), bfs_img, scale=0.95 * scale),
        "astar": Button(button_x, int(8 * 50 * scale), astar_img, scale=0.95 * scale),
        "dijkstra": Button(button_x, int(9 * 50 * scale), dijkstra_img, scale=0.95 * scale),
        }


buttons = create_buttons(BUTTON_X, SCALE_FACTOR)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            CELL_SIZE, BUTTON_X, SCALE_FACTOR = update_layout(HEIGHT, WIDTH, COLS)
            UI_WIDTH_SCALED = int(200 * SCALE_FACTOR)
            buttons = create_buttons(BUTTON_X, SCALE_FACTOR)

    if buttons["obstacles"].draw(WIN):
        obs = True

    if buttons["no_obstacles"].draw(WIN):
        obs = False

    if obs:
        WIN.fill(
            "black",
            rect=(
                (BUTTON_X, int(200 * SCALE_FACTOR)), 
                (UI_WIDTH_SCALED, int(50 * SCALE_FACTOR))
                )
        )

    if not obs:
        WIN.fill(
            "black",
            rect=(
                (BUTTON_X, int(250 * SCALE_FACTOR)), 
                (UI_WIDTH_SCALED, int(50 * SCALE_FACTOR))
                )
        )

    if buttons["perfect"].draw(WIN):
        Maze_done = False
        WIN.fill("black", ((0, 0), (WIDTH - UI_WIDTH_SCALED, HEIGHT)))
        pygame.display.update()
        random_seed = random.randint(0, 1000)
        print(f"Seed:{random_seed}")
        grid = Grid(ROWS, COLS, CELL_SIZE, WIN, seed=random_seed)

        # maze generation
        while grid.current_cell:
            handle_quit()
            grid.maze_gen(loops=False, obstacles=obs)
            # pygame.time.delay(90)

        grid.adjacency_list = grid.get_adjacency_list()

        # find deepest cell
        deepest = grid.bfs(find_deepest=True)
        # color deepest cell
        deep_row, deep_col = grid.num_to_ij(deepest)
        grid.draw_square(deep_row, deep_col, background_col="green")

        Maze_done = True
        Solved = False

    if buttons["non_perfect"].draw(WIN):
        Maze_done = False
        WIN.fill("black", rect=((0, 0), (WIDTH - UI_WIDTH_SCALED, HEIGHT)))
        pygame.display.update()
        random_seed = random.randint(0, 1000)
        print(f"Seed:{random_seed}")
        grid = Grid(ROWS, COLS, CELL_SIZE, WIN, seed=random_seed)

        # maze Generation
        while grid.current_cell:
            handle_quit()
            grid.maze_gen(loops=True, obstacles=obs)
            # pygame.time.delay(90)

        # creates the adjacency list
        grid.get_adjacency_list()

        # using BFS to find the deepest cell in the maze
        deepest = grid.bfs(find_deepest=True)
        # colors the deepest cell
        deep_row, deep_col = grid.num_to_ij(deepest)
        grid.draw_square(deep_row, deep_col, background_col="green")

        Maze_done = True
        Solved = False

    if buttons["deepest"].draw(WIN):
        grid.end = deepest

    if buttons["bottom_right"].draw(WIN):
        grid.end = ROWS * COLS

    if grid.end == ROWS * COLS:
        WIN.fill(
            "black",
            rect=(
                (BUTTON_X, int(150 * SCALE_FACTOR)), 
                (UI_WIDTH_SCALED, int(50 * SCALE_FACTOR))
            )
        )

    if grid.end == deepest and grid.end != ROWS * COLS:
        WIN.fill(
            "black",
            rect=(
                (BUTTON_X, int(100 * SCALE_FACTOR)), 
                (UI_WIDTH_SCALED, int(50 * SCALE_FACTOR))
                )
        )

    if buttons["dfs"].draw(WIN):
        if Maze_done:
            if not Solved:
                path = grid.dfs(end_cell=grid.end, sleep=DELAY)
                print(f"Length: {len(path)}")
                if obs:
                    grid.redraw_obstacles(path)
                    grid.count_obstacles(path)
                Solved = True
            else:
                grid.new_solve(deepest, obs)
                path = grid.dfs(end_cell=grid.end, sleep=DELAY)
                print(f"Length: {len(path)}")
                if obs:
                    grid.redraw_obstacles(path)
                    grid.count_obstacles(path)

                Solved = True

    if buttons["bfs"].draw(WIN):
        if Maze_done:
            if not Solved:
                path = grid.bfs(end_cell=grid.end, sleep=DELAY)
                print(f"Length: {len(path)}")
                if obs:
                    grid.redraw_obstacles(path)
                    grid.count_obstacles(path)
                Solved = True
            else:
                grid.new_solve(deepest, obs)
                path = grid.bfs(end_cell=grid.end, sleep=DELAY)
                print(f"Length: {len(path)}")
                if obs:
                    grid.redraw_obstacles(path)
                    grid.count_obstacles(path)
                Solved = True

    if buttons["astar"].draw(WIN):
        if Maze_done:
            if not Solved:
                path = grid.a_star(end_cell=grid.end, h_mult=H_MULT, sleep=DELAY)
                print(f"Length: {len(path)}")
                if obs:
                    grid.redraw_obstacles(path)
                    grid.count_obstacles(path)
                Solved = True
            else:
                grid.new_solve(deepest, obs)
                path = grid.a_star(end_cell=grid.end, h_mult=H_MULT, sleep=DELAY)
                print(f"Length: {len(path)}")
                if obs:
                    grid.redraw_obstacles(path)
                    grid.count_obstacles(path)
                Solved = True

    if buttons["dijkstra"].draw(WIN):
        if Maze_done:
            if not Solved:
                path = grid.a_star(dijkstra=True, end_cell=grid.end, sleep=DELAY)
                print(f"Length: {len(path)}")
                if obs:
                    grid.redraw_obstacles(path)
                    grid.count_obstacles(path)
                Solved = True
            else:
                grid.new_solve(deepest, obs)
                path = grid.a_star(dijkstra=True, end_cell=grid.end, sleep=DELAY)
                print(f"Length: {len(path)}")
                if obs:
                    grid.redraw_obstacles(path)
                    grid.count_obstacles(path)
                Solved = True

    clock.tick(120)
    pygame.display.update()

pygame.quit()



