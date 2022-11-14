from redscare import load_file, is_directed, create_graph

# test 1
path = "data/common-1-20.txt"
vertices_count, edge_count, cardinality, s, t, vertices, edges =     load_file(path)
directed =is_directed(edges)

G = create_graph(vertices,edges,directed)

assert s == 'start'
assert t == 'ender'
assert vertices_count == 20
assert edge_count == 0
assert cardinality == 9
assert G.nodes['purls']['red'] == True
assert directed == False

# test 2
path = "data/wall-p-1.txt"
vertices_count, edge_count, cardinality, s, t, vertices, edges =     load_file(path)
directed =is_directed(edges)

G = create_graph(vertices,edges,directed)

assert s == '7'
assert t == '0'
assert vertices_count == 8
assert edge_count == 8
assert cardinality == 1
assert G.nodes['3']['red'] == True
assert directed == False

# test 3
path = "data/ski-level3-1.txt"
vertices_count, edge_count, cardinality, s, t, vertices, edges =     load_file(path)
directed =is_directed(edges)

G = create_graph(vertices,edges,directed)

assert s == '0'
assert t == '15'
assert vertices_count == 16
assert edge_count == 21
assert cardinality == 5
assert G.nodes['10']['red'] == True
assert directed == True

