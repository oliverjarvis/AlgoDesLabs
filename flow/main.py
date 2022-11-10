from dataclasses import dataclass, field
from typing import List, Tuple
import numpy as np


@dataclass
class DiGraph:
    N: int
    nodes: List[str]  # only used for debugging
    edges: List[Tuple[int, int, int]]
    adjacency: np.ndarray = field(init=False)

    def __post_init__(self):
        self.adjacency = np.zeros(shape=(self.N, self.N), dtype=int)
        for src, tar, weight in self.edges:
            # both cases because they are considered undirected
            self.adjacency[src, tar] = weight
            self.adjacency[tar, src] = weight
        self.original = self.adjacency.copy()  # used in find_min_cut


class BFS:
    def __init__(self, G) -> None:
        self.G: DiGraph = G
        self.parent: List[int] = field(init=False)

    def search(self, source, sink) -> bool:
        """Find path from source to sink (if any). O(|V|^2) because of adjacency matrix"""
        # parent indicate the parent index of a node index
        self.parent = [-1] * self.G.N
        visited = [False] * self.G.N

        queue: List[int] = [source]
        visited[source] = True
        self.parent[source] = 0  # or None or similar

        while queue:
            current_node = queue.pop(0)
            current_node_name = self.G.nodes[current_node]  # debug
            adjacent_nodes = self.G.adjacency[current_node]

            for adjacent_node, edge_capacity in enumerate(adjacent_nodes):
                adjacent_node_name = self.G.nodes[adjacent_node]  # debug
                # If there is any edge capacity to an unvisited node
                if not visited[adjacent_node] and edge_capacity != 0:

                    if adjacent_node == sink:  # if sink is reached
                        self.parent[adjacent_node] = current_node
                        return True

                    self.parent[adjacent_node] = current_node
                    visited[adjacent_node] = True
                    queue.append(adjacent_node)

        return False


class FordFulkerson:
    """Ford Fulkerson algorithm implemented acordingly to page 340-344"""

    def __init__(self, G: DiGraph, N: int) -> None:
        # utilities
        self.G: DiGraph = G
        self.path_finder: BFS = BFS(self.G)

        # hardcoded source and sink
        self.source = 0
        self.sink = N - 1

        # class function containers
        self.flow_pushed: int = 0
        self.min_cut_flow: int = 0
        self.min_cut: List[Tuple[int, int, int]] = []

    def push_max_flow(self, source: int, sink: int) -> None:
        """Ford-Fulkerson: Computes the maximum flow. Defined on page 344"""
        while self.path_finder.search(source, sink):
            self._augment()

    def find_min_cut(self) -> None:
        """Find the cut when BFS doesn't find any s-t paths"""
        has_path: bool = self.path_finder.search(self.source, self.sink)
        assert not has_path

        not_reached, reached = set(), set()
        for idx, parent_idx in enumerate(self.path_finder.parent):
            if parent_idx == -1:  # not reached by bfs
                not_reached.add(idx)
            else:  # reached by bfs
                reached.add(idx)

        for reached_node in reached:
            for unreached_node in not_reached:
                edge_cap = self.G.original[unreached_node, reached_node]
                if edge_cap > 0:
                    self.min_cut.append((reached_node, unreached_node, edge_cap))
                    self.min_cut_flow += edge_cap

    def _augment(self) -> None:
        """Update the adjacency and update pushed flow. Defined on page 342-343"""
        bottleneck = self._get_bottleneck()
        parent = -1
        node_idx = self.sink

        while parent != self.source:

            parent = self.path_finder.parent[parent]
            capacity = self.G.adjacency[node_idx, parent]

            if capacity != -1:
                # Remove flow from capacity
                self.G.adjacency[parent, node_idx] -= bottleneck
                # Add flow to residual capacity
                self.G.adjacency[node_idx, parent] += bottleneck

            node_idx = parent

        self.flow_pushed += bottleneck

    def _get_bottleneck(self) -> int:
        """Definition from page 342: We define bottleneck(P,f) to be the minimum residual capacity of any edge on P, with repect to the flow f."""
        residual_capacities = set()
        source_idx, target_idx = self.sink, self.sink

        while target_idx != 0:

            target_idx = self.path_finder.parent[source_idx]
            residual_capacity = self.G.adjacency[target_idx, source_idx]
            if residual_capacity not in (-1, 0):
                residual_capacities.add(residual_capacity)

            source_idx = target_idx

        return min(residual_capacities)


if __name__ == "__main__":

    def read_rail(path: str):
        """a bit hacky yes"""
        with open(path, "r", encoding="utf-8") as infile:
            lines = [line.strip() for line in infile]

        N = int(lines[0])
        nodes = lines[1 : N + 1]

        M = int(lines[N + 1])
        edges = [tuple(map(int, line.split())) for line in lines[N + 2 :]]

        return N, nodes, M, edges

    N, nodes, m, edges = read_rail("data/rail.txt")

    src, sink_idx = 0, N - 1
    assert nodes[src] == "ORIGINS" and nodes[sink_idx] == "DESTINATIONS"

    # part one
    G = DiGraph(N, nodes, edges)
    FF = FordFulkerson(G, N)
    FF.push_max_flow(src, sink_idx)
    FF.find_min_cut()

    # print(f"{FF.flow_pushed=}")
    # print(f"{FF.min_cut_flow=}")
    for src, tar, weight in FF.min_cut:
        print(src, tar, weight)

    # # part two
    # print("PART TWO")
    # # modify edges between 4W<->48 and 4W<->49 to capacity 10
    # for i, edge in enumerate(edges):
    #     src, tar, weight = edge
    #     if nodes[src] == "4W":
    #         if nodes[tar] in ("49","48"):
    #             if nodes[tar] == "49":
    #                 edges[i] = (src, tar, 10)
    #                 print(nodes[src],nodes[tar],10)
    #             else:
    #                 print(nodes[src],nodes[tar],weight)

    # src, sink_idx = 0, N - 1
    # G = DiGraph(N, nodes, edges)
    # FF = FordFulkerson(G, N)
    # FF.push_max_flow(src, sink_idx)
    # FF.find_min_cut()

    # print(f"{FF.flow_pushed=}")
    # print(f"{FF.min_cut_flow=}")
    # for src, tar, weight in FF.min_cut:
    #     print(src, tar, weight)
