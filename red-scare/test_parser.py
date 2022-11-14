from redscare import Parser

# test 1
path = "common-1-20.txt"
p = Parser(path)
assert p.s == 'start'
assert p.t == 'ender'
assert p.vertices_count == 20
assert p.edge_count == 0
assert p.cardinality == 9
assert p.G.nodes['purls']['red'] == True
assert p.directed == False

# test 2
path = "wall-p-1.txt"
p = Parser(path)
assert p.s == '7'
assert p.t == '0'
assert p.vertices_count == 8
assert p.edge_count == 8
assert p.cardinality == 1
assert p.G.nodes['3']['red'] == True
assert p.directed == False

# test 3
path = "ski-level3-1.txt"
p = Parser(path)
assert p.s == '0'
assert p.t == '15'
assert p.vertices_count == 16
assert p.edge_count == 21
assert p.cardinality == 5
assert p.G.nodes['10']['red'] == True
assert p.directed == True

