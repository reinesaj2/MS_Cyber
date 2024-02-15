import itertools
import os
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.graph = dict()

    def add_edge(self, u, v):
        """ Add edge between vertices u and v. """
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append(v)
        self.graph[v].append(u)

    def is_clique(self, vertices):
        """ Check if the given set of vertices forms a clique. """
        for pair in itertools.combinations(vertices, 2):
            if pair[1] not in self.graph[pair[0]]:
                return False
        return True

    def find_cliques(self, N):
        """ Find all cliques of size N in the graph. """
        cliques = []
        for vertices in itertools.combinations(self.graph.keys(), N):
            if self.is_clique(vertices):
                cliques.append(vertices)
        return cliques
    
    def compliance_report(self, N, expected_cliques):
        """ Generate a compliance report for cliques of size N. """
        actual_cliques = self.find_cliques(N)
        report = {
            'test_passed': all(clique in actual_cliques for clique in expected_cliques),
            'expected_cliques': expected_cliques,
            'actual_cliques': actual_cliques,
            'correct_cliques': all(clique in actual_cliques for clique in expected_cliques)
        }
        return report
    
    def visualize_graph(self, cliques=None, filename='graph_plot.png'):
        """ Visualize the graph with optional highlighted cliques, add a legend, and save the plot. """
        G = nx.Graph()
        
        # Add nodes and edges to the NetworkX graph
        for node in self.graph:
            G.add_node(node)
        for node, neighbors in self.graph.items():
            for neighbor in neighbors:
                G.add_edge(node, neighbor)

        # Default node color
        color_map = ['blue' for node in G]

        # Prepare a legend
        legend_labels = {}

        # Highlight cliques with different colors
        if cliques:
            colors = ['red', 'green', 'yellow', 'cyan', 'magenta']
            for i, clique in enumerate(cliques):
                color = colors[i % len(colors)]
                legend_labels[f'Clique {i+1}'] = plt.Line2D([0], [0], marker='o', color='w', label=f'Clique {i+1}',
                                                            markersize=10, markerfacecolor=color)
                for node in clique:
                    color_map[node] = color

        nx.draw(G, node_color=color_map, with_labels=True)

        # Add the legend to the plot
        plt.legend(handles=legend_labels.values())

        # Ensure 'plots' directory exists
        plots_dir = 'plots'
        os.makedirs(plots_dir, exist_ok=True)
        
        # Save the plot
        plt.savefig(os.path.join(plots_dir, filename))
        plt.show()  
        plt.close()  


    
    

def create_graphs():
    """Create two specific graph structures for demonstration."""
    # Graph 1: 10 vertices with a fully interconnected subgraph of 5 vertices
    graph1 = Graph()
    for i in range(5):
        for j in range(i + 1, 5):
            graph1.add_edge(i, j)
    for i in range(5, 10):
        graph1.add_edge(i, min(i + 1, 9))

    # Graph 2: 10 vertices with overlapping cliques
    graph2 = Graph()
    for c in range(0, 9, 3):
        for a in range(c, c + 4):
            for b in range(a + 1, c + 4):
                graph2.add_edge(a, b)

    return graph1, graph2

def main():
    graph1, graph2 = create_graphs()

    # Finding, printing, and visualizing cliques for both graphs
    for size in range(3, 6):
        cliques_graph1 = graph1.find_cliques(size)
        cliques_graph2 = graph2.find_cliques(size)

        print(f"\n--- Clique of size {size} in Graph 1 ---\n{cliques_graph1}")
        graph1.visualize_graph(cliques=cliques_graph1, filename=f'graph1_cliques_size_{size}.png')

        print(f"\n--- Clique of size {size} in Graph 2 ---\n{cliques_graph2}")
        graph2.visualize_graph(cliques=cliques_graph2, filename=f'graph2_cliques_size_{size}.png')

    # Compliance Reports
    expected_cliques_graph1 = [(0, 1, 2), (0, 1, 3)]  #  expected cliques for graph1
    expected_cliques_graph2 = [(0, 1, 2, 3), (3, 4, 5, 6)]  #  expected cliques for graph2

    report1 = graph1.compliance_report(3, expected_cliques_graph1)
    report2 = graph2.compliance_report(4, expected_cliques_graph2)

    print("\n--- Compliance Report for Graph 1 ---")
    for key, value in report1.items():
        print(f"{key.capitalize()}: {value}")

    print("\n--- Compliance Report for Graph 2 ---")
    for key, value in report2.items():
        print(f"{key.capitalize()}: {value}")

if __name__ == "__main__":
    main()