import sys
import networkx as nx

file = open("skilevel.txt")
# load data
vertices_count, edge_count, cardinality = tuple(map(int, next(file).split()))

s, t = tuple(next(file).split())

vertices = [next(file).split() for _ in range(vertices_count)]

vertices_name = {v[0]: i + 1 for i, v in enumerate(vertices)}

s, t = vertices_name[s], vertices_name[t]

edges = [next(file).strip().split() for _ in range(edge_count)]
edges = [(vertices_name[x[0]], vertices_name[x[2]]) for x in edges]

all_vertices = list(map(lambda x: vertices_name[x[0]], vertices))
red_vertices = list(map(lambda x: vertices_name[x[0]], filter(lambda x: len(x) == 2, vertices)))

G = nx.Graph()
for v in edges:
    G.add_edge(v[0], v[1])
