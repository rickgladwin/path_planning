class Node:
    """
    Node in a tree graph with an arbitrary number of children
    """
    node_id: int
    children: list
    def __init__(self, node_id, children=None):
        if children is None:
            children = []
        self.node_id = node_id
        self.children = children
