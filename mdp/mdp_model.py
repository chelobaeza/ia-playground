from dataclasses import dataclass
from functools import reduce
from typing import Dict, List
import numpy as np

@dataclass
class Transition:
    current_state: str
    action: str
    next_state: str
    reward: int = 0
    probability: float = 0
    probability_diff: float = 0
    
    acumulated_reward: int = 0  # suma de las responmpensas de (s,a,s')
    count: int = 0  # ocurrencias de (s,a,s')

    def __repr__(self) -> str:
        return f"R: {self.reward}, P: {self.probability}"

    def set_probability(self, new_prob):
        self.probability_diff = abs(self.probability - new_prob)
        self.probability = new_prob

    def add_reward_and_count(self, new_reward):
        self.acumulated_reward += new_reward
        self.count += 1


class MDPCreator:
    """Markov Decission Process
    this class creates an online MDP from a given environment
    
    precision: difference from last probability. when mdp is stable then stops 
    min_episodes: min episodes are reandomly created at least, before it can finish 
    when the last 2 conditions are met then the mdp is done.
    """
    
    def __init__(self, env, precision = 0.001, min_episodes = 1000) -> None:
        self.environment = env
        self.precision = precision
        self.min_episodes = min_episodes

    def create_model(self):
        self.model = {}
        self.mdp_model: List[Transition] = []
        episode_count = 0
        while not self.is_mdp_done() or episode_count < self.min_episodes:
            episode = self.create_episode()
            print(f"episode {episode}")
            self.set_estimated_probability_and_reward()
            episode_count += 1
        return self.model, episode_count
    
    def create_episode(self):
        state, info = self.environment.reset()
        done = False
        reward = 0
        episode = []
        # print(state, end='')
        while not done:
            next_action = np.random.choice(info['actions'], size=1)[0]
            episode.append((reward, state, next_action))
            next_state, reward, done, info = self.environment.step(next_action)
            if state not in self.model:
                self.model[state] = {}   
            if next_action not in self.model[state]:
                self.model[state][next_action] = {"count": 0}
            if next_state not in self.model[state][next_action]:
                new_mdp_node = Transition(
                    current_state=state,
                    action=next_action,
                    next_state=next_state
                )
                self.model[state][next_action][next_state] = new_mdp_node
                self.mdp_model.append(new_mdp_node)
            self.model[state][next_action]['count'] += 1
            node:Transition = self.model[state][next_action][next_state]
            node.add_reward_and_count(reward)
            # print(f',{next_action},{reward},{next_state}', end='')
            state = next_state
        episode.append((reward, state, ""))
        return episode
    
    def set_estimated_probability_and_reward(self):
        for transition in self.mdp_model:
            prob_estimate = self.estimate_probability(transition)
            transition.set_probability(prob_estimate)
            transition.reward = self.estimate_reward(transition)
    
    def estimate_probability(self, transition: Transition):
        state_action_state_count = transition.count
        state_action_count = self.model[transition.current_state][transition.action]['count']
        return state_action_state_count / state_action_count
    
    def estimate_reward(self, transition: Transition):
        state_action_state_reward = transition.acumulated_reward
        state_action_state_count = transition.count
        return state_action_state_reward / state_action_state_count
    
    def is_mdp_done(self):
        """Is done when de rewards/probabilities doesn't change 
        or they do very little
        """
        if not self.mdp_model:
            return False
        transitions_has_min_precision = list(map(lambda diff: diff <= self.precision, [transition.probability_diff for transition in self.mdp_model]))
        return reduce(lambda a, b: a and b, transitions_has_min_precision)

