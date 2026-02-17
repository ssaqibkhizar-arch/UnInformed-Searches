import pygame
import heapq

def ucsVisualizer(drawFunc, grid, start, end):
    count = 0
    openSet = []
    # Priority Queue: (cost, entry_count, node)
    heapq.heappush(openSet, (0, count, start))
    
    costSoFar = {node: float('inf') for row in grid for node in row}
    costSoFar[start] = 0
    
    visited = {start}

    while openSet:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        # Pop the node with the lowest cumulative cost
        currentCost, _, current = heapq.heappop(openSet)

        if current == end:
            return True

        if current.isWall():
            continue

        if current != start:
            current.makeClosed()

        # Using the neighbors defined in main.py:
        # (Up, Right, Bottom, Bottom-Right, Left, Top-Left)
        for neighbor in current.neighbors:
            # new_cost = current cumulative cost + weight of the neighbor node
            newCost = costSoFar[current] + neighbor.weight

            if not neighbor.isWall() and newCost < costSoFar[neighbor]:
                costSoFar[neighbor] = newCost
                neighbor.parent = current
                
                count += 1
                heapq.heappush(openSet, (newCost, count, neighbor))
                
                if neighbor != end:
                    neighbor.makeOpen()
                visited.add(neighbor)

        drawFunc()

    return False