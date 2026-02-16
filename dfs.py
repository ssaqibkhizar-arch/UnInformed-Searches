def dfs(graph, start, goal,visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    if start == goal:
        return True
    for neighbor in graph[start]:
        if neighbor not in visited:
            if dfs(graph, neighbor, goal, visited):
                return True
    return False
    