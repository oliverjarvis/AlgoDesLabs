import sys
import networkx as nx

def parser(file):
    # load data
    vertices_count, edge_count, cardinality = tuple(map(int, next(file).split()))

    s, t = tuple(next(file).split())

    vertices = [next(file).split() for _ in range(vertices_count)]

    vertices_name = {v[0]: i for i, v in enumerate(vertices)}

    s, t = vertices_name[s], vertices_name[t]

    edges = [next(file).strip().split() for _ in range(edge_count)]
    directed = all([edge[1] == "->" for edge in edges]) # True if the graph is directed
    edges = [(vertices_name[edge[0]], vertices_name[edge[2]]) for edge in edges]

    all_vertices = list(map(lambda x: vertices_name[x[0]], vertices))
    red_vertices = list(map(lambda x: vertices_name[x[0]], filter(lambda x: len(x) == 2, vertices)))

    G = nx.DiGraph()

    for v in edges:
        G.add_edge(v[0], v[1])

    # set node attributes to red or false for not red
    for v in all_vertices:
        if v in G.nodes:
            if v in red_vertices:
                G.nodes[v]["red"] = True
            else:
                G.nodes[v]["red"] = False

    # If the graph is undirected, add the edges in the opposite direction
    if not directed:
        for e in edges:
            G.add_edge(e[1], e[0])
    
    return G, s, t