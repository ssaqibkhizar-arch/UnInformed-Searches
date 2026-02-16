import pygame

def dfs_visualizer(draw_func, grid, start, end):
    # 1. Setup
    stack = [start]
    visited = {start}
    
    # 2. Loop
    while stack:
        # --- SAFETY: Allow quitting during search ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        # --------------------------------------------

        current = stack.pop()

        # 3. Check if Goal Found
        if current == end:
            return True # Success! Returns to main.py

        # 4. Process Node (Color it Red)
        if current != start:
            current.make_closed()

        # 5. Get Neighbors (Counter-Clockwise)
        # We push them so they pop in Clockwise order (Up, Right, Down, Left)
        neighbors = []
        row, col = current.row, current.col
        rows = len(grid)
        
        # Directions: Top, Right, Bottom, Left
        # We add them in REVERSE order of how we want to search
        moves = [(0, -1), (1, 0), (0, 1), (-1, 0)] 
        
        for dr, dc in moves:
            r, c = row + dr, col + dc
            if 0 <= r < rows and 0 <= c < rows:
                neighbor = grid[r][c]
                if not neighbor.is_wall() and neighbor not in visited:
                    visited.add(neighbor)
                    neighbor.parent = current # CRITICAL: Remember path
                    stack.append(neighbor)
                    neighbor.make_open() # Color it Green/Purple

        # 6. Update Screen
        draw_func()

    return False # Stack empty, no path found