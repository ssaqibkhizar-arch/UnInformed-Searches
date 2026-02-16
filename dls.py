
def DLS(graph, start, goal, limit, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    if start == goal:
        return True
    if limit <= 0:
        return False
    for neighbor in graph[start]:
        if neighbor not in visited:
            if DLS(graph, neighbor, goal, limit - 1, visited):
                return True
    visited.remove(start)
    return False
    