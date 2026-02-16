import pygame
import random
from collections import deque

def bfs_visualizer(draw_func, grid, start, end):
    # 1. Setup Queue (FIFO for BFS)
    queue = deque([start])
    visited = {start}
    
    # 2. Movement: 8 Directions (Clockwise starting Up)
    # Up, Up-Right, Right, Bottom-Right, Bottom, Bottom-Left, Left, Top-Left
    directions = [
        (0, -1), (1, -1), (1, 0), (1, 1), 
        (0, 1), (-1, 1), (-1, 0), (-1, -1)
    ]
    
    # Counter to control random obstacle spawn rate
    loop_count = 0 

    while queue:
        # --- GUI INTERACTION ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        
        # --- ALGORITHM STEP ---
        current = queue.popleft() # Pop from Left (FIFO)

        if current == end:
            return True # Path Found!

        # --- DYNAMIC OBSTACLES (Assignment Req) ---
        # Every 10 steps, 2% chance to spawn a wall
        loop_count += 1
        if loop_count % 10 == 0:
            if random.random() < 0.02: # 2% chance
                spawn_dynamic_obstacle(grid, start, end)

        # Skip if the current node became a wall dynamically
        if current.is_wall():
            continue

        if current != start:
            current.make_closed() # Color Red (Visited)

        # --- EXPLORE NEIGHBORS ---
        row, col = current.row, current.col
        rows = len(grid)

        for dr, dc in directions:
            r, c = row + dr, col + dc

            if 0 <= r < rows and 0 <= c < rows:
                neighbor = grid[r][c]
                
                # Standard BFS Check: Not Wall AND Not Visited
                if not neighbor.is_wall() and neighbor not in visited:
                    visited.add(neighbor)
                    neighbor.parent = current
                    queue.append(neighbor)
                    neighbor.make_open() # Color Green (Frontier)

        # Update screen
        draw_func()

    return False

def spawn_dynamic_obstacle(grid, start, end):
    """Spawns a wall at a random empty location."""
    rows = len(grid)
    r = random.randint(0, rows-1)
    c = random.randint(0, rows-1)
    node = grid[r][c]
    
    # Don't block Start, End, or existing walls
    if node != start and node != end and not node.is_wall():
        node.make_wall()