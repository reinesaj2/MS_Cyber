import os
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

class WarshallsGraph(object):
    def __init__(self, directed=False):
        """
        Initialize an empty WarshallsGraph, with an option to set it as directed or undirected.
        """
        self._directed = directed
        self._adjacency_list = {}

    def createWarshallsGraph(self, vertices, edges):
        """
        Create a WarshallsGraph using the provided vertices and edges.
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
            filename = f"WarshallsGraph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

        G = nx.DiGraph() if self._directed else nx.MultiDiGraph()
        for vertex, edges in self._adjacency_list.items():
            for edge in edges:
                G.add_edge(vertex, edge)
                if not self._directed:
                    G.add_edge(edge, vertex)  # Add edge in the opposite direction for undirected graphs

        pos = nx.shell_layout(G)

        # Draw nodes and edges with customizations
        nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue')
        nx.draw_networkx_edges(G, pos, edge_color='gray', width=2, arrowsize=20)
        nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')

        # Add graph title and other customizations
        plt.title('Graph Visualization')
        plt.axis('off')  # Turn off axis

        # Save the plot with high quality
        plt.savefig(os.path.join(plots_dir, filename), format='PNG', dpi=300)

        plt.show()
        plt.close()
        
    def addEdge(self, u, v):
        """
        Add an edge to the WarshallsGraph. In directed WarshallsGraphs, edge is from u to v.
        """
        self._adjacency_list[u].add(v)
        if not self._directed:
            self._adjacency_list[v].add(u)

    def print(self):
        """
        Print the WarshallsGraph. Use different arrow symbols for directed and undirected WarshallsGraphs.
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
    
    def connectivityMatrix(self):
        """
        Compute the connectivity matrix using Warshall's algorithm and return a matrix of 1s and 0s.
        """
        # Convert node labels to indices
        node_indices = {node: idx for idx, node in enumerate(self._adjacency_list)}
        n = len(node_indices)

        # Initialize the connectivity matrix with 0s
        matrix = [[0 for _ in range(n)] for _ in range(n)]

        # Fill the matrix based on the adjacency list
        for node, edges in self._adjacency_list.items():
            for edge in edges:
                matrix[node_indices[node]][node_indices[edge]] = 1

        # Apply Warshall's algorithm to update the matrix
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    matrix[i][j] = matrix[i][j] or (matrix[i][k] and matrix[k][j])

        return matrix
    
    def hasCycles(self):
        """
        Check for the presence of cycles in the graph.
        """
        conn_mat = self.connectivityMatrix()
        n = len(conn_mat)

        # Check if any vertex has a path to itself
        for i in range(n):
            if conn_mat[i][i] == 1:
                return True
        return False
        
    def printComplianceReport(self):
        """
        Print a compliance report for the NewGraph.
        """
        report = f"\nCompliance Report for {'Directed' if self._directed else 'Undirected'} NewGraph\n"
        report += "----------------------------------------------------\n"
        report += f"Number of Vertices: {len(self._adjacency_list)}\n"
        report += f"Number of Edges: {sum(len(edges) for edges in self._adjacency_list.values()) // (2 if not self._directed else 1)}\n"
        report += f"Presence of Cycles: {'Yes' if self.hasCycles() else 'No'}\n"
        report += "Connectivity Matrix:\n"
        
        conn_matrix = self.connectivityMatrix()
        for i, row in enumerate(conn_matrix):
            report += f"{list(self._adjacency_list)[i]}: {' '.join(map(str, row))}\n"

        print(report)
        
        
        
# Create a WarshallsGraph instance
warshalls_graph = WarshallsGraph(directed=True)  # Assuming it's a directed graph

# Vertices and edges for the WarshallsGraph
vertices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
edges = [('A', 'G'), ('A', 'I'), ('C', 'F'), ('D', 'A'), ('D', 'I'), ('H', 'D'), ('H', 'E'), ('H', 'F'), ('H', 'G'), ('I', 'H'), ('J', 'C'), ('J', 'H')]

# Create the graph
warshalls_graph.createWarshallsGraph(vertices, edges)

# Compute and print the connectivity matrix
connectivity_matrix = warshalls_graph.connectivityMatrix()

# Creating undirected WarshallsGraph
undirected_WarshallsGraph = WarshallsGraph()
undirected_WarshallsGraph.createWarshallsGraph(vertices, edges)
print("\nUndirected WarshallsGraph:")
undirected_WarshallsGraph.print()
print("\nDepth-First Traversal from J:", undirected_WarshallsGraph.depthFirst('J'))

# Creating directed WarshallsGraph
directed_WarshallsGraph = WarshallsGraph(directed=True)
directed_WarshallsGraph.createWarshallsGraph(vertices, edges)
print("\nDirected WarshallsGraph:")
directed_WarshallsGraph.print()
print("\nDepth-First Traversal from J:", directed_WarshallsGraph.depthFirst('J'))

undirected_WarshallsGraph.draw("undirected_graph.png")
directed_WarshallsGraph.draw("directed_graph.png")

# Test connectivity and cycles for undirected graph
#print("\nConnectivity Matrix for Undirected Graph:")
#print(undirected_WarshallsGraph.connectivityMatrix())
print("\nDoes the Undirected Graph have cycles? ", undirected_WarshallsGraph.hasCycles())

# Test connectivity and cycles for directed graph
#print("\nConnectivity Matrix for Directed Graph:")
#print(directed_WarshallsGraph.connectivityMatrix())
print("\nDoes the Directed Graph have cycles? ", directed_WarshallsGraph.hasCycles())

undirected_WarshallsGraph.printComplianceReport()
directed_WarshallsGraph.printComplianceReport()