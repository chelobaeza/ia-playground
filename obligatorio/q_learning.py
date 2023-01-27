from dataclasses import dataclass
from functools import reduce
import pickle
from time import time
from typing import Dict, List
import numpy as np
import pathlib


class QMonitor:
    start_time = None
    end_time = None
    start_episode_time = None
    episode_time = None
    explore_policy_count = 0
    exploit_policy_count = 0
    success_episode_count = 0
    episode_count = 0
    episode_step_count = 0
    max_episode_step_count = 0
    average_episode_step_count = 0
    explore_chance = 0
    is_q_loaded_from_file = False
    
    def __init__(self, alpha, gamma) -> None:
        self.alpha = alpha
        self.gamma = gamma
    
    def set_explore_chance(self, explore_chance):
        self.explore_chance = explore_chance
    
    def start_policy_timer(self):
        self.start_time = time()
    
    def stop_policy_timer(self):
        self.end_time = time()
    
    def start_episode_timer(self):
        self.start_episode_time = time()
    
    def count_explore_policy(self):
        self.explore_policy_count += 1
    
    def count_exploit_policy(self):
        self.exploit_policy_count += 1
    
    def q_loaded_from_file(self):
        self.is_q_loaded_from_file = True
    
    def count_success_episode(self):
        self.success_episode_count += 1
    
    def done_learning(self):
        self.is_done_learning = True
    
    def close_and_print_episode(self, total_episodes, episode_steps, avg_episode_steps):
        self.episode_count = total_episodes
        self.episode_time = time() - self.start_episode_time
        self.episode_step_count = episode_steps
        self.average_episode_step_count = avg_episode_steps
        if self.episode_step_count > self.max_episode_step_count:
            self.max_episode_step_count = self.episode_step_count
        print(self)
        self.episode_step_count = 0
        self.exploit_policy_count = 0
        self.explore_policy_count = 0
    
    def __repr__(self) -> str:
        return str(self.__dict__)



class QLearning:
    """
    Estimacion de la estrategia optima π∗ = arg max Q
    
    alpha = factor de aprendizaje
    gamma = factor de convergencia
    """
    AVG_EPISODE_LEARNING_STEPS = 500
    MIN_EXPLORE_CHANCE = 0.005
    
    bins = None
    
    def __init__(self, env, q_path=None,
                 explore_chance=1,
                 alpha=0.11,
                 gamma=0.9999,
                 training_set=10000,
                 explore_chance_decrease_value=.0001
                ) -> None:
        self.environment = env
        self.q_path = q_path
        self.explore_chance = explore_chance
        self.alpha = alpha
        self.gamma = gamma
        self.training_set = training_set
        self.explore_chance_decrease_value = explore_chance_decrease_value
        self.monitor = QMonitor(alpha, gamma)
        self.initialize_q()

    def initialize_q(self):
        if self.q_path and pathlib.Path(self.q_path).exists():
            self.load_q_from_file()
        else:
            self.create_q()

    def load_q_from_file(self):
        if pathlib.Path(self.q_path).exists():
            with open(self.q_path, 'rb') as file:
                self.Q = pickle.load(file)
                self.monitor.q_loaded_from_file()
                print(self.Q.shape)
            print("Q loaded")
    
    def save_q_to_file(self):
        print("Saving Q to file")
        with open(self.q_path, 'wb') as file:
            pickle.dump(self.Q, file)

    def create_q(self):
        self.Q = np.random.random((31,31,61,31,2))

    def best_policy(self):
        self.monitor.start_policy_timer()
        self.monitor.set_explore_chance(self.explore_chance)
        last_episode_steps = 0
        total_episode_steps = 0
        total_episodes = 0
        avg_episode_steps = 0
        try:
            while self.is_q_learning(avg_episode_steps):
                self.monitor.start_episode_timer()
                episode_steps = self.create_episode()
                if total_episodes > self.training_set and self.explore_chance > self.MIN_EXPLORE_CHANCE and episode_steps >= last_episode_steps:
                    self.update_explore_chance()
                    self.monitor.set_explore_chance(self.explore_chance)
                last_episode_steps = episode_steps
                total_episode_steps += episode_steps
                total_episodes += 1
                avg_episode_steps = total_episode_steps / total_episodes
                if total_episodes % 100 == 0:
                    self.save_q_to_file()
                self.monitor.close_and_print_episode(total_episodes, episode_steps, avg_episode_steps)
            self.monitor.done_learning()
        except Exception as e:
            print(e())
        finally:
            self.save_q_to_file()
            self.monitor.stop_policy_timer()
            return self.monitor
    
    def is_q_learning(self, avg_episode_steps):
            return avg_episode_steps < self.AVG_EPISODE_LEARNING_STEPS
        
    def create_episode(self):
        obs = self.environment.reset()
        done = False
        total_reward = 0
        state = self.get_state(obs)
        while not done: 
            action = self.epsilon_greedy_policy(state)
            obs, reward, done, _ = self.environment.step(action)
            next_state = self.get_state(obs)
            # print('->', state, action, reward, next_state, done, info)
            self.improve_q(state, action, next_state, reward)
            state = next_state
            total_reward += reward
        return total_reward
            
    def get_state(self, obs):
        if self.bins is None:
            self.bins = [
                np.linspace(-2.4, 2.4, 30),
                np.linspace(-2, 2, 30),
                np.linspace(-.2095, .2095, 60),
                np.linspace(-2, 2, 30),
            ]
        state = tuple(np.digitize(np.array([item]), bin_list)[0]
             for item, bin_list
             in zip(obs, self.bins))
        return state
    
    def update_explore_chance(self):
        self.explore_chance -= self.explore_chance_decrease_value
    
    def epsilon_greedy_policy(self, state):
        explore = np.random.binomial(1, self.explore_chance)
        if explore:
            action = self.environment.action_space.sample()
            self.monitor.count_explore_policy()
        else:
            action = self.optimal_policy(state)
            self.monitor.count_exploit_policy()
        return action
    
    def optimal_policy(self, state):
        action = np.argmax(self.Q[state])
        return action
    
    def improve_q(self, state, action, next_state, reward):
        next_state_max_q = np.max(self.Q[next_state])
        self.Q[state][action] += self.alpha * (
            reward 
            + self.gamma * next_state_max_q
            - self.Q[state][action]
        )
