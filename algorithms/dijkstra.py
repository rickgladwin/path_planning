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
import typing
from typing import TypeVar, Hashable, TypeAlias

import networkx as nx
from networkx.classes import Graph
import matplotlib.pyplot as plt
from networkx.classes.reportviews import NodeView

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

def draw_graph():
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

print(f'{G=}')
print(f'{G.nodes=}')
print(f'{G.nodes["A"]=}')
graph_adjacency = G.adjacency()
for element in graph_adjacency:
    print(f'adjacency element: {element}')
print(f'{G.adjacency()=}')

# types

# Node = TypeAlias("Node", bound=Hashable)

class Traverser:
    # NOTE: in the visitor pattern, the original data is kept minimal
    #  and immutable (immutable by the visitor anyway), and an internal
    #  representation of the data and search results is built that belongs
    #  to the visitor.
    graph: Graph # original (immutable) graph data
    node_info: dict # internal data about the search results
    expanded: list  # nodes in the search graph that have been explored,
                    # and their adjacent nodes generated and added to the frontier
    frontier: list # nodes in the search graph that have been generated but not expanded (visited)
    # NOTE: (expanded nodes) ∪ (frontier nodes) == reached nodes
    goal_node: typing.Any

    def __init__(self, graph: Graph):
        self.goal_node = None
        self.graph = graph
        self.node_info = dict(dict())
        self.expanded = []
        self.frontier = []
        #populate the node table using the graph
        for node in graph.nodes:
            self.node_info[node] = {node: {"shortest_distance": float('inf'), "previous_node": None}}

        print(f'{self.node_info=}')

    def start_visit(self, start_node, goal_node):
        print(f'starting at: {start_node}')
        self.node_info[start_node]["shortest_distance"] = 0
        self.goal_node = goal_node
        self.visit(start_node, None)

    # TODO: build the evaluation and updating functions
    def visit(self, node, visit_from):
        # on visiting a node:
        #  - update the node's info in node_info
        #  - test the node against the goal
        #  - for each adjacent node:
        #    - if adjacent node not in frontier or expanded:
        #      - generate adjacent node
        #  - add the node to expanded
        #  - for each node on the frontier, in order of lowest cost,
        #    - pop the node off the frontier
        #    - visit the node
        # self.node_info[node]["previous_node"] = visit_from
        if node == self.goal_node:
            self.finish(True, self.goal_node)

        # for reachable in self.graph.nodes:
            # if reachable not in self.expanded:
        self.expanded.append(node)

    def generate(self, node, generate_from, cost: int):
        # update the node's info in node_info
        # push the node to the frontier
        current_node_info: dict = self.node_info[node]
        current_node_info["previous_node"] = generate_from
        current_node_info["shortest_distance"] = current_node_info["shortest_distance"] + cost
        self.frontier.append(node)

    def finish(self, success: bool, last_node):
        if success:
            print(f'success!')
            print(f'reached goal node: {last_node}')
            print(f'{self.node_info=}')
        else:
            print(f'finished without success.')
            print(f'last node reached: {last_node}')
            print(f'{self.node_info=}')

if __name__ == "__main__":
    dijkstra_traverser = Traverser(G)
    dijkstra_traverser.start_visit(G.nodes["A"], tuple(G.nodes["C"]))
    print("done.")
