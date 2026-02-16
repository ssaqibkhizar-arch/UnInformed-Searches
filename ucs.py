
def UCS(graph, start, goal, visited=None, cost=0):
    if visited is None:
        visited = set()
    visited.add(start)
    if start == goal:
        return cost
    min_cost = float('inf')
    for neighbor, edge_cost in graph[start]:
        if neighbor not in visited:
            total_cost = UCS(graph, neighbor, goal, visited, cost + edge_cost)
            min_cost = min(min_cost, total_cost)
    visited.remove(start)
    return min_cost