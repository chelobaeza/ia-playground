from dataclasses import dataclass
from typing import Generator
from priorityQueue import PriorityQueue
from search_algorithms.base_search import BaseSearch
from search_algorithms.node import Node
from search_algorithms.ucs_search import UCSSearch

class Heuristic:
    def evaluate(self, initial, goal):
        raise NotImplementedError()

@dataclass
class AStarSearch(UCSSearch):
    """this is same as UCS but the evaluation function now have one more term as heuristic
    """
    heuristic: Heuristic
    weight: int = 1
    
    def evaluation_function(self, node: Node):
        heuristic = self.heuristic.evaluate(node.state, self.goal_state)
        return node.path_cost + heuristic * self.weight