import random
import time
from collections import deque
from queue import PriorityQueue

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

    def draw(self, win, wall_color="white", background_color="purple", line_width=1):
        """
        dessine les murs du labyrinthes et background
        """
        x = self.col * self.cell_size
        y = self.row * self.cell_size
        if self.visited:
            pygame.draw.rect(
                win, background_color, (x, y, self.cell_size, self.cell_size)
            )

        if self.walls["top"]:
            pygame.draw.line(
                win, wall_color, (x, y), (x + self.cell_size, y), line_width
            )
        if self.walls["right"]:
            pygame.draw.line(
                win,
                wall_color,
                (x + self.cell_size, y),
                (x + self.cell_size, y + self.cell_size),
                line_width,
            )
        if self.walls["bottom"]:
            pygame.draw.line(
                win,
                wall_color,
                (x + self.cell_size, y + self.cell_size),
                (x, y + self.cell_size),
                line_width,
            )
        if self.walls["left"]:
            pygame.draw.line(
                win, wall_color, (x, y + self.cell_size), (x, y), line_width
            )

    def highlight(self, win):
        x = self.col * self.cell_size
        y = self.row * self.cell_size
        pygame.draw.rect(win, "red", (x, y, self.cell_size, self.cell_size))


class Grid:
    """
    forme une liste 2D d'objets cell
    """

    def __init__(self, rows, cols, cell_size, win, seed=42):
        import random

        random.seed(seed)  # Fixed seed for reproducibility

        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.win = win
        self.grid = [
            [Cell(row, col, cell_size) for col in range(cols)] for row in range(rows)
        ]

        # For maze generation
        self.stack = deque()
        # Pick a random starting cell using the fixed seed
        self.current_cell = self.grid[random.randint(0, rows - 1)][
            random.randint(0, cols - 1)
        ]
        self.current_cell.visited = True
        self.stack.append(self.current_cell)

        # For maze solve
        self.adjacency_list = None
        self.current = 1  # Starting cell
        self.end = self.rows * self.cols
        self.visited = set()
        self.visited.add(self.current)

    def get_cell(self, row, col):
        # access each cell in the grid
        if 0 <= row <= self.rows and 0 <= col <= self.cols:
            return self.grid[row][col]
        else:
            return None

    # returns dict of a cell's neighbors
    def get_neighbors(self, row, col):
        neighbors = {}
        if top := self.get_cell(row - 1, col):
            neighbors["top"] = top
        if col != self.cols - 1:
            if right := self.get_cell(row, col + 1):
                neighbors["right"] = right
        if row != self.rows - 1:
            if bottom := self.get_cell(row + 1, col):
                neighbors["bottom"] = bottom
        if left := self.get_cell(row, col - 1):
            neighbors["left"] = left

        return neighbors

    # remove wall of 2 adjacent cells
    def remove_wall_between(self, cell1, cell2):
        if cell1.row == cell2.row:
            if cell1.col < cell2.col:
                cell1.remove_wall(cell2, "right")
            else:
                cell1.remove_wall(cell2, "left")

        elif cell1.col == cell2.col:
            if cell1.row < cell2.row:
                cell1.remove_wall(cell2, "bottom")
            else:
                cell1.remove_wall(cell2, "top")

    def draw_square(
        self, row, col, wall_col="white", background_col="purple", surface=None
    ):
        if surface is None:
            surface = self.win
        Cell.draw(
            self.grid[row][col],
            surface,
            wall_color=wall_col,
            background_color=background_col,
        )
        x, y = (col - 1) * self.cell_size, (row - 1) * self.cell_size
        # Update a region on the surface if needed. You can omit display updates here.
        pygame.display.update((x, y, self.cell_size * 3, self.cell_size * 3))

    def maze_gen(self, loops=False, skip=False):
        """
        Algo for maze gen, each iteration removes walls between cells
        Must be used inside a while loop to see the maze being generated
        """

        # Colors cells
        if not skip:
            self.draw_square(
                self.current_cell.row, self.current_cell.col, background_col="purple"
            )

        if self.stack:
            self.current_cell = self.stack.pop()
            self.current_cell.visited = True

            neighbors = self.get_neighbors(self.current_cell.row, self.current_cell.col)
            unvisited_cells = [cell for cell in neighbors.values() if not cell.visited]

            # Small chance to remove additional walls, creating more loops
            if loops and random.random() < 0.25:
                loops = [cell for cell in neighbors.values() if cell.visited]
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

        # Highlight current cell
        if self.current_cell and not skip:
            self.draw_square(
                self.current_cell.row, self.current_cell.col, background_col="red"
            )

    def ij_to_num(self, row, col):
        """(i,j) to num"""
        return row * self.cols + col + 1

    def num_to_ij(self, num):
        """num to (i,j)"""
        row = (num - 1) // self.cols
        col = (num - 1) - (row * self.cols)
        return row, col

    def get_accessible_neighbors(self, row, col):
        """ """
        free_neighbors = {}
        neighbors = self.get_neighbors(row, col)
        cell = self.get_cell(row, col)

        for direction in cell.walls:
            if not cell.walls[direction]:
                free_neighbors[direction] = neighbors[direction]

        return free_neighbors

    def get_adjacency_list(self, weights=True):
        """
        Returns an adjacency list of the maze with each cell in numeric coordinates.

        Format: {start_cell: [(neighbor_cell, weight), ...]}
        """
        adjacency_list = {}

        for row in self.grid:
            for cell in row:
                start_cell = self.ij_to_num(cell.row, cell.col)
                free_neighbors = self.get_accessible_neighbors(cell.row, cell.col)

                if start_cell not in adjacency_list:
                    adjacency_list[start_cell] = []

                for neighbor in free_neighbors.values():
                    neighbor_cell = self.ij_to_num(neighbor.row, neighbor.col)

                    # Add the connection (undirected graph)
                    if weights:
                        adjacency_list[start_cell].append((neighbor_cell, 1))
                    else:
                        adjacency_list[start_cell].append(neighbor_cell)

        self.adjacency_list = adjacency_list
        return adjacency_list

    def draw_nodes(self):
        """
        Draws nodes at each cell position in the maze
        """
        adjacency_list = self.get_adjacency_list()
        width = self.cell_size / 10

        for (
            node
        ) in (
            adjacency_list.keys()
        ):  # Iterate through node keys (numeric cell coordinates)
            row, col = self.num_to_ij(node)  # Convert numeric ID back to (row, col)
            (x, y) = self.from_row_col_coords_to_pygame_coords(row, col)

            pygame.draw.circle(self.win, "green", (x, y), width)

    def draw_green_lines(self):
        """
        Draws green lines between connected nodes using the adjacency list.
        Ensures each edge is drawn only once.
        """
        adjacency_list = self.get_adjacency_list()

        drawn_edges = set()  # To prevent drawing duplicate edges

        for start_cell, neighbors in adjacency_list.items():
            start_cell_py_coords = self.from_num_coords_to_pygame_coords(start_cell)

            for neighbor_cell, _ in neighbors:  # (neighbor, weight)
                if (neighbor_cell, start_cell) in drawn_edges:
                    continue  # Skip if already drawn (prevents duplicates)

                neighbor_cell_py_coords = self.from_num_coords_to_pygame_coords(
                    neighbor_cell
                )
                pygame.draw.line(
                    self.win, "green", start_cell_py_coords, neighbor_cell_py_coords, 2
                )
                drawn_edges.add((start_cell, neighbor_cell))  # Mark as drawn

            pygame.display.update()  # Refresh the display

    def from_row_col_coords_to_pygame_coords(self, row, col):
        """ """
        x = self.cell_size * col + self.cell_size / 2
        y = self.cell_size * row + self.cell_size / 2
        return (x, y)

    def from_num_coords_to_pygame_coords(self, num_coord, for_nodes=True):
        """ """
        if for_nodes:
            (row, col) = self.num_to_ij(num_coord)
            x = self.cell_size * col + self.cell_size / 2
            y = self.cell_size * row + self.cell_size / 2
            return (int(x), int(y))
        else:
            (row, col) = self.num_to_ij(num_coord)
            x = self.cell_size * col
            y = self.cell_size * row
            return (int(x), int(y))

    def is_node(self, n):
        """
        returns true if a cell is either start, end, dead end or crossroad
        """

        if n == 1 or n == self.rows * self.cols:
            return True

        row, col = self.num_to_ij(n)
        cell = self.get_cell(row, col)
        counter = 0

        for direction in cell.walls:
            if cell.walls[direction]:
                counter += 1

        if counter != 2:
            return True
        else:
            return False

    def get_list_of_nodes(self):
        """
        returns a list of the nodes
        """
        list = []
        for row in self.grid:
            for cell in row:
                if self.is_node(self.ij_to_num(cell.row, cell.col)):
                    list.append(self.ij_to_num(cell.row, cell.col))
        return list

    def get_path_2_nodes(self, start, end):
        """
        returns the shortest path between 2 nodes
        """

    def get_reduced_adjacency_list(self): ...

    def dfs(self):
        operations = 0
        self.visited = {1}
        self.stack.append(1)

        while self.end not in self.visited:
            row, col = self.num_to_ij(self.current)
            self.draw_square(row, col, background_col="orange")
            operations += 1

            neighbors = self.adjacency_list[self.current]
            unvisited = [n[0] for n in neighbors if n[0] not in self.visited]

            if unvisited:
                chosen_neighbor = random.choice(unvisited)
                self.stack.append(chosen_neighbor)
                self.visited.add(chosen_neighbor)
                self.current = chosen_neighbor
            else:
                self.stack.pop()
                self.current = self.stack[-1]

            # Draw the current cell in green
            row, col = self.num_to_ij(self.current)
            self.draw_square(row, col, background_col="green")
            time.sleep(0)

        # Draw the end cell in orange before showing final path
        x, y = self.from_num_coords_to_pygame_coords(self.end, for_nodes=False)
        pygame.draw.rect(self.win, "orange", (x, y, self.cell_size, self.cell_size))
        time.sleep(0)

        # Redraw the complete path in red, including the end cell
        for cell in self.stack:
            row, col = self.num_to_ij(cell)
            self.draw_square(row, col, background_col="red")
            time.sleep(0)

        return list(self.stack), operations

    def h(self, n, null=False):
        """
        heuristic function for a_star
        null = True if you want to use dijkstra
        """
        if null:
            return 0

        # Manhattan distance
        row, col = self.num_to_ij(n)
        end_row, end_col = self.num_to_ij(self.end)
        return abs(row - end_row) + abs(col - end_col)

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def a_star(self, dijkstra=False):
        self.visited = {1}  # Start with the first cell as visited
        operations = 0
        count = 0
        open_set = PriorityQueue()
        open_set.put((self.h(1, null=dijkstra), count, 1))
        came_from = {}
        g_score = {
            spot: float("inf")
            for row in self.grid
            for spot in [self.ij_to_num(cell.row, cell.col) for cell in row]
        }
        g_score[1] = 0
        f_score = {
            spot: float("inf")
            for row in self.grid
            for spot in [self.ij_to_num(cell.row, cell.col) for cell in row]
        }
        f_score[1] = self.h(1, null=dijkstra)
        open_set_hash = {1}

        # Draw the starting cell as visited (orange)
        row, col = self.num_to_ij(1)
        self.draw_square(row, col, background_col="orange")
        last_current = 1  # Starting cell

        while not open_set.empty():
            current = open_set.get()[2]  # Get the current cell
            open_set_hash.remove(current)

            # Mark the previous cell as visited (orange)
            if last_current is not None and last_current != current:
                row, col = self.num_to_ij(last_current)
                self.draw_square(row, col, background_col="orange")

            # Draw the current cell in green
            row, col = self.num_to_ij(current)
            self.draw_square(row, col, background_col="green")
            operations += 1
            last_current = current
            time.sleep(0)  # Minimal delay

            # If the end is reached, reconstruct the path
            if current == self.end:
                # Draw the end cell in orange
                row, col = self.num_to_ij(self.end)
                self.draw_square(row, col, background_col="orange")
                time.sleep(0)

                # Reconstruct and then draw the final path in red
                path = self.reconstruct_path(came_from, current)
                for cell in path:
                    row, col = self.num_to_ij(cell)
                    self.draw_square(row, col, background_col="red")
                    time.sleep(0)
                return path, operations

            # Process neighbors
            for neighbor, weight in self.adjacency_list[current]:
                temp_g_score = g_score[current] + weight
                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.h(neighbor, null=dijkstra)
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        self.visited.add(neighbor)  # Mark the neighbor as visited

                        # Draw the neighbor as visited (orange)
                        row, col = self.num_to_ij(neighbor)
                        self.draw_square(row, col, background_col="orange")

        return None

    def bfs(self):
        operations = 0
        self.visited = {1}
        queue = [
            (self.current, [self.current])
        ]  # queue stores (current_cell, path_so_far)
        solution = None

        while queue:
            current, path = queue.pop(0)

            if current == self.end:
                solution = (
                    path  # Found the end, and we already have the full solution path
                )
                break

            self.visited.add(current)

            # Visualize the exploration
            row, col = self.num_to_ij(current)
            self.draw_square(row, col, background_col="orange")
            operations += 1

            # Explore all neighbors (each neighbor is a tuple: (neighbor, weight))
            for neighbor_tuple in self.adjacency_list[current]:
                neighbor = (
                    neighbor_tuple[0]
                    if isinstance(neighbor_tuple, tuple)
                    else neighbor_tuple
                )
                if neighbor not in self.visited and neighbor not in [c for c, _ in queue]:
                    queue.append((neighbor, path + [neighbor]))

        # Draw the final path in red, including the end cell
        if solution:
            for cell in solution:
                row, col = self.num_to_ij(cell)
                self.draw_square(row, col, background_col="red")
        return solution, operations