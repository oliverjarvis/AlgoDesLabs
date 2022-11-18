import math
from typing import List

import networkx as nx
import networkx.algorithms.shortest_paths as sp


class Parser:
    def __init__(self, filename: str, data_folder="data/"):
        path = data_folder + filename
        (
            self.vertices_count,
            self.edge_count,
            self.cardinality,
            self.s,
            self.t,
            self.vertices,
            self.edges,
        ) = self.load_file(path)
        self.directed = self.is_directed(self.edges)
        self.G = self.create_graph(self.vertices, self.edges, self.directed)

    def load_file(self, path):
        with open(path, "r") as graph_file:
            vertices_count, edge_count, cardinality = tuple(
                map(int, next(graph_file).split())
            )

            s, t = tuple(next(graph_file).split())

            vertices = [next(graph_file).split() for _ in range(vertices_count)]
            edges = [
                next(graph_file).strip().split() for _ in range(edge_count)
            ]  # node connection node

            return vertices_count, edge_count, cardinality, s, t, vertices, edges

    def is_directed(self, edges) -> bool:
        # if the first edge is directed, the entire graph is directed
        if edges:
            return edges[0][1] == "->"
        return False

    def create_graph(self, vertices: List[str], edges, directed):
        G = nx.DiGraph()

        for node in vertices:
            if len(node) == 2:
                G.add_node(node[0], red=True)
            else:
                G.add_node(node[0], red=False)

        for src, _, dst in edges:
            G.add_edge(src, dst)

            if not directed:
                G.add_edge(dst, src)

        return G


class RedScare:
    def __init__(self, G, s, t):
        self.G = G
        self.s = s
        self.t = t

    def none(self) -> int:
        """No red nodes in the graph. Returns the path lenght from s to t and -1 if no path exists.
        Removal of R in V = V, find path = V+E.
        Actual Time: V+((V-R)+(E-E_in/out_R))
        """
        tmp_G = self.G.copy()

        for node in self.G.nodes:
            if self.G.nodes[node]["red"]:
                tmp_G.remove_node(node)

        try:
            path = nx.shortest_path_length(tmp_G, source=self.s, target=self.t)
        except nx.exception.NetworkXNoPath:
            path = -1
        except nx.exception.NodeNotFound:  # node removed since it's red
            path = -1

        return path

    def some(self) -> bool:
        """
        First choose a random red node. Find a path from s to the red node.
        If no path exists, pick another red node.
        Find a path from that red node to t.
        If no path exists, pick another red node. Repeat until a path is found.
        I no path, return False.
        Time complexity --> 2V*(V+E) --> bfs på alle røde 2 gange,
        og worst case er alle røde så V. BIG O(V^2+E).
        """
        graph_data = dict(self.G.nodes.data())
        red_nodes = [node for node, attr in graph_data.items() if attr["red"]]
        for red_node in red_nodes:  #
            tmp_G = self.G.copy()
            try:
                path = nx.shortest_path(tmp_G, self.s, red_node)
            except nx.NetworkXNoPath:
                path = False
            if path:
                # remove the elements in the path from s to red_node
                for node in path:
                    if node != red_node:
                        # could potentially stop if node == self.t
                        tmp_G.remove_node(node)

                # check if there is a path from red_node to t
                try:
                    has_path = nx.has_path(tmp_G, red_node, self.t)
                except nx.NodeNotFound:
                    has_path = False

                if has_path:
                    return True
        return False

    def many(self) -> int:
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
        ---------------------
        Dynamic part -> O(V)
        """
        if not nx.is_directed_acyclic_graph(self.G):
            return "NP-HARD"

        def Opt(i: str) -> int:
            i = node_to_id[i]
            if memo[i] is None:
                pre = [x for x in self.G.predecessors(id_to_node[i])]
                if pre:
                    # Generate values for all predecessors
                    values = [Opt(j) for j in pre]
                    # Check if i is red: Add 1 if it is
                    if self.G.nodes[id_to_node[i]]["red"]:
                        memo[i] = max([1 + x for x in values], default=0)
                    # If i is not red: Add 0
                    else:
                        memo[i] = max(values, default=0)
                else:
                    memo[i] = float("-inf")
                    return memo[i]
            return memo[i]

        id_to_node = dict(enumerate(self.G.nodes))
        node_to_id = {v: k for k, v in id_to_node.items()}

        memo = [None] * (self.G.number_of_nodes())
        # Base case: Opt(s) = 0 if not red, 1 if red
        if self.G.nodes[self.s]["red"]:
            memo[node_to_id[self.s]] = 1
        else:
            memo[node_to_id[self.s]] = 0

        results = Opt(self.t)
        if results == float("-inf"):
            return -1
        else:
            return results

    def few(self) -> int:
        """
        Time complexity: Augmentation -> E, Path finding -> V+E.
        O(V+E)
        """
        for e in self.G.edges:
            if self.G.nodes[e[1]]["red"]:
                self.G.edges[e]["weight"] = 1
            else:
                self.G.edges[e]["weight"] = 0

        try:
            sum = sp.shortest_path_length(self.G, self.s, self.t, weight="weight")
            if self.G.nodes[self.s]["red"]:
                return sum + 1
            else:
                return sum
        except nx.NetworkXNoPath:
            return -1

    def alternate(self):
        """
        Time complexity: Augmentation -> E, Path finding -> V+E.
        O(V+E)
        """
        graph_data = dict(self.G.nodes.data())
        edges = list(self.G.edges)

        for u, v in edges:
            u_c: bool = graph_data[u]["red"]
            v_c: bool = graph_data[v]["red"]
            if u_c == v_c:
                self.G.remove_edge(u, v)

        return nx.has_path(self.G, self.s, self.t)

    def all(self):
        print("none")
        none: int = self.none()
        print("some")
        some: bool = self.some()
        print("many")
        many: int = self.many()
        print("few")
        few: int = self.few()
        print("alternate")
        alternate: bool = self.alternate()

        return none, some, many, few, alternate


if __name__ == "__main__":
    filename = "ski-illustration.txt"
    G, s, t = Parser(filename).G, Parser(filename).s, Parser(filename).t
    redscare = RedScare(G, s, t)
    print(redscare.none())
    # path_length, some, flow, few, has_path = redscare.all()
    # print(path_length, some, flow, few, has_path)
