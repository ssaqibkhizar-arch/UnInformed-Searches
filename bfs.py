import pygame
import random
from collections import deque

def bfs_visualizer(draw_func, grid, start, end):
    queue = deque([start])
    visited = {start}
    
    directions = [
        (0, -1), (1, -1), (1, 0), (1, 1), 
        (0, 1), (-1, 1), (-1, 0), (-1, -1)
    ]
    
    loop_count = 0 

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        
        current = queue.popleft() 

        if current == end:
            return True 

        loop_count += 1
        if loop_count % 10 == 0:
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
                
                if not neighbor.is_wall() and neighbor not in visited:
                    visited.add(neighbor)
                    neighbor.parent = current
                    queue.append(neighbor)
                    neighbor.make_open() 

        draw_func()

    return False

def spawn_dynamic_obstacle(grid, start, end):
    rows = len(grid)
    r = random.randint(0, rows-1)
    c = random.randint(0, rows-1)
    node = grid[r][c]
    
    if node != start and node != end and not node.is_wall():
        node.make_wall()