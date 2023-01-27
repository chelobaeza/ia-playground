from gym_maze.envs.maze_env import MazeEnv
import numpy as np
import pygame
import random

from gym_maze.envs.maze_view_2d import MazeView2D


class MazeEnvExtended(MazeEnv):

    def __init__(self, *args, **kwargs):
        super(MazeEnvExtended, self).__init__(*args, **kwargs)
        self.trace = False
        self.trace_count = np.zeros(self.maze_size, dtype=int)

    def reset(self):
        self.reset_trace()
        return super()._reset()

    def should_trace_location(self, trace):
        self.trace = trace

    def reset_trace(self):
        self.trace_count = np.zeros(self.maze_size, dtype=int)
        for i in range(0, self.maze_size[0]):
            for j in range(0, self.maze_size[1]):
                self._draw_trace(np.array([i, j]))

    def step(self, action):
        prev_obs = np.array(self.observation)

        obs, reward, done, info = super()._step(action)

        if (prev_obs is not None
                and not(np.array_equal(self.observation_space, prev_obs))
                and self.trace):
            self.trace_count[int(prev_obs[0]), int(
                prev_obs[1])] = self.trace_count[int(prev_obs[0]), int(prev_obs[1])] + 1
            self._draw_trace(prev_obs)

        return obs, reward, done, info

    def _draw_trace(self, position):
        if self.mode == "human":
            x = int(position[0] * self.maze_view.CELL_W +
                    self.maze_view.CELL_W * 0.5 + 0.5)
            y = int(position[1] * self.maze_view.CELL_H +
                    self.maze_view.CELL_H * 0.5 + 0.5)
            r = int(min(self.maze_view.CELL_W, self.maze_view.CELL_H)/5 + 0.5)

            opacity = min(
                [self.trace_count[int(position[0]), int(position[1])]*50, 255])

            pygame.draw.circle(self.maze_view.maze_layer,
                               (0, 150, 0, opacity), (x, y), r)

    def set_goal(self, goalId):
        self.maze_view.set_goal(goalId)
