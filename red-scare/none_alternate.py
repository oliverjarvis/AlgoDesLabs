import sys
import networkx as nx
import matplotlib.pyplot as plt

def parser():

    file = open("data/G-ex.txt")

    vertices_count, edge_count, cardinality = tuple(map(int, next(file).split()))
    s, t = tuple(next(file).split())

    vertices = [next(file).split() for _ in range(vertices_count)]
    edges = [next(file).strip().split() for _ in range(edge_count)]

    vertices_name = {v[0]: i + 1 for i, v in enumerate(vertices)}
    edges = [(vertices_name[x[0]], vertices_name[x[2]]) for x in edges]
    s, t = vertices_name[s], vertices_name[t]

    #all_vertices = list(map(lambda x: vertices_name[x[0]], vertices))
    black_vertices = list(map(lambda x: vertices_name[x[0]], filter(lambda x: len(x) != 2, vertices)))
    red_vertices = list(map(lambda x: vertices_name[x[0]], filter(lambda x: len(x) == 2, vertices)))

    graph = dict()
    for v in black_vertices:
        graph[v] = 'black'
    for v in red_vertices:
        graph[v] = 'red'
    
    G = nx.Graph()
    for v, attr in graph.items():
        G.add_node(v, color=attr)
    G.add_edges_from(edges)

    return G, s, t


def none(G, s, t):

    graph_data = list(G.nodes.data())

    for v, attr in graph_data:
        if attr['color'] == 'red':
            G.remove_node(v)    

    try:
        path = nx.shortest_path_length(G, source=s, target=t)
    except nx.exception.NetworkXNoPath:
        path = -1
        
    return path


def alternating(G, s, t):

    graph_data = dict(G.nodes.data())
    edges = list(G.edges)

    for u, v in edges:
        u_c = graph_data[u]['color']
        v_c = graph_data[v]['color']
        if u_c == v_c:
            G.remove_edge(u, v)
    
    return nx.has_path(G, s, t)
        
G, s, t = parser()

print(alternating(G, s, t))




