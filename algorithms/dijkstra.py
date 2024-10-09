"""
Use Dijkstra's algorithm to calculate the most efficient path from A to C.

        ┌───┐     6    ┌───┐
  ┌─────┤ B ├──────────┤ E ├───────┐
 2│     └─┬─┘          └┬┬─┘       │9
  │       │             ││         │
┌─┴─┐     │      ┌──────┘│      ┌──┴┐
│ A │    5│      │3      │1     │ C │
└─┬─┘     │      │       │      └─┬─┘
  │       │┌─────┘       │        │
 8│     ┌─┴┴┐          ┌─┴─┐      │3
  └─────┤ D ├──────────┤ F ├──────┘
        └───┘    2     └───┘

https://monosketch.io/
"""

import networkx as nx
from networkx.classes import Graph
import matplotlib.pyplot as plt

# build the graph
G: Graph = nx.Graph()
G.add_nodes_from("ABCDEF")
G.add_weighted_edges_from([
    ("A", "B", 2),
    ("A", "D", 8),
    ("B", "D", 5),
    ("D", "E", 3),
    ("B", "E", 6),
    ("D", "F", 2),
    ("F", "C", 3),
    ("E", "C", 9),
    ("E", "F", 1),
])

# draw the weighted graph
# See https://networkx.org/documentation/latest/auto_examples/drawing/plot_weighted_graph.html

# nx.draw(G, with_labels=True, font_weight="bold")
# nx.draw_networkx(G, with_labels=True, font_weight="bold")
# nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G))

# G = nx.petersen_graph()
# subax1 = plt.subplot(121)
# nx.draw(G, with_labels=True, font_weight='bold')
# subax2 = plt.subplot(122)
# nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility
# pos = nx.circular_layout(G)
pos = {
    "A": (1,1),
    "B": (2,2),
    "D": (2,0),
    "E": (4,2),
    "F": (4,0),
    "C": (5,1),
}

# nodes
nx.draw_networkx_nodes(G, pos, node_size=700)

# edges
nx.draw_networkx_edges(G, pos, width=6)
# nx.draw_networkx_edges(
#     G, pos, width=6, alpha=0.5, edge_color="b", style="dashed"
# )

# node labels
nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
# edge weight labels
all_edge_weights = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, font_size=20, edge_labels=all_edge_weights)

ax = plt.gca()
ax.margins(0.08)
plt.axis("off")
plt.tight_layout()

plt.show()
