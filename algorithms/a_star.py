"""
Use the A* algorithm to solve this 8-puzzle.

┌───────────────────────┐       ┌───────────────────────┐
│      Initial State    │       │       Goal State      │
│                       │       │                       │
├───────┬───────┬───────┤       ├───────┬───────┬───────┤
│   2   │   8   │   3   │       │   1   │   2   │   3   │
├───────┼───────┼───────┤       ├───────┼───────┼───────┤
│   1   │   6   │   4   │       │   8   │       │   4   │
├───────┼───────┼───────┤       ├───────┼───────┼───────┤
│   7   │       │   5   │       │   7   │   6   │   5   │
└───────┴───────┴───────┘       └───────┴───────┴───────┘

https://monosketch.io/

The simple evaluation function f(x) is defined as follows:
f(x) = g(x)+h(x)
where,
g(x) = depth of node X in the search tree (equivalent to cost so far)
h(x) = the number of tiles not in their goal position in a given state X (equivalent to minimum cost to completion)

States: Location of eight tiles plus blank
Initial state: Any state can be designated as the initial state
Actions: Blank tile moves left, right, up, or down and exchanges places with a numbered tile
Successor function: Actions have their expected effects
Goal test: Check whether the goal configuration is reached
Path cost: Each step costs 1

Determine the following:
- Is this puzzle solvable?
- If so, what is the minimum number of steps to complete the puzzle?

Extended challenge: Write a Python script to solve the puzzle using the A* algorithm.
Whether you feel you have the skills to do this or not, it is a valuable exercise to work through the steps required.

----

- branching factor will be minimum 2, maximum 4 for any given state, depending on the location of the blank space.
- it should be possible to generate a state graph for this problem by applying the valid actions
  to any state on the frontier.

"""

# enable late evaluation of types (allows us to use type declarations
# in classes that are the type of the class itself)
from __future__ import annotations

from typing import Hashable


class Problem:
    """
    The properties and constraints on the problem, and the actions and constraints on the solution(s)
    """
    start_node: StateNode
    goal_node: StateNode
    actions: tuple

    def __init__(self, start_node, goal_node):
        self.start_node = start_node
        self.goal_node = goal_node
        self.actions = (self.swap_up, self.swap_down, self.swap_right, self.swap_left)

    """
    The actions for the problem that move from one SearchNode to another
    are a set of swaps between the blank space and another tile.
    
    As these actions are intended to generate new SearchNodes and not just
    move between known states, the functions will return StateNodes, which
    we will then use to generate new SearchNodes.
    """
    def swap_up(self, from_state: StateNode.state_id) -> StateNode.state_id:
        """
        012 --> no swaps
        345 --> swap index with -3
        678 --> swap index with -3
        """
        new_state = from_state
        blank_index = from_state.index("0")

        if blank_index <= 2:
            raise RuntimeError("Can't swap up: blank is already in top row.")

        swap_index = blank_index - 3
        swap_tile = from_state[swap_index]
        new_state = str_replace_char_at(new_state, blank_index, swap_tile)
        new_state = str_replace_char_at(new_state, swap_index, "0")

        return new_state


    def swap_down(self, from_state: StateNode.state_id) -> StateNode.state_id:
        """
        012 --> swap index with +3
        345 --> swap index with +3
        678 --> no swaps
        """
        new_state = from_state
        blank_index = from_state.index("0")

        if blank_index >= 6:
            raise RuntimeError("Can't swap down: blank is already in bottom row.")

        swap_index = blank_index + 3
        swap_tile = from_state[swap_index]
        new_state = str_replace_char_at(new_state, blank_index, swap_tile)
        new_state = str_replace_char_at(new_state, swap_index, "0")

        return new_state


    def swap_right(self, from_state: StateNode.state_id) -> StateNode.state_id:
        """
        012
        345
        678
          ↑ no swaps
        ↑↑  index + 1
        """
        new_state = from_state
        blank_index = from_state.index("0")

        if blank_index in (2,5,8):
            raise RuntimeError("Can't swap right: blank is already in right column.")

        swap_index = blank_index + 1
        swap_tile = from_state[swap_index]
        new_state = str_replace_char_at(new_state, blank_index, swap_tile)
        new_state = str_replace_char_at(new_state, swap_index, "0")

        return new_state


    def swap_left(self, from_state: StateNode.state_id) -> StateNode.state_id:
        """
        012
        345
        678
        ↑   no swaps
         ↑↑ index - 1
        """
        new_state = from_state
        blank_index = from_state.index("0")

        if blank_index in (0,3,6):
            raise RuntimeError("Can't swap right: blank is already in left column.")

        swap_index = blank_index - 1
        swap_tile = from_state[swap_index]
        new_state = str_replace_char_at(new_state, blank_index, swap_tile)
        new_state = str_replace_char_at(new_state, swap_index, "0")

        return new_state


