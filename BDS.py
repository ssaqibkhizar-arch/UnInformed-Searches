# function for bidirectional search algorithm
def BDS(graph, start, goal, visited_start=None, visited_goal=None):
    if visited_start is None:
        visited_start = set()
    if visited_goal is None:
        visited_goal = set()
    
    visited_start.add(start)
    visited_goal.add(goal)
    
    if start == goal:
        return True
    
    # Explore neighbors from the start side
    for neighbor in graph[start]:
        if neighbor not in visited_start:
            if BDS(graph, neighbor, goal, visited_start, visited_goal):
                return True
    
    # Explore neighbors from the goal side
    for neighbor in graph[goal]:
        if neighbor not in visited_goal:
            if BDS(graph, start, neighbor, visited_start, visited_goal):
                return True
    
    return False