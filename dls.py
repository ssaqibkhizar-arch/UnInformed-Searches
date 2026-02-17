import pygame

def dlsVisualizer(drawFunc, grid, start, end, limit=10):
    # Stack stores (Node, Depth)
    # DFS is LIFO (Last In, First Out)
    stack = [(start, 0)]
    visited = set()
    
    while stack:
        # --- GUI Safety ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        # --- Pop Current ---
        current, depth = stack.pop()

        if current == end:
            return True

        if current.isWall():
            continue

        # --- DEPTH LIMIT CHECK ---
        # If we reached the limit, do NOT expand neighbors
        if depth >= limit:
            continue

        if current != start:
            current.makeClosed()

        visited.add(current)

        # --- EXPLORE NEIGHBORS ---
        # Using the neighbors list pre-populated in main.py
        # Strictly enforces: Up, Right, Bottom, Bottom-Right, Left, Top-Left
        for neighbor in current.neighbors:
            # Standard 'visited' check to prevent cycles in DLS
            if not neighbor.isWall() and neighbor not in visited:
                neighbor.parent = current
                
                if neighbor != end:
                    neighbor.makeOpen()
                
                stack.append((neighbor, depth + 1))

        drawFunc()

    return False