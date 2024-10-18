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
# enable late evaluation of types (allows us to use type declarations
# in classes that are the type of the class itself)
from __future__ import annotations

from typing import Hashable

import matplotlib.pyplot as plt
import networkx as nx
from networkx.classes import Graph
from networkx.classes.reportviews import EdgeDataView

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

    # pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility
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


class StateNode:
    """
    A Node in the underlying state data from the problem.
    For any problem for which we can draw a state diagram, there will be equivalency
    between the graph of StateNodes and the graph of SearchNodes, but the properties
    on the nodes and the configuration of the edges may differ.

    In this example, StateNodes will correspond directly to the nodes in the networkx graph for
    the problem.
    """
    state: Hashable
    # edges type is a concretion of Graph.adj[_Node] type dict[Hashable | Any, dict[str, Any]]
    # that lets us use string node identifiers and { 'weight': int } dictionary entries for edge properties
    edges: EdgeDataView

    def __init__(self, state, edges):
        self.state = state
        self.edges = edges

class SearchNode:
    """
    A Node in the search graph, generated while solving the problem.
    Each SearchNode may correspond to each StateNode in the underlying data 1-to-1,
    especially if the underlying problem can be formulated using a state diagram.
    A SearchNode may have a similar relationship to the search graph as its corresponding
    StateNode has to the data graph but with different properties (relevant to the
    search), and the structure of the search graph may not match the state graph.
    """
    def __init__(self, state_node: StateNode, parent_node: SearchNode | None, path_cost: int | float):
        self.state: StateNode = state_node
        self.parent: SearchNode = parent_node
        # Note: for Dijkstra's, we're letting the information about the actions belong to the
        #  expansion function, since it's straightforward (expand from a parent node, add the
        #  parent node's path cost to the edge cost from the parent to the current node to get
        #  the current node's path cost)
        # self.action = action
        self.path_cost = path_cost


class Frontier:
    """
    The Frontier class for best-first-search.
    dijkstra.Frontier uses smallest path size for evaluation
    and (in this example), a set (which is unordered) for storing nodes.
    NOTE: in the networkx package, the type of a Node can be any hashable
    type, and it's more messy than it's worth (and at the cost of polymorphism)
    to restrict the type of the node itself in the classes in this module for
    the *state* nodes (the nodes in the underlying data from the problem).
    For state nodes, It's enough to declare the types of the Graphs (etc.)
    themselves, and let the requirements from the networkx package trigger
    warnings while using those types.
    For *search* nodes, which may contain additional data, and which represent
    parts of the search graph (which may not even be the same shape as the
    underlying data graph), we can declare any type that suits us, including
    custom types.
    """
    nodes: set[SearchNode]

    def __init__(self):
        self.nodes = set()

    def is_empty(self):
        return not self.nodes

    def pop(self) -> SearchNode | None:
        # return the node in the frontier with the best score based on the evaluation function
        # and remove it from the set.
        top_node = self.top()
        self.nodes.remove(top_node)
        return top_node

    def top(self) -> SearchNode | None:
        # return the node in the frontier with the best score (lowest cost, in the case of Dijkstra's
        # algorithm) based on the evaluation function, but do not remove it from the set.
        best_node = next(iter(self.nodes))
        for node in self.nodes:
            if self.evaluate(node) < best_node.path_cost:
                best_node = node
        return best_node

    def add(self, node: SearchNode) -> None:
        # add the node to the set (unordered, in this example)
        self.nodes.add(node)
        print(f"Frontier nodes:\n{self}")

    def evaluate(self, node: SearchNode) -> int:
        # The evaluation function f(n).
        # return a score for the node based on the criteria defined by the problem or algorithm type
        return node.path_cost

    def __str__(self):
        output = ""
        for node in self.nodes:
            output += f"{node.state.state}, cost: {node.path_cost}\n"
        return output


class Traverser:
    # NOTE: in the visitor pattern, the original data is kept minimal
    #  and immutable (immutable by the visitor anyway), and an internal
    #  representation of the data and search results is built that belongs
    #  to the visitor. The way these search-based solutions work essentially
    #  implements the visitor pattern by default, and runs with it by constructing
    #  a whole search graph based on the problem data.
    graph: Graph # original (immutable) graph data
    frontier: Frontier # nodes in the search graph that have been generated but not expanded (visited)
    reached: dict[Hashable, SearchNode] # SearchNodes that have been generated or expanded, i.e. nodes in the frontier
                              # plus nodes that have been visited
    # NOTE: (expanded nodes) ∪ (frontier nodes) == reached nodes
    start_node: SearchNode
    goal_node: SearchNode

    def __init__(self, graph: Graph, start_node_id: Hashable, goal_node_id: Hashable):
        # NOTE: for Dijkstra's algorithm, the Graph (including weighted edges), start_node,
        #  and goal_node comprise the problem, alongside the assumption that every action
        #  involves traversing from one node to an adjacent node, and the action cost is
        #  the weight of the edge, and that the optimal solution involves the path with
        #  lowest cost.
        self.graph = graph
        self.start_node = SearchNode(StateNode(start_node_id, graph.edges(start_node_id, data=True)), None, 0)
        self.goal_node = SearchNode(StateNode(goal_node_id, graph.edges(goal_node_id, data=True)), None, float('inf'))
        self.frontier = Frontier()
        self.frontier.add(self.start_node)
        self.reached = {self.start_node.state.state: self.start_node}

    def solve(self) -> None:
        while not self.frontier.is_empty():
            # visit phase
            current_node = self.frontier.pop()
            if current_node.state.state == self.goal_node.state.state:
                self.finish(True, current_node)
                return
            # expand phase
            for child_node in self.expand(current_node):
                if child_node.state.state not in self.reached.keys() or child_node.path_cost < self.reached[child_node.state.state].path_cost:
                    self.reached[child_node.state.state] = child_node
                    self.frontier.add(child_node)
        self.finish(False, None)

    def expand(self, node: SearchNode) -> set[SearchNode]:
        expanded: set = set()
        for _, child_id, edge_data in node.state.edges:
            path_cost = node.path_cost + edge_data['weight']
            child_node = SearchNode(StateNode(child_id, self.graph.edges(child_id, data=True)), node, path_cost)
            expanded.add(child_node)
        return expanded

    def finish(self, success: bool, last_node):
        if success:
            print(f'success!')
            print(f'reached goal node: {last_node.state.state}')
            print(f"goal node cost: {last_node.path_cost}")
            solution_path: list[Hashable] = []
            path_node = last_node
            reached_start = False
            while not reached_start:
                solution_path.append(path_node.state.state)
                if not path_node.parent:
                    reached_start = True
                else:
                    path_node = path_node.parent
            solution_path.reverse()
            print(f"path to goal: {solution_path}")
        else:
            print(f'finished without success.')
            print(f"reached nodes:")
            for key, value in self.reached.items():
                print(f"{key}, cost: {value.path_cost}")


if __name__ == "__main__":
    dijkstra_traverser = Traverser(G, "A", "C")
    dijkstra_traverser.solve()
    draw_graph()
    print("done.")
