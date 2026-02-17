import pygame

RED = (255, 65, 54)
GREEN = (46, 204, 64)
BLUE = (0, 116, 217)

def iddfsVisualizer(drawFunc, grid, start, end):
    maxDepth = 50 
    
    for depthLimit in range(maxDepth):
        resetSearchColors(grid)
        
        # We pass the pre-calculated neighbors to ensure 6-direction movement
        if dlsWithLimit(drawFunc, grid, start, end, depthLimit):
            return True
            
    return False

def resetSearchColors(grid):
    for row in grid:
        for node in row:
            if node.color in {RED, GREEN, BLUE}:
                node.reset() 
                node.parent = None

def dlsWithLimit(drawFunc, grid, start, end, limit):
    # Stack stores tuples of (Node, CurrentDepth)
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
            
        visited.add(current)
        
        if current != start:
            current.makeClosed() 
            
        # Using the neighbors defined in main.py (Up, Right, Bottom, Bottom-Right, Left, Top-Left)
        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.isWall():
                neighbor.parent = current
                neighbor.makeOpen() 
                stack.append((neighbor, depth + 1))
        
        drawFunc()
        
    return False