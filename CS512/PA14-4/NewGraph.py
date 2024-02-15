import os
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

class NewGraph(object):
    def __init__(self, directed=False):
        """
        Initialize an empty NewGraph, with an option to set it as directed or undirected.
        """
        self._directed = directed
        self._adjacency_list = {}

    def createNewGraph(self, vertices, edges):
        """
        Create a NewGraph using the provided vertices and edges.
        """
        self._adjacency_list = {v: set() for v in vertices}
        for edge in edges:
            self.addEdge(*edge)

    def draw(self, filename=None):
        """
        Draw the graph using networkx and matplotlib, and save the plot in the 'plots' directory.
        """
        # Create 'plots' directory if it doesn't exist
        plots_dir = os.path.join(os.path.dirname(__file__), 'plots')
        os.makedirs(plots_dir, exist_ok=True)

        # Generate a unique filename if not provided
        if filename is None:
            filename = f"NewGraph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

        G = nx.DiGraph() if self._directed else nx.Graph()
        for vertex, edges in self._adjacency_list.items():
            for edge in edges:
                G.add_edge(vertex, edge)

        nx.draw(G, with_labels=True)

        # Save the plot
        plt.savefig(os.path.join(plots_dir, filename))
        plt.show()

    def addEdge(self, u, v):
        """
        Add an edge to the NewGraph. In directed NewGraphs, edge is from u to v.
        """
        self._adjacency_list[u].add(v)
        if not self._directed:
            self._adjacency_list[v].add(u)

    def print(self):
        """
        Print the NewGraph. Use different arrow symbols for directed and undirected NewGraphs.
        """
        arrow = '->' if self._directed else '<->'
        for vertex, edges in self._adjacency_list.items():
            for edge in edges:
                print(f"{vertex} {arrow} {edge}")

    def depthFirst(self, start_vertex):
        """
        Perform a depth-first traversal starting from the given vertex.
        """
        visited = set()
        path = []

        def dfs(vertex):
            if vertex not in visited:
                visited.add(vertex)
                path.append(vertex)
                for neighbour in self._adjacency_list[vertex]:
                    dfs(neighbour)

        dfs(start_vertex)
        return path

# Vertices and edges for the NewGraph
vertices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
edges = [('A', 'G'), ('A', 'I'), ('C', 'F'), ('D', 'A'), ('D', 'I'), ('H', 'D'), ('H', 'E'), ('H', 'F'), ('H', 'G'), ('I', 'H'), ('J', 'C'), ('J', 'H')]

# Creating undirected NewGraph
undirected_NewGraph = NewGraph()
undirected_NewGraph.createNewGraph(vertices, edges)
print("Undirected NewGraph:")
undirected_NewGraph.print()
print("\nDepth-First Traversal from J:", undirected_NewGraph.depthFirst('J'))

# Creating directed NewGraph
directed_NewGraph = NewGraph(directed=True)
directed_NewGraph.createNewGraph(vertices, edges)
print("\nDirected NewGraph:")
directed_NewGraph.print()
print("\nDepth-First Traversal from J:", directed_NewGraph.depthFirst('J'))

undirected_NewGraph.draw("undirected_graph.png")
directed_NewGraph.draw("directed_graph.png")
