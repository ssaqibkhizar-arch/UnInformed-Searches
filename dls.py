import pygame

def dlsVisualizer(drawFunc, grid, start, end, limit=10):
    stack = [(start, 0)]
    visited = set()
    
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current, depth = stack.pop()

        if current == end:
            return True

        if current.isWall():
            continue

        if depth >= limit:
            continue

        if current != start:
            current.makeClosed()

        visited.add(current)

        for neighbor in current.neighbors:
            if not neighbor.isWall() and neighbor not in visited:
                neighbor.parent = current
                
                if neighbor != end:
                    neighbor.makeOpen()
                
                stack.append((neighbor, depth + 1))

        drawFunc()

    return False