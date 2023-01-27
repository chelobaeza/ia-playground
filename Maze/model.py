from abc import ABC, abstractmethod

#DO NOT CHANGE THIS CLASS: EXTEND IT WITH YOUR OWN
class Model(ABC):

    def __init__(self, model_file):
        super().__init__()
        self.reset()

    def get_goal(self, step):
        GOALS = { 
            0: (39, True), # with only this goal we can see that A* is faster but more expensive than UCS
            # 0: (29, False),
            # 5: (80, False),
            # 10: (9, False),
            # 15: (85, False),
            # 20: (99, True)
        }
        self.current_goal = GOALS.get(step, self.current_goal) 

        return self.current_goal

    def reset(self):
        self.current_goal = None

    def is_win_goal(self):
        if self.current_goal == None:
            return False
        return self.current_goal[1]

