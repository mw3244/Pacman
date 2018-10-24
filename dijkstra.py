def Dijkstra(start, goal, nodes):
    graph = nodes.copy()
    shortest_distance = {}
    predecessors = {}
    unseen_nodes = graph

    #print('total unseen_nodes: ' + str(len(unseen_nodes)))

    infinity = 9999999
    path = []

    for node in unseen_nodes:
        shortest_distance[node] = infinity
    shortest_distance[start] = 0

    while unseen_nodes:
        min_node = None
        for node in unseen_nodes:
            if min_node is None:
                min_node = node
            elif shortest_distance[node] < shortest_distance[min_node]:
                min_node = node

        for child_node, weight in graph[min_node].items():
            if weight + shortest_distance[min_node] < shortest_distance[child_node]:
                shortest_distance[child_node] = weight + shortest_distance[min_node]
                predecessors[child_node] = min_node
        unseen_nodes.pop(min_node)

    current_node = goal
    while current_node != start:
        try:
            path.insert(0, current_node)
            current_node = predecessors[current_node]
        except KeyError:
            print('Path not reachable')
            break

    path.insert(0, start)
    if shortest_distance[goal] != infinity:
        #print('\nShortest distance: ', shortest_distance[goal])
        #print('Shortest path is: ' + str(path))
        return path
