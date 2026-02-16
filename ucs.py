import pygame
import heapq # Python's Priority Queue implementation
import random

def ucs_visualizer(draw_func, grid, start, end):
    # 1. Setup Priority Queue: Stores tuples of (cost, count, node)
    # 'count' is a tie-breaker so Python doesn't try to compare Nodes directly
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    
    # 2. Track Costs & Visited
    # Initialize all costs to Infinity
    cost_so_far = {node: float('inf') for row in grid for node in row}
    cost_so_far[start] = 0
    
    visited = {start}

    # 3. Directions (8-way Clockwise)
    directions = [
        (0, -1), (1, -1), (1, 0), (1, 1), 
        (0, 1), (-1, 1), (-1, 0), (-1, -1)
    ]
    
    loop_count = 0

    while open_set:
        # --- GUI Safety ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        # --- Get Lowest Cost Node ---
        current_cost, _, current = heapq.heappop(open_set)

        if current == end:
            return True

        # --- Dynamic Obstacles (Assignment Req) ---
        loop_count += 1
        if loop_count % 15 == 0: # Slightly slower spawn rate for UCS
            if random.random() < 0.02:
                spawn_dynamic_obstacle(grid, start, end)

        # If a wall spawned on our path, skip this node
        if current.is_wall():
            continue

        if current != start:
            current.make_closed() # Red (Visited)

        # --- Explore Neighbors ---
        row, col = current.row, current.col
        rows = len(grid)

        for dr, dc in directions:
            r, c = row + dr, col + dc

            if 0 <= r < rows and 0 <= c < rows:
                neighbor = grid[r][c]
                
                # Calculate new cost (Current + 1 for step)
                new_cost = cost_so_far[current] + neighbor.weight

                # If neighbor is not a wall AND we found a cheaper way to get there
                if not neighbor.is_wall() and new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    neighbor.parent = current
                    
                    count += 1
                    heapq.heappush(open_set, (new_cost, count, neighbor))
                    neighbor.make_open() # Green (Frontier)
                    visited.add(neighbor)

        draw_func()

    return False

def spawn_dynamic_obstacle(grid, start, end):
    rows = len(grid)
    r = random.randint(0, rows-1)
    c = random.randint(0, rows-1)
    node = grid[r][c]
    if node != start and node != end and not node.is_wall():
        node.make_wall()