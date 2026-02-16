import pygame
import heapq
import random

def ucs_visualizer(draw_func, grid, start, end):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    
    cost_so_far = {node: float('inf') for row in grid for node in row}
    cost_so_far[start] = 0
    
    visited = {start}

    directions = [
        (0, -1), (1, -1), (1, 0), (1, 1), 
        (0, 1), (-1, 1), (-1, 0), (-1, -1)
    ]
    
    loop_count = 0

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current_cost, _, current = heapq.heappop(open_set)

        if current == end:
            return True

        loop_count += 1
        if loop_count % 15 == 0:
            if random.random() < 0.02:
                spawn_dynamic_obstacle(grid, start, end)

        if current.is_wall():
            continue

        if current != start:
            current.make_closed()

        row, col = current.row, current.col
        rows = len(grid)

        for dr, dc in directions:
            r, c = row + dr, col + dc

            if 0 <= r < rows and 0 <= c < rows:
                neighbor = grid[r][c]
                
                new_cost = cost_so_far[current] + neighbor.weight

                if not neighbor.is_wall() and new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    neighbor.parent = current
                    
                    count += 1
                    heapq.heappush(open_set, (new_cost, count, neighbor))
                    neighbor.make_open()
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