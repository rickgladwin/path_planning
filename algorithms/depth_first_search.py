"""
- perform depth first search on the below graph
- record the order in which the nodes are visited

  0
  │
  ├─────┬──┐
  7     5  3
  ├──┐  │  │
  2  4  1  6

version 2 (from https://www.youtube.com/watch?v=-yF6k_bV_JQ):

                             ┌───┐
                             │ A │
                             └┬┬┬┘
                              │││
          ┌───────────────────┘│└─────────────┐
          │                    │              │
        ┌─┴─┐                ┌─┴─┐          ┌─┴─┐
        │ B │                │ C │          │ D │
        └┬─┬┘                └─┬─┘          └┬─┬┘
         │ │                   │             │ │
  ┌──────┘ └─────┐        ┌────┘       ┌─────┘ └─────┐
┌─┴─┐          ┌─┴─┐    ┌─┴─┐        ┌─┴─┐         ┌─┴─┐
│ E │          │ F │    │ N │        │ G │         │ H │
└───┘          └┬─┬┘    └───┘        └──┬┘         └───┘
                │ │                     │
          ┌─────┘ └────┐                └─────┐
        ┌─┴─┐        ┌─┴─┐                  ┌─┴─┐
        │ I │        │ J │                  │ K │
        └───┘        └───┘                  └───┘

(see https://monosketch.io/ for ASCII drawing tool)

(see https://monosketch.io/ for ASCII drawing tool)
"""
from graphs.node import Node

# build a graph of Nodes
parent_node = Node(0, [])
parent_node.children = [
    Node(7, [
        Node(2),
        Node(4),
    ]),
    Node(5, [
        Node(1),
    ]),
    Node(3, [
        Node(6)
    ]),
]

parent_node_2 = Node("A", [])
parent_node_2.children = [
    Node("B", [
        Node("E"),
        Node("F", [
            Node("I"),
            Node("J")
        ])
    ]),
    Node("C", [
        Node("N")
    ]),
    Node("D", [
        Node("G", [
            Node("K")
        ]),
        Node("H")
    ])
]

# traverse the graph using depth first search

class Traverser:
    start_node: Node
    history: list[Node]
    def __init__(self, start_node: Node):
        self.start_node = start_node
        self.history = []

    def walk(self, from_node=None):
        if from_node is None:
            from_node = self.start_node
        self.history.append(from_node)
        for node in from_node.children:
           self.walk(node)
        if from_node == self.start_node:
           print(f'DFS traversal complete.')
           self.print_history()

    def print_history(self):
        output: list = [x.node_id for x in self.history]
        print(f'Path from {self.start_node.node_id}: {output}')

if __name__ == "__main__":
    dfs_traverser = Traverser(parent_node)
    dfs_traverser.walk()
    traversed_ids = [x.node_id for x in dfs_traverser.history]
    assert traversed_ids == [0, 7, 2, 4, 5, 1, 3, 6] # depth first order

    dfs_traverser = Traverser(parent_node_2)
    dfs_traverser.walk()
    traversed_ids = [x.node_id for x in dfs_traverser.history]
    # TODO: confirm that this is the expected behaviour
    #  Should the deepest node in the tree be explored first, or just the deepest in the current branch?
    #  If the algorithm is rewritten with a frontier, is that proper DFS?
    assert traversed_ids == ['A', 'B', 'E', 'F', 'I', 'J', 'C', 'N', 'D', 'G', 'K', 'H'] # depth first order
