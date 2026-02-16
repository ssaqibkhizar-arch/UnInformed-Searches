import pygame
import random

RED = (255, 65, 54)
GREEN = (46, 204, 64)
BLUE = (0, 116, 217)

def iddfs_visualizer(draw_func, grid, start, end):
    max_depth = 50 
    
    for depth_limit in range(max_depth):
        reset_search_colors(grid)
        
        if dls_with_limit(draw_func, grid, start, end, depth_limit):
            return True
            
    return False

def reset_search_colors(grid):
    for row in grid:
        for node in row:
            if node.color in {RED, GREEN, BLUE}:
                node.reset() 
                node.parent = None

def dls_with_limit(draw_func, grid, start, end, limit):
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

        current, depth = stack.pop() 

        if current == end:
            return True

        loop_count += 1
        if loop_count % 15 == 0:
            if random.random() < 0.01:
                spawn_dynamic_obstacle(grid, start, end)

        if current.is_wall():
            continue

        if depth >= limit:
            continue
            
        visited.add(current)
        
        if current != start:
            current.make_closed() 
            
        row, col = current.row, current.col
        rows = len(grid)
        
        for dr, dc in directions:
             r, c = row + dr, col + dc
             if 0 <= r < rows and 0 <= c < rows:
                 neighbor = grid[r][c]
                 if not neighbor.is_wall() and neighbor not in visited:
                     neighbor.parent = current
                     neighbor.make_open() 
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