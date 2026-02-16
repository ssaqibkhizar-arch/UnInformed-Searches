import dls
def IDDFS(graph, start, goal):
    depth = 0
    while True:
        result = dls.DLS(graph, start, goal, depth)
        if result is not None:
            return result
        depth += 1