
import pathlib
import gym
import time
from random import randint
from q_learning import QLearning

env = gym.make('CartPole-v1', render_mode='human')

#  Run with fixed explore_chance and training_set = 0 to avoid initial explore training
#  The normal use case would be to exploit the existing model
q_learning = QLearning(env, "q_learnings.pkl", explore_chance=0, training_set=0)
#  Run with explore_chance=1 to start from fresh model
# q_learning = QLearning(env, "new_q_learnings.pkl", explore_chance=1)
monitor = q_learning.best_policy()
print(monitor)
print(f"execution time: {monitor.end_time - monitor.start_time}")
env.close()