import pygame
from collections import deque

def bfsVisualizer(drawFunc, grid, start, end):
    queue = deque([start])
    visited = {start}
    
    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        
        current = queue.popleft() 

        if current == end:
            return True 

        if current.isWall():
            continue

        if current != start:
            current.makeClosed() 

        for neighbor in current.neighbors:
            if not neighbor.isWall() and neighbor not in visited:
                visited.add(neighbor)
                neighbor.parent = current
                queue.append(neighbor)
                
                if neighbor != end:
                    neighbor.makeOpen() 

        drawFunc()

    return False