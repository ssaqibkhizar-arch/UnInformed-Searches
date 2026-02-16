import pygame
import random

# Import colors from main or define them locally for checking
RED = (255, 65, 54)
GREEN = (46, 204, 64)
BLUE = (0, 116, 217)

def iddfs_visualizer(draw_func, grid, start, end):
    # IDDFS tries depth 0, then 1, then 2, etc.
    # We cap it at 50 to prevent infinite loops if unreachable
    max_depth = 50 
    
    for depth_limit in range(max_depth):
        
        # 1. VISUAL RESET
        # We must clear the "Visited" and "Frontier" nodes from the previous
        # shallow iteration to show that a NEW, deeper search is starting.
        # We do NOT clear walls.
        reset_search_colors(grid)
        
        # 2. Run DLS with the new limit
        # If it returns True, we found the target!
        if dls_with_limit(draw_func, grid, start, end, depth_limit):
            return True
            
    return False

def reset_search_colors(grid):
    """Clears Red/Green/Blue colors but keeps Walls, Start, and End."""
    for row in grid:
        for node in row:
            # Check if color is Visited(Red), Frontier(Green), or Path(Blue)
            if node.color in {RED, GREEN, BLUE}:
                node.reset() # Turn back to White
                node.parent = None

def dls_with_limit(draw_func, grid, start, end, limit):
    """Standard DLS but returns True/False immediately."""
    stack = [(start, 0)]
    visited = set()
    
    directions = [
        (0, -1), (1, 0), (0, 1), (1, 1), 
        (-1, 0), (-1, -1), (1, -1), (-1, 1)
    ]
    
    loop_count = 0

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current, depth = stack.pop() # LIFO

        if current == end:
            return True

        # --- Dynamic Obstacles ---
        loop_count += 1
        if loop_count % 15 == 0:
            if random.random() < 0.01:
                spawn_dynamic_obstacle(grid, start, end)

        if current.is_wall():
            continue

        # --- Limit Check ---
        if depth >= limit:
            continue
            
        visited.add(current)
        
        if current != start:
            current.make_closed() # Red
            
        # Neighbors
        row, col = current.row, current.col
        rows = len(grid)
        
        for dr, dc in directions:
             r, c = row + dr, col + dc
             if 0 <= r < rows and 0 <= c < rows:
                 neighbor = grid[r][c]
                 if not neighbor.is_wall() and neighbor not in visited:
                     neighbor.parent = current
                     neighbor.make_open() # Green
                     # Add to stack with Depth + 1
                     stack.append((neighbor, depth + 1))
        
        draw_func()
        
    return False

def spawn_dynamic_obstacle(grid, start, end):
    rows = len(grid)
    r = random.randint(0, rows-1)
    c = random.randint(0, rows-1)
    node = grid[r][c]
    if node != start and node != end and not node.is_wall():
        node.make_wall()