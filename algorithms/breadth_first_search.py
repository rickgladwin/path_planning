"""
- perform breadth first search on the below graph
- record the order in which the nodes are visited

  0
  │
  ├─────┬──┐
  7     5  3
  ├──┐  │  │
  2  4  1  6

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

# traverse the graph using breadth first search

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
        # "process" loop
        for node in from_node.children:
            self.history.append(node)
        # "spawn walkers" loop
        for node in from_node.children:
            self.walk(node)
        if from_node == self.start_node:
           print(f'BFS traversal complete.')
           self.print_history()

    def print_history(self):
        output: list = [x.node_id for x in self.history]
        print(f'Path from {self.start_node.node_id}: {output}')


if __name__ == "__main__":
    bfs_traverser = Traverser(parent_node)
    bfs_traverser.walk()
    traversed_ids = [x.node_id for x in bfs_traverser.history]
    assert traversed_ids == [0, 7, 5, 3, 2, 4, 1, 6] # breadth first order
