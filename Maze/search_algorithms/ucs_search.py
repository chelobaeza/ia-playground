from queue import Queue
from typing import Generator
from priorityQueue import PriorityQueue
from search_algorithms.base_search import BaseSearch
from search_algorithms.node import Node


class UCSSearch(BaseSearch):
    """uniform-cost search INFORMED
    well known as Dijkstra
    """
    
    def path_to(self, goal_state):
        node = self.find_node(goal_state)
        return self.make_path(node)
    
    def find_node(self, goal_state) -> Node:
        self.goal_state = goal_state
        node = Node(state=self.initial_state, parent_node=None, action=None)
        frontier = PriorityQueue()
        frontier.push(node, 1)
        reached = {node.state: node}
        
        while not frontier.is_empty():
            node, _ = frontier.pop()
            if node.state == self.goal_state:
                return node
            for child in self.get_children_nodes(node):  # expand node
                if child.state not in reached or child.path_cost < reached[child.state].path_cost:
                    reached[child.state] = child
                    frontier.push(child, child.path_cost)
        raise Exception("Error during search")
    
    def get_children_nodes(self, node: Node) -> Generator[Node, None, None]:
        parent_state = node.state
        for action in self.get_model_actions(parent_state):
            child_state = self.get_model_result(parent_state, action)
            cost = self.get_model_action_cost(parent_state, action, child_state) + self.evaluation_function(node=node)
            yield Node(
                state=child_state,
                parent_node=node,
                action=action,
                path_cost=cost
            )
        
    def make_path(self, node: Node):
        """return queue or gen with recursion, with the ordered path
        """
        if node.parent_node.state != self.initial_state:
            yield from self.make_path(node.parent_node)
        yield node
        
    def evaluation_function(self, node: Node):
        return node.path_cost