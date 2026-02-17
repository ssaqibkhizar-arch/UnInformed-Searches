# Uninformed Search Algorithms Visualizer

A Python-based visualization tool for various uninformed pathfinding algorithms using the `pygame` library. This project demonstrates how different search strategies explore a grid to find the shortest path between a Start node and an End node.

## 👥 Authors

* **Saqib Ali** (Roll No: 24P-0726)
* **Abbas Raza** (Roll No: 24P-0728)

---

## 🚀 Features

* **Interactive Grid:** Draw walls and obstacles with your mouse.
* **Real-time Visualization:** Watch how algorithms explore nodes (Green/Red) and find the path (Blue).
* **Multiple Algorithms:** Switch between 6 different search strategies instantly.
* **Weighted Nodes:** Random weight generation for testing cost-based algorithms like Uniform Cost Search.

## 🛠️ Algorithms Implemented

This project visualizes the following uninformed search strategies:

1.  **Breadth-First Search (BFS):** Guarantees the shortest path in an unweighted grid.
2.  **Depth-First Search (DFS):** Explores deep paths first; not optimal but memory efficient.
3.  **Uniform Cost Search (UCS):** Explores paths based on lowest cost (Dijkstra's algorithm).
4.  **Depth-Limited Search (DLS):** A variation of DFS with a depth limit (default: 10).
5.  **Iterative Deepening DFS (IDDFS):** Repeatedly runs DLS with increasing depth limits.
6.  **Bidirectional Search:** Runs two simultaneous searches from Start and End to meet in the middle.

---

## ⚙️ Prerequisites

* **Python 3.x**
* **Pygame** library

## 📥 Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Install dependencies:**
    You only need `pygame` to run this project.
    ```bash
    pip install pygame
    ```

3.  **Run the application:**
    ```bash
    python main.py
    ```

---

## 🎮 Controls & Usage

### **Mouse Controls**
* **Left Click:** Place Start (Orange), End (Turquoise), and Walls (Black).
    * *First click:* Places Start Node.
    * *Second click:* Places End Node.
    * *Subsequent clicks/drag:* Draws Walls.
* **Right Click:** Erase nodes (Turn them back to White).

### **Keyboard Shortcuts**
* **`SPACE`**: Start the visualization (runs the selected algorithm).
* **`C`**: Clear the grid (removes walls and paths).
* **`R`**: Generate random weights (useful for UCS).
* **`1`**: Select **BFS** (Breadth-First Search).
* **`2`**: Select **DFS** (Depth-First Search).
* **`3`**: Select **UCS** (Uniform Cost Search).
* **`4`**: Select **DLS** (Depth-Limited Search).
* **`5`**: Select **IDDFS** (Iterative Deepening DFS).
* **`6`**: Select **Bidirectional Search**.

---

## 📂 Project Structure

```text
├── main.py         # The main GUI entry point
├── bfs.py          # Breadth-First Search implementation
├── dfs.py          # Depth-First Search implementation
├── ucs.py          # Uniform Cost Search implementation
├── dls.py          # Depth-Limited Search implementation
├── iddfs.py        # Iterative Deepening DFS implementation
├── bds.py          # Bidirectional Search implementation
└── README.md       # Project documentation