def str_replace_char_at(string: str, char_index: int, new_char: chr) -> str:
    if char_index < 0 or char_index >= len(string):
        raise ValueError("position must be within string length")

    new_string = string[:char_index] + new_char + string[char_index + 1:]
    return new_string


class StateNode:
    """
    A Node in the underlying state data from the problem.
    """
    # a minimal representation of the state of the puzzle board, e.g.
    # ├─┬─┬─┤
    # │2│8│3│
    # ├─┼─┼─┤
    # │1│6│4│ ==> "283164705"
    # ├─┼─┼─┤
    # │7│ │5│
    # └─┴─┴─┘
    #
    state_id: str

    # NOTE: in this case, the actions available from each state will follow a set
    #  of rules that will depend on the position of the blank square. So we can
    #  assign responsibility for this information to a more singular entity,
    #  like a Problem class, a Solver/Traverser class, or even the Frontier class, as part
    #  of the expand() function (though this seems like a stretch – the expand() function
    #  should expand based on what it's given, not be responsible for knowing the rules of expansion)

    # NOTE: the fact that this class consists of a single property and a generic constructor
    #  is a code smell, but it's a result of trying to build these search solvers in the most
    #  general way possible, ideally being able to refactor the general structure in a simple way
    #  in order to adapt the template to different algorithms and problem types.

    def __init__(self, state_id):
        self.state_id = state_id


class SearchNode:
    """
    A Node in the search graph, generated while solving the problem.
    """
    problem: Problem
    state: StateNode
    parent: SearchNode
    path_cost: int
    actions: tuple

    def __init__(self, problem: Problem, state_node: StateNode, parent_node: SearchNode | None, path_cost: int | float):
        self.problem = problem
        self.state: StateNode = state_node
        self.parent: SearchNode = parent_node
        # the action that led to this SearchNode
        # self.action = action
        # set the actions available to this SearchNode
        # NOTE: setting the actions functions as properties on the SearchNodes is sensible so long as
        #  a) memory isn't at risk of being used up and
        #  b) the functions are passed by reference and stored as pointers until they're actually used
        self.set_actions()
        self.path_cost = path_cost

    def set_actions(self) -> None:
        """
        Based on the state, some actions are permitted and some are excluded, depending on the
        position of the blank space. Set the available actions for this SearchNode.
        """
        blank_index = self.state.state_id.index("0")
        node_actions = list(self.problem.actions)
        if blank_index <= 2:
            # can't swap up
            node_actions.remove(self.problem.actions[0])
        if blank_index >= 6:
            # can't swap down
            node_actions.remove(self.problem.actions[1])
        if blank_index in (2,5,8):
            # can't swap right
            node_actions.remove(self.problem.actions[2])
        if blank_index in (0,3,6):
            # can't swap left
            node_actions.remove(self.problem.actions[3])
        self.actions = tuple(node_actions)


