
from dataclasses import dataclass
from os import stat
from typing import Iterable


class ProblemModel:
    def get_actions(self, state) -> Iterable[str]:
        """get possible actions from the state

        Args:
            state (int | str): state representation of the problem

        Returns:
            iterable[str]: iterable of actions
        """
        raise NotImplementedError()
    
    def get_result(self, state, action) -> int|str:
        """get the result state (s') of applying "action" to "state"

        Args:
            state (int | str): state representation
            action (str): action representation

        Returns:
            int | str: child or result state
        """
        raise NotImplementedError()
    
    def get_action_cost(self, state, action, child) -> int:
        """returns the cost of applying the action to get from state to child

        Args:
            state (int|str): the state representation
            action (str): action of the state
            child (int|str): child state of state

        Raises:
            NotImplementedError: _description_

        Returns:
            int: cost
        """
        raise NotImplementedError()


@dataclass
class BaseSearch:
    
    def path_to(self, goal_state: str):
        raise NotImplementedError()
            
    def set_problem_model(self, model: ProblemModel):
        self.model = model

    def set_initial_state(self, state):
        self.initial_state = state

    def get_model_actions(self, state):
        """get possible actions from the model

        Args:
            state (int | str): state representation of the problem

        Returns:
            iterable[str]: iterable of actions
        """
        return self.model.get_actions(state)
    
    def get_model_result(self, state, action):
        """get the result state (s') of applying "action" to "state"

        Args:
            state (int | str): state representation
            action (str): action representation

        Returns:
            int | str: child or result state
        """
        return self.model.get_result(state, action)

    def get_model_action_cost(self, state, action, child):
        return self.model.get_action_cost(state, action, child)
