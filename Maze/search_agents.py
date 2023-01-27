from modelExample import ModelExample
from search_algorithms.a_star_search import AStarSearch, Heuristic
from search_algorithms.base_search import BaseSearch
from search_algorithms.ucs_search import UCSSearch
from agent import Agent


class SearchAgent(Agent):
    name = None
    model: ModelExample
    search_algorithm: BaseSearch
    
    def __init__(self, model, search_algorithm=None):
        super().__init__(model)
        if search_algorithm:
            self.search_algorithm = search_algorithm
        print(type(self.search_algorithm))
        self.search_algorithm.set_problem_model(self.model)
        
    def _loop(self, env):
        self.last_goal = None
        print(self.name)
        obs = env.reset()
        # print(obs)
        done = False
        step_counter = 0
        all_rewards = 0
        self.total_cost = 0
        env.render()

        while not done:
            action = self.next_action(obs, step_counter, env)
            self.check_action(action)
            obs, reward, done_env, _ = env.step(action)
            # print(f'{obs=} {reward=} {done_env=}')
            all_rewards += reward
            done = done_env and self.model.is_win_goal()
            env.render()
            step_counter += 1
        print(f"COST!: {self.total_cost}")
        return all_rewards, step_counter

    def next_action(self, obs, step_counter, env):
        goalId = self.model.get_goal(step_counter)[0]
        env.set_goal(goalId)
        if goalId is not self.last_goal:
            self.last_goal = goalId
            self.search_algorithm.set_initial_state(
                state=self.convert_observation_to_model_representation(obs)
            )
            self.path_to_goal = self.search_algorithm.path_to(str(goalId))
        node = next(self.path_to_goal)
        ###
        state = node.state
        cost = self.model.get_action_cost("", "", state)
        print(f"state {state} cost: {cost}")
        self.total_cost += cost
        ###
        return node.action

    def convert_observation_to_model_representation(self, obs):
        return str(int(f"{obs[1]}{obs[0]}"))

    def check_action(self, action):
        if action not in ["N", "E", "S", "W"]:
            raise ValueError("Run Ended - Invalid Action")


class AgentUCS(SearchAgent):
    name = "UCS"
    search_algorithm = UCSSearch()
    
    
class ManhatanHeuristic(Heuristic):
    def evaluate(self, initial, goal):
        goal_x, goal_y = self.decompose(goal)
        initial_x, initial_y = self.decompose(initial)
        distance_to_goal = goal_x - initial_x + goal_y - initial_y
        return abs(distance_to_goal)
    
    def decompose(self, state):
        if len(state) == 1:
            return 0, int(state)
        else:
            return int(state[0]), int(state[1])
    
    
class AgentA(SearchAgent):
    name = "A*"
    search_algorithm = AStarSearch(heuristic=ManhatanHeuristic(), weight=1000)