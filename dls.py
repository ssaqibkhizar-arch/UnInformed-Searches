import pygame
import random

def dls_visualizer(draw_func, grid, start, end, limit=10):
    # 1. Stack stores (Node, Depth)
    # DFS is LIFO (Last In, First Out)
    stack = [(start, 0)]
    visited = set()
    
    # 2. Movement: 8 Directions (Clockwise)
    # Up, Right, Bottom, Bottom-Right, Left, Top-Left + (Top-Right, Bottom-Left)
    directions = [
        (0, -1), (1, 0), (0, 1), (1, 1), 
        (-1, 0), (-1, -1), (1, -1), (-1, 1)
    ]
    
    loop_count = 0

    while stack:
        # --- GUI Safety ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        # --- Pop Current ---
        current, depth = stack.pop() # LIFO

        if current == end:
            return True

        # --- DYNAMIC OBSTACLES (Assignment Req) ---
        loop_count += 1
        if loop_count % 10 == 0:
            if random.random() < 0.02:
                spawn_dynamic_obstacle(grid, start, end)

        if current.is_wall():
            continue

        # --- DEPTH LIMIT CHECK ---
        # If we reached the limit, do NOT expand neighbors
        if depth >= limit:
            continue

        if current != start:
            current.make_closed()

        visited.add(current)

        # --- EXPLORE NEIGHBORS ---
        row, col = current.row, current.col
        rows = len(grid)

        # Iterate backwards to ensure "Up" is popped first (Standard DFS trick)
        # But for DLS visualization, standard order is fine.
        for dr, dc in directions:
            r, c = row + dr, col + dc

            if 0 <= r < rows and 0 <= c < rows:
                neighbor = grid[r][c]
                
                # Check bounds, walls, and loops
                # Note: We must allow re-visiting nodes if we found a shorter path to them? 
                # For simple DLS/DFS, standard 'visited' check is usually sufficient 
                # to prevent cycles.
                if not neighbor.is_wall() and neighbor not in visited:
                    neighbor.parent = current
                    neighbor.make_open()
                    stack.append((neighbor, depth + 1)) # Add 1 to depth

        draw_func()

    return False

def spawn_dynamic_obstacle(grid, start, end):
    rows = len(grid)
    r = random.randint(0, rows-1)
    c = random.randint(0, rows-1)
    node = grid[r][c]
    if node != start and node != end and not node.is_wall():
        node.make_wall()