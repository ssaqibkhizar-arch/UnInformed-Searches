# dfs.py
from collections import deque

# Directions in Counter-Clockwise order (so they POP from stack in Clockwise order)
# The assignment asks to explore: Up, Right, Bottom, Bottom-Right, etc.
# So we push them in REVERSE of that priority.
def get_neighbors(node, grid, rows, cols):
    row, col = node.row, node.col
    neighbors = []
    
    # We list moves in REVERSE priority for the Stack
    # Priority desired: Up -> Top-Right -> Right -> Bottom-Right -> Bottom -> Bottom-Left -> Left -> Top-Left
    # So we push: Top-Left first... Up last.
    
    moves = [
        (-1, -1), # Top-Left
        (-1, 0),  # Left
        (1, -1),  # Bottom-Left (Check strictness of your prompt directions again, this is standard 8-way)
        (0, 1),   # Bottom
        (1, 1),   # Bottom-Right
        (1, 0),   # Right
        (1, -1),  # Top-Right
        (0, -1)   # Up (Last pushed = First popped)
    ]

    for dr, dc in moves:
        r, c = row + dr, col + dc
        # Check bounds and if it's not a wall
        if 0 <= r < rows and 0 <= c < cols and not grid[r][c].is_wall():
            neighbors.append(grid[r][c])
            
    return neighbors

def dfs_visualizer(draw_func, grid, start, end):
    """
    Args:
        draw_func: A function we call to update the GUI
        grid: The 2D array of Nodes
        start: The start Node
        end: The target Node
    """
    stack = [start]
    visited = {start}

    while stack:
        # 1. Get current node
        current = stack.pop()

        # 2. If we found the target, we are done
        if current == end:
            current.make_target()
            return True # Success

        # 3. Visualization Hook: Don't color the start/end nodes
        if current != start:
            current.make_closed() # Color it "Explored" (e.g., Red/Yellow)
            
        # 4. Update the screen immediately to show this step
        draw_func() 

        # 5. Process Neighbors
        neighbors = get_neighbors(current, grid, len(grid), len(grid[0]))
        
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                neighbor.parent = current # Keep track of path
                stack.append(neighbor)
                
                # Visualization Hook: Mark as in "Frontier" (e.g., Green/Blue)
                if neighbor != end:
                    neighbor.make_open()
                draw_func()

    return False # Failed to find path