import networkx as nx
from redscare import Parser, RedScare


# The many problem
def many(G, s, t):
    """
    Parameters
    ----------
    G : Graph
        Graph to be searched.

    Returns
    -------
    int
        Maximum number of red nodes in a path from s to t in G.

    Flow of the algorithm
    ---------------------
    1. Run dynamic programming algorithm:
        Opt(i) = max(1 + Opt(j)) for all j in G.predecessors(i)
    """
    if not nx.is_directed_acyclic_graph(G):
        return "NP-HARD"

    def Opt(i: int):
        i = node_to_id[i]
        if memo[i] is None:
            values = [Opt(j) for j in G.predecessors(id_to_node[i])]
            # Check if i is red: Add 1 if it is
            if G.nodes[id_to_node[i]]["red"]:
                memo[i] = max([1 + x for x in values], default=0)
            # If i is not red: Add 0
            else:
                memo[i] = max(values, default=0)
        return memo[i]

    id_to_node = dict(enumerate(G.nodes))
    node_to_id = {v: k for k, v in id_to_node.items()}

    memo = [None] * (G.number_of_nodes())

    # Base case: Opt(s) = 0 if not red, 1 if red
    if G.nodes[s]["red"]:
        memo[node_to_id[s]] = 1
    else:
        memo[node_to_id[s]] = 0

    return Opt(t)


filename = "increase-n8-2.txt"
G, s, t = Parser(filename).G, Parser(filename).s, Parser(filename).t

print(G)


sol = many(G, s, t)
print(sol)
