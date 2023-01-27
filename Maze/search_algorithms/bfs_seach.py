

from asyncio import Queue
from lib2to3.pytree import Node
from search_algorithms.ucs_search import UCSSearch


class BreadthFirstSearchUninformed(UCSSearch):
    """Breadth-first search
    
    uninformed bfs search with the early goal efficiency enhancements:
  
    frontier: PriorityQueue -> Fifo queue
    reached: dict -> set
    
    this is apropiate when all actions have the same cost.
    """
    def find_node(self, goal_state):
        node = Node(state=self.initial_state, parent_node=None, action=None)
        if node.state == goal_state:
            return node
        frontier = Queue()
        frontier.put(node)
        reached = set((node.state))
        
        while not frontier.is_empty():
            node = frontier.get()
            for child in self.get_children_nodes(node):  # expand node
                if child.state == goal_state:
                    return node
                if child.state not in reached:
                    reached.add(child)
                    frontier.put(child)
        raise Exception("Error during search")