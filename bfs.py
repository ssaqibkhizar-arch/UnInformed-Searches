import queue
def BFS(graph, start, goal, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    q = queue.Queue()
    q.put(start)
    while not q.empty():
        node = q.get()
        if node == goal:
            return True
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                q.put(neighbor)
    return False