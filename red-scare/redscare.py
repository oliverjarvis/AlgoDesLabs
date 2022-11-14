from dataclasses import dataclass
import sys
from typing import List
import networkx as nx

class Parser:
    def __init__(self, filename):
        path = "data/" + filename
        self.vertices_count, self.edge_count, self.cardinality, self.s, self.t, self.vertices, self.edges = self.load_file(path)
        self.directed = self.is_directed(self.edges)
        self.G = self.create_graph(self.vertices, self.edges, self.directed)

    def load_file(self,path):
        with open(path, "r") as graph_file:
            vertices_count, edge_count, cardinality = tuple(map(int, next(graph_file).split()))
        
            s, t = tuple(next(graph_file).split())

            
            vertices = [next(graph_file).split() for _ in range(vertices_count)]
            edges = [next(graph_file).strip().split() for _ in range(edge_count)] # node connection node
            
            return vertices_count, edge_count, cardinality, s, t, vertices, edges

    def is_directed(self,edges) -> bool:
        # if the first edge is directed, the entire graph is directed
        if edges:
            return edges[0][1] == "->"
        return False

    def create_graph(self,vertices:List[str],edges, directed):
        G = nx.DiGraph()

        for node in vertices:
            if len(node) == 2:
                G.add_node(node[0], red=True)
            else:
                G.add_node(node[0], red=False)
        
        for src,_,dst in edges:
            G.add_edge(src,dst)

            if not directed:
                G.add_edge(dst,src)

        return G

class RedScare:
    def __init__(self, G, s, t):
        self.G = G
        self.s = s
        self.t = t
    
    def none(self) -> int:
        """No red nodes in the graph. Returns the path lenght from s to t and -1 if no path exists."""
        graph_data = list(G.nodes.data())

        for v, attr in graph_data:
            if attr['red']:
                G.remove_node(v)    

        try:
            path = nx.shortest_path_length(self.G, source=self.s, target=self.t)
        except nx.exception.NetworkXNoPath:
            path = -1
            
        return path
    
    def some(self):
        return
    
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

        Works on:
        ---------
        
        """
        
        def Opt(i, last_node):
            if memo[i] == None:
                # Check if i is red: Add 1 if it is
                if G.nodes[i]["red"]:
                    values = [Opt(j, i) for j in G.predecessors(i) if j is not last_node]
                    memo[i] = max([1 + x for x in values], default = 0)
                # If i is not red: Add 0
                else:
                    values = [Opt(j, i) for j in G.predecessors(i) if j is not last_node]
                    memo[i] = max(values, default = 0)
            return memo[i]
        
        memo = [None]*(G.number_of_nodes())
        # Base case: Opt(s) = 0 if not red, 1 if red
        if G.nodes[self.s]["red"]:
            memo[int(self.s)] = 1
        else:
            memo[int(self.s)] = 0
        last_node = None
        return Opt(self.t, last_node)

    def few(self):
        return
    
    def alternate(self):
        """Doc"""
        graph_data = dict(G.nodes.data())
        edges = list(G.edges)

        for u, v in edges:
            u_c:bool = graph_data[u]['red']
            v_c:bool = graph_data[v]['red']
            if u_c == v_c:
                G.remove_edge(u, v)
        
        return nx.has_path(self.G, self.s, self.t)

    def all(self):
        path_length:int = self.none()
        some =  self.some()
        flow:int = self.many()
        few= self.few()
        has_path: bool = self.alternate()
        return path_length, some, flow, few, has_path


if __name__ == '__main__':
    G = Parser('wall-p-1.txt').G
    redscare = RedScare(G, '7', '0')
    path_length, some, flow, few, has_path = redscare.all()
    print(path_length, some, flow, few, has_path)
    