class Frontier:
    """
    The Frontier class for best-first-search.
    For A*, evaluate() uses some metric for judging the cost for a node in the frontier,
    for example ortholinear proximity to the goal node. For an 8-puzzle, we're using
    f(x) = g(x)+h(x)
    where
    g(x) = depth of node X in the search tree (equivalent to cost so far)
    h(x) = the number of tiles not in their goal position in a given state X (equivalent to minimum cost to completion)
    Note that we could use the sum of the distances of each tile from the goal state instead of/in addition to h(x).
    The exact evaluation function alters the algorithm, but is only used to select one node from the frontier, so it
    only needs to be as fine-tuned as that task requires.
    """
    nodes: set[SearchNode]
    goal_node: SearchNode

    def __init__(self, goal_node):
        self.nodes = set()
        self.goal_node = goal_node

    def is_empty(self):
        return not self.nodes

    def pop(self) -> SearchNode | None:
        # return the node in the frontier with the best score based on the evaluation function
        # and remove it from the set.
        top_node = self.top()
        self.nodes.remove(top_node)
        return top_node

    def top(self) -> SearchNode | None:
        # return the node in the frontier with the best score (lowest cost, typically)
        # based on the evaluation function, but do not remove it from the set.
        if not self.nodes:
            return None
        best_node = next(iter(self.nodes))
        for node in self.nodes:
            if self.evaluate(node) < best_node.path_cost:
                best_node = node
        return best_node

    def add(self, node: SearchNode) -> None:
        # add the node to the set (unordered, in this example)
        self.nodes.add(node)
        # print(f"Frontier nodes: {self}")

    def evaluate(self, node: SearchNode) -> int:
        # The evaluation function f(n).
        # return a score for the node based on the criteria defined by the problem or algorithm type
        return node.path_cost + self.nodes_out_of_goal_count(node)

    def nodes_out_of_goal_count(self, node: SearchNode) -> int:
        """
        e.g.                           ↓↓  ↓ ↓↓
        search_node.state.state_id = [234567018]
        goal_node.state.state_id   = [243560781]
        count = 5 (we're not counting the blank space)
        """
        search_state = node.state.state_id
        goal_state   = self.goal_node.state.state_id
        count = 0
        for i in range(0, len(goal_state)):
            if goal_state[i] != 0 and goal_state[i] != search_state[i]:
                count += 1
        return count

    def __str__(self):
        output = ""
        for node in self.nodes:
            output += f"{node.state.state_id}, cost: {node.path_cost}\n"
        return output


class Solver:
    problem: Problem
    frontier: Frontier # nodes in the search graph that have been generated but not expanded (visited)
    reached: dict[Hashable, SearchNode] # SearchNodes that have been generated or expanded,
    # i.e. nodes in the frontier plus nodes that have been visited
    # NOTE: (expanded nodes) ∪ (frontier nodes) == reached nodes
    start_node: SearchNode
    goal_node: SearchNode

    def __init__(self, problem: Problem):
        self.problem = problem
        self.start_node = SearchNode(self.problem, problem.start_node, None, 0)
        self.goal_node = SearchNode(self.problem, problem.goal_node, None, float('inf'))
        self.frontier = Frontier(self.goal_node)
        self.frontier.add(self.start_node)
        self.reached = {self.start_node.state.state_id: self.start_node}

    def solve(self) -> None:
        while not self.frontier.is_empty():
            # visit phase
            current_node = self.frontier.pop()
            if current_node.state.state_id == self.goal_node.state.state_id:
                self.finish(True, current_node)
                return
            # expand phase
            for child_node in self.expand(current_node):
                if (child_node.state.state_id not in self.reached.keys()
                        or child_node.path_cost < self.reached[child_node.state.state_id].path_cost):
                    self.reached[child_node.state.state_id] = child_node
                    self.frontier.add(child_node)
        self.finish(False, None)

    def expand(self, node: SearchNode) -> set[SearchNode]:
        expanded: set = set()
        for action in node.actions:
            path_cost = node.path_cost + 1
            child_state_id = action(node.state.state_id)
            child_node = SearchNode(self.problem, StateNode(child_state_id), node, path_cost)
            expanded.add(child_node)
        return expanded

    def finish(self, success: bool, last_node: SearchNode | None):
        if success:
            print(f'success!')
            print(f'reached goal node: {last_node.state.state_id}')
            print(f"goal node cost: {last_node.path_cost}")
            solution_path: list[Hashable] = []
            path_node = last_node
            reached_start = False
            while not reached_start:
                solution_path.append(path_node.state.state_id)
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
    start_node_1 = StateNode("283164705")
    goal_node_1 = StateNode("123804765")
    problem_1 = Problem(start_node_1, goal_node_1)
    a_star_solver = Solver(problem_1)
    a_star_solver.solve()
    print("done.")
