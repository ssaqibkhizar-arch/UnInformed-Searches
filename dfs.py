import pygame

def dfs_visualizer(draw_func, grid, start, end):
    stack = [start]
    visited = {start}
    
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = stack.pop()

        if current == end:
            return True 

        if current != start:
            current.make_closed()

        row, col = current.row, current.col
        rows = len(grid)
        
        moves = [(0, -1), (1, 0), (0, 1), (-1, 0)] 
        
        for dr, dc in moves:
            r, c = row + dr, col + dc
            if 0 <= r < rows and 0 <= c < rows:
                neighbor = grid[r][c]
                if not neighbor.is_wall() and neighbor not in visited:
                    visited.add(neighbor)
                    neighbor.parent = current 
                    stack.append(neighbor)
                    neighbor.make_open()

        draw_func()

    return False