import pygame
import collections
import random

# Reuse colors or define distinct ones for the backward search
RED = (255, 65, 54)      # Forward Visited
GREEN = (46, 204, 64)    # Forward Frontier
PURPLE = (177, 13, 201)  # Backward Visited
ORANGE = (255, 165, 0)   # Backward Frontier (New Color)
BLUE = (0, 116, 217)     # Path

def bidirectional_visualizer(draw_func, grid, start, end):
    # 1. Two Queues
    start_q = collections.deque([start])
    end_q = collections.deque([end])
    
    # 2. Two Parent Trackers (Node -> Parent)
    start_parents = {start: None}
    end_parents = {end: None}
    
    # 3. Directions (8-way)
    directions = [
        (0, -1), (1, 0), (0, 1), (1, 1), 
        (-1, 0), (-1, -1), (1, -1), (-1, 1)
    ]
    
    loop_count = 0

    while start_q and end_q:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        # --- Dynamic Obstacles ---
        loop_count += 1
        if loop_count % 12 == 0:
            if random.random() < 0.02:
                spawn_dynamic_obstacle(grid, start, end)

        # === 1. EXPAND FORWARD SEARCH ===
        if start_q:
            current = start_q.popleft()

            # CHECK INTERSECTION
            if current in end_parents:
                join_paths(current, start_parents, end_parents, draw_func)
                return True # Done

            if current != start:
                current.make_closed() # Red
            
            # Neighbors
            for dr, dc in directions:
                r, c = current.row + dr, current.col + dc
                if 0 <= r < len(grid) and 0 <= c < len(grid):
                    neighbor = grid[r][c]
                    if not neighbor.is_wall() and neighbor not in start_parents:
                        start_parents[neighbor] = current
                        start_q.append(neighbor)
                        neighbor.make_open() # Green

        # === 2. EXPAND BACKWARD SEARCH ===
        if end_q:
            current_b = end_q.popleft()

            # CHECK INTERSECTION
            if current_b in start_parents:
                join_paths(current_b, start_parents, end_parents, draw_func)
                return True # Done

            if current_b != end:
                # Custom color for backward search (Purple)
                current_b.color = PURPLE 
            
            # Neighbors
            for dr, dc in directions:
                r, c = current_b.row + dr, current_b.col + dc
                if 0 <= r < len(grid) and 0 <= c < len(grid):
                    neighbor = grid[r][c]
                    if not neighbor.is_wall() and neighbor not in end_parents:
                        end_parents[neighbor] = current_b
                        end_q.append(neighbor)
                        # Custom color for backward frontier (Orange)
                        neighbor.color = ORANGE

        draw_func()

    return False

def join_paths(meet_node, start_parents, end_parents, draw_func):
    """
    Traces path from Start -> Meeting Point -> End.
    """
    # 1. Trace from Meeting Point back to Start
    curr = meet_node
    while curr:
        curr.make_path()
        curr = start_parents.get(curr)
        draw_func()
        
    # 2. Trace from Meeting Point back to End
    curr = meet_node
    while curr:
        curr.make_path()
        curr = end_parents.get(curr)
        draw_func()

def spawn_dynamic_obstacle(grid, start, end):
    rows = len(grid)
    r = random.randint(0, rows-1)
    c = random.randint(0, rows-1)
    node = grid[r][c]
    if node != start and node != end and not node.is_wall():
        node.make_wall()