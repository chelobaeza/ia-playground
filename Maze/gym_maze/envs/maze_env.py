import numpy as np

import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym_maze.envs.maze_view_2d import MazeView2D
from gym_maze.envs.maze_view_ansi import MazeViewAnsi


class MazeEnv(gym.Env):
    metadata = {
        "render.modes": ["human", "ansi"],
    }

    ACTION = ["N", "S", "E", "W"]

    def __init__(self, maze_file=None, maze_size=None, has_loops=False, mode="ansi"):
        self.mode = mode
        self.viewer = None

        if maze_file:
            if mode == "human":
                self.maze_view = MazeView2D(maze_name="OpenAI Gym - Maze (%s)" % maze_file,
                                            maze_file_path=maze_file,
                                            screen_size=(640, 640))
            elif mode == "ansi":
                self.maze_view = MazeViewAnsi(maze_file_path=maze_file)
        elif maze_size:
            if mode == "human":
                self.maze_view = MazeView2D(maze_name="OpenAI Gym - Maze (%d x %d)" % maze_size,
                                            maze_size=maze_size, screen_size=(
                                                640, 640),
                                            has_loops=has_loops)
            elif mode == "ansi":
                self.maze_view = MazeViewAnsi(
                    maze_size=maze_size, has_loops=has_loops)
        else:
            raise AttributeError(
                "One must supply either a maze_file path (str) or the maze_size (tuple of length 2)")

        self.maze_size = self.maze_view.maze_size

        # forward or backward in each dimension
        self.action_space = spaces.Discrete(2*len(self.maze_size))

        # observation is the x, y coordinate of the grid
        low = np.zeros(len(self.maze_size), dtype=int)
        high = np.array(self.maze_size, dtype=int) - \
            np.ones(len(self.maze_size), dtype=int)
        self.observation_space = spaces.Box(low, high)

        # initial condition
        self.observation = None
        self.steps_beyond_done = None

        # Simulation related variables.
        self._seed()
        self._reset()

        # Just need to initialize the relevant attributes
        self._configure()

    def __del__(self):
        self.maze_view.quit_game()

    def _configure(self, display=None):
        self.display = display

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action):
        if isinstance(action, int):
            self.maze_view.move_robot(self.ACTION[action])
        else:
            self.maze_view.move_robot(action)

        if np.array_equal(self.maze_view.robot, self.maze_view.goal):
            reward = 1
            done = True
        else:
            reward = 0
            done = False

        self.observation = self.maze_view.robot

        info = {}

        return self.observation, reward, done, info

    def _reset(self):
        self.maze_view.reset_robot()
        self.observation = self.maze_view.robot
        self.steps_beyond_done = None
        self.done = False
        return self.observation

    def is_game_over(self):
        return self.maze_view.game_over

    def render(self, mode="human", close=False):
        if close:
            self.maze_view.quit_game()

        return self.maze_view.update(mode)
