"""
- perform breadth first search on the below graph
- record the order in which the nodes are visited

version 1 (from class):

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

# traverse the graph using breadth first search

# FIXME: this doesn't actually implement BFS.
# Visitor pattern may still be possible, but the visitor may be more complex.
# Also, using this kind of traverser, which minimizes travel within the graph,
# may not be appropriate for BFS. The BFS algorithm allows us to jump around.
class Traverser:
    visited: list[Node]
    queue: list[Node]

    def __init__(self, start_node: Node):
        self.visited = []
        self.queue = []

    def scan(self):
        # start by adding the parent node to the queue.
        # then visit it.
        # from the perspective of the last node visited
        # add the child nodes to the queue.
        # then visit the queue, 1 by 1 (and move the node from queue to visited)
        # when all nodes from the current queue (the current level) are visited,
        # there will be more nodes in the queue from the next level down.
        # visiting moves the current node from queue to visited
        # visiting adds the current node's children to the queue.
        # once the queue is empty or when a goal is reached, exit
        # and report the visited list and the goal result, if applicable.

        # NOTE: should still be able to do this with a recursive function plus a loop,
        # given the pseudocode above. Just need to modify the actions and add that
        # second queue.


    def walk(self, from_node=None):
        if from_node is None:
            from_node = self.start_node
            self.visited.append(from_node)
        # "process" loop
        for node in from_node.children:
            self.visited.append(node)
        # "spawn walkers" loop
        for node in from_node.children:
            self.walk(node)
        if from_node == self.start_node:
           print(f'BFS traversal complete.')
           self.print_history()

    def print_history(self):
        output: list = [x.node_id for x in self.visited]
        print(f'Path from {self.start_node.node_id}: {output}')


if __name__ == "__main__":
    bfs_traverser = Traverser(parent_node)
    bfs_traverser.walk()
    traversed_ids = [x.node_id for x in bfs_traverser.visited]
    assert traversed_ids == [0, 7, 5, 3, 2, 4, 1, 6] # breadth first order

    bfs_traverser_2 = Traverser(parent_node_2)
    bfs_traverser_2.walk()
    traversed_ids = [x.node_id for x in bfs_traverser_2.visited]
    assert traversed_ids == ["A", "B", "C", "D", "E", "F", "N", "G", "H", "I", "J", "K"] # breadth first order
