# 🧩 Maze Visualizer & Solver

A Pygame-based application for **generating, visualizing, and solving mazes** using various classical pathfinding algorithms, with optional obstacles and dynamic resizing support.

---

## 🚀 Features

- **Maze Generation**
  - *Perfect Maze:* Generated using recursive backtracking with no loops.
  - *Non-perfect Maze:* Includes optional loops for more complex topologies.
  - *Obstacle Placement:* Randomized and visualized as black squares.

- **Algorithms**
  - Depth-First Search (DFS)
  - Breadth-First Search (BFS)
  - A* Search
  - Dijkstra's Algorithm (A* with zero heuristic)

- **Interactive UI**
  - Clickable buttons for:
    - Generating maze types
    - Adding/removing obstacles
    - Choosing endpoints (bottom-right or deepest)
    - Running solving algorithms

- **Visualization**
  - Real-time drawing of maze construction and pathfinding steps.
  - Custom color-coding:
    - Purple: Visited path
    - Red: Final path
    - Black: Obstacles
    - Orange: Current exploration
    - Green: Endpoint

- **Responsive Layout**
  - Automatically adjusts button layout and cell size when window is resized.

---

## 📦 Project Structure

```text
├── main.py        # Entry point with Pygame loop and UI logic
├── classes.py     # Grid, Cell, and Button classes with core logic
├── utils.py       # Utility functions (quit handling, layout updates)
├── Buttons/       # Folder with button images
├── README.md      # You're reading it!
```

---

## 🧠 How It Works

### Grid Representation
- The maze is a grid of `Cell` objects, each with walls on four sides.
- Recursive backtracking removes walls to form paths.

### Algorithms
- **DFS:** Uses a stack to go deep before backtracking.
- **BFS:** Uses a queue to ensure the shortest path in unweighted graphs.
- **A\*:** Uses `f(n) = g(n) + h(n)` with Manhattan distance as `h`.
- **Dijkstra:** Special case of A* with `h(n) = 0`.

### Obstacles
- When enabled, cells may become impassable and increase path cost to 1000.

---

## 🕹️ Controls

| Action                        | Description                              |
|------------------------------|------------------------------------------|
| `Perfect`                    | Generate a perfect maze                  |
| `Non-perfect`                | Generate maze with loops                 |
| `Obstacles / No Obstacles`  | Toggle obstacle placement                |
| `Deepest`                    | Set the end cell as the farthest from start |
| `Bottom Right`              | Set the end cell as the bottom-right corner |
| `DFS`, `BFS`, `A*`, `Dijkstra` | Solve the maze using the chosen algorithm |

---

## 🧰 Requirements

- Python 3.7+
- [Pygame](https://www.pygame.org/)
- [heapdict](https://pypi.org/project/heapdict/)

### Install dependencies

```bash
pip install pygame heapdict

