import sys
from dataclasses import dataclass
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
        tmp_G = self.G.copy()
        """No red nodes in the graph. Returns the path lenght from s to t and -1 if no path exists."""
        graph_data = list(tmp_G.nodes.data())

        for v, attr in graph_data:
            if attr["red"]:
                tmp_G.remove_node(v)

        try:
            path = nx.shortest_path_length(tmp_G, source=self.s, target=self.t)
        except nx.exception.NetworkXNoPath:
            path = -1

        return path

    def some(self):
        # First choose a random red node. Find a path from s to the red node. If no path exists, pick another red node. Find a path from that red node to t. If no path exists, pick another red node. Repeat until a path is found. I no path, return False.
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
        """
        if not nx.is_directed_acyclic_graph(self.G):
            return "NP-HARD"

        def Opt(i: int, last_node):
            if memo[i] is None:
                # Check if i is red: Add 1 if it is
                if G.nodes[id_to_node[i]]["red"]:
                    values = [
                        Opt(j, i)
                        for j in G.predecessors(id_to_node[i])
                        if j is not last_node
                    ]
                    memo[i] = max([1 + x for x in values], default=0)
                # If i is not red: Add 0
                else:
                    values = [
                        Opt(j, i)
                        for j in G.predecessors(id_to_node[i])
                        if j is not last_node
                    ]
                    memo[i] = max(values, default=0)
            return memo[i]

        id_to_node = dict(enumerate(G.nodes))
        node_to_id = {v: k for k, v in id_to_node.items()}
        memo = [None] * (G.number_of_nodes())
        # Base case: Opt(s) = 0 if not red, 1 if red
        if self.G.nodes[self.s]["red"]:
            memo[node_to_id[self.s]] = 1
        else:
            memo[node_to_id[self.s]] = 0
        last_node = None
        return Opt(self.t, last_node)

    def few(self):
        for e in self.G.edges:
            if self.G.nodes[e[1]]["red"]:
                self.G.edges[e]["weight"] = 1
            else:
                self.G.edges[e]["weight"] = 0

        sum = 0

        nodes = sp.shortest_path(self.G, self.s, self.t, weight="weight")

        # sum weights of paths in nodes
        for i in range(len(nodes) - 1):
            if i == 0:
                if self.G.nodes[nodes[i]]["red"]:
                    sum += 1
            sum += self.G.edges[nodes[i], nodes[i + 1]]["weight"]
        return sum

    def alternate(self):
        """Doc"""
        graph_data = dict(self.G.nodes.data())
        edges = list(self.G.edges)

        for u, v in edges:
            u_c: bool = graph_data[u]["red"]
            v_c: bool = graph_data[v]["red"]
            if u_c == v_c:
                self.G.remove_edge(u, v)

        return nx.has_path(self.G, self.s, self.t)

    def all(self):
        try:
            none: int = self.none()
        except:
            none = None
        try:
            some = self.some()
        except:
            some = None
        try:
            many: int = self.many()
        except:
            many = None
        try:
            few = self.few()
        except:
            few = None
        try:
            alternate: bool = self.alternate()
        except:
            alternate = None
        return none, some, many, few, alternate


if __name__ == "__main__":
    filename = "increase-n8-2.txt"
    G, s, t = Parser(filename).G, Parser(filename).s, Parser(filename).t
    redscare = RedScare(G, s, t)
    # redscare.many()
    path_length, some, flow, few, has_path = redscare.all()
    print(path_length, some, flow, few, has_path)
