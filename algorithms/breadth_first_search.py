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

class Traverser:
    visited: list[Node]
    queue: list[Node]
    goal_met: bool

    def __init__(self):
        self.visited = []
        self.queue = []
        self.goal_met = False

    def visit(self, current_node: Node):
        self.visited.append(current_node)
        self.queue.extend(current_node.children)

        # TODO: evaluate a goal or goals here.

        if len(self.queue) != 0:
            # self.print_queue()
            self.visit(self.queue.pop(0))
        else:
            print(f'BFS Traversal complete.')


    def print_history(self):
        output: list = [x.node_id for x in self.visited]
        print(f'Path from parent_node: {output}')


    def print_queue(self):
        output: list = [x.node_id for x in self.queue]
        print(f'current queue: {output}')


if __name__ == "__main__":
    bfs_traverser = Traverser()
    bfs_traverser.visit(parent_node)
    bfs_traverser.print_history()
    traversed_ids = [x.node_id for x in bfs_traverser.visited]
    assert traversed_ids == [0, 7, 5, 3, 2, 4, 1, 6] # breadth first order

    bfs_traverser_2 = Traverser()
    bfs_traverser_2.visit(parent_node_2)
    bfs_traverser_2.print_history()
    traversed_ids = [x.node_id for x in bfs_traverser_2.visited]
    assert traversed_ids == ["A", "B", "C", "D", "E", "F", "N", "G", "H", "I", "J", "K"] # breadth first order
