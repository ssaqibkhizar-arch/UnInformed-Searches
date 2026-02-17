import pygame

def dfsVisualizer(drawFunc, grid, start, end):
    stack = [start]
    visited = {start}
    
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        # DFS uses a stack (LIFO)
        current = stack.pop()

        if current == end:
            return True 

        if current != start:
            current.makeClosed()
        
        # Using neighbors pre-calculated in main.py:
        # Up, Right, Bottom, Bottom-Right, Left, Top-Left
        for neighbor in current.neighbors:
            if not neighbor.isWall() and neighbor not in visited:
                visited.add(neighbor)
                neighbor.parent = current 
                stack.append(neighbor)
                
                if neighbor != end:
                    neighbor.makeOpen()

        drawFunc()

    return False