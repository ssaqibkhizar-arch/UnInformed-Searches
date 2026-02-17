import pygame
import collections

RED = (255, 65, 54)      
GREEN = (46, 204, 64)    
PURPLE = (177, 13, 201)  
ORANGE = (255, 165, 0)   
BLUE = (0, 116, 217)     

def bidirectionalVisualizer(drawFunc, grid, start, end):
    startQ = collections.deque([start])
    endQ = collections.deque([end])
    
    startParents = {start: None}
    endParents = {end: None}
    

    while startQ and endQ:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        # --- Forward Search (Start -> End) ---
        if startQ:
            current = startQ.popleft()

            # Check if paths met
            if current in endParents:
                joinPaths(current, startParents, endParents, drawFunc)
                return True 

            if current != start:
                current.makeClosed() 
            
            for neighbor in current.neighbors:
                if neighbor not in startParents and not neighbor.isWall():
                    startParents[neighbor] = current
                    startQ.append(neighbor)
                    neighbor.makeOpen() 

        # --- Backward Search (End -> Start) ---
        if endQ:
            currentB = endQ.popleft()

            # Check if paths met
            if currentB in startParents:
                joinPaths(currentB, startParents, endParents, drawFunc)
                return True 

            if currentB != end:
                currentB.color = PURPLE 
            
            for neighbor in currentB.neighbors:
                if neighbor not in endParents and not neighbor.isWall():
                    endParents[neighbor] = currentB
                    endQ.append(neighbor)
                    neighbor.color = ORANGE

        drawFunc()

    return False

def joinPaths(meetNode, startParents, endParents, drawFunc):
    # Trace back to Start
    curr = meetNode
    while curr:
        curr.makePath()
        curr = startParents.get(curr)
        drawFunc()
        
    # Trace back to End
    curr = meetNode
    while curr:
        curr.makePath()
        curr = endParents.get(curr)
        drawFunc()