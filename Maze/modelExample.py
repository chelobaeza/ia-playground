from abc import ABC, abstractmethod
from typing import Iterable
from search_algorithms.base_search import ProblemModel
from model import Model

class ModelExample(Model, ProblemModel):
    graph = None

    def __init__(self, model_file):
        self.model_file = model_file
        self.relative_path = 'gym_maze/envs/maze_samples/'
        super().__init__(model_file)
    
    def reset(self):
        super().reset()
        self.graph = {}
        self._load_model(self.relative_path + self.model_file)

    def _load_model(self, fullpath):
        print("Load your model here with file:", fullpath)
        with open(str(fullpath), 'r') as f:
            for line in f:
                node, action, child = self.read_node_childs(line)
                if node not in self.graph:
                    self.graph[node] = {}
                self.graph[node][action] = child
    
    def read_node_childs(self, text_node):
        node, action, child = text_node.strip().split(' ')
        return node, action, child
    
    def get_actions(self, state) -> Iterable[str]:
        return self.graph[state].keys()
    
    def get_result(self, state, action) -> int | str:
        return self.graph[state][action]
    
    def get_action_cost(self, state, action, child) -> int:
        cost = int(child)
        return cost if cost > 0 else 1
        # return 1
