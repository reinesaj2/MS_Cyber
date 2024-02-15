import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyArrowPatch, PathPatch
from matplotlib.path import Path
import matplotlib.patches as mpatches

# Define the set A and relation R
A = {0, 1, 2, 3}
R = {(1, 2), (2, 1), (1, 3), (3, 1)}

# Create a directed graph from the relation R
G = nx.DiGraph()
G.add_nodes_from(A)
G.add_edges_from(R)

# Custom function to draw curved edges with arrows
def draw_curved_edges(G, pos, ax):
    for (u, v) in G.edges():
        if (v, u) in G.edges() and u < v:
            # Draw a curved line for bidirectional edges
            rad = 0.2
            style = "arc3,rad={}".format(rad)
            arrow = FancyArrowPatch(pos[u], pos[v], connectionstyle=style, arrowstyle='-|>', color='black',
                                    mutation_scale=20, lw=1)
            ax.add_patch(arrow)
            # Reverse direction
            arrow = FancyArrowPatch(pos[v], pos[u], connectionstyle=style, arrowstyle='-|>', color='black',
                                    mutation_scale=20, lw=1, linestyle='dotted')
            ax.add_patch(arrow)
        elif not (v, u) in G.edges():
            # Straight line otherwise
            arrow = FancyArrowPatch(pos[u], pos[v], arrowstyle='-|>', color='black', mutation_scale=20, lw=1)
            ax.add_patch(arrow)

# Draw the graph
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G)  # or any other layout you prefer
ax = plt.gca()

# Draw nodes and labels
nx.draw_networkx_nodes(G, pos, node_size=150, node_color="lightblue", ax=ax)
nx.draw_networkx_labels(G, pos, font_size=15, ax=ax)

# Draw edges
draw_curved_edges(G, pos, ax)

plt.title("Directed Graph of the Relation R")
plt.axis('off')  # Turn off the axis
plt.show()
