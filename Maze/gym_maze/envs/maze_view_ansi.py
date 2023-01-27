import numpy as np
import os
from gym_maze.envs.maze import Maze


class MazeViewAnsi:
    maze: Maze

    def __init__(self, maze_file_path=None,
                 maze_size=(30, 30),
                 has_loops=False, num_portals=0, entrance=(0, 0), goal_pos=None):
        self.__game_over = False
        if maze_file_path is None:
            self.__maze = Maze(maze_size, has_loops,
                               num_portals, entrance, goal_pos)
        else:
            if not os.path.exists(maze_file_path):
                dir_path = os.path.dirname(os.path.abspath(__file__))
                rel_path = os.path.join(
                    dir_path, "maze_samples", maze_file_path)
            if os.path.exists(rel_path):
                maze_file_path = rel_path
            else:
                raise FileExistsError("Cannot find %s." % maze_file_path)
            self.__maze = Maze(maze_cells=Maze.load_maze(maze_file_path))
            self.maze_size = self.__maze.maze_size
            self.__entrance = np.array(entrance, dtype=int)
            self.__goal = np.array(self.maze_size) - np.array((1, 1)
                                                              ) if goal_pos is None else np.array(goal_pos, dtype=int)
            self.__robot = np.array(entrance, dtype=int)

    def move_robot(self, dir):
        if dir not in self.__maze.COMPASS.keys():
            raise ValueError("dir cannot be %s. The only valid dirs are %s." % (
                str(dir), str(self.__maze.COMPASS.keys())))
        if self.__maze.is_open(self.__robot, dir):
            self.__robot += np.array(self.__maze.COMPASS[dir])
            # if it's in a portal afterward
            if self.maze.is_portal(self.__robot):
                self.__robot = np.array(self.maze.get_portal(
                    tuple(self.__robot)).teleport(tuple(self.robot)))

    def reset_robot(self):
        self.__robot = self.__entrance

    def save_maze_for_model(self, file_path):
        if not isinstance(file_path, str):
            raise TypeError("Invalid file_path. It must be a str.")

        if not os.path.exists(os.path.dirname(file_path)):
            dir_path = os.path.dirname(os.path.abspath(__file__))
            rel_path = os.path.join(
                dir_path, "maze_samples", file_path)
            if os.path.exists(os.path.dirname(rel_path)):
                file_path = rel_path
            else:
                raise ValueError(
                    "Cannot find the directory for %s." % file_path)

        with open(file_path + ".txt", "w") as output:
            # breaking the walls
            Xmax = len(self.maze.maze_cells)
            Ymax = len(self.maze.maze_cells[0])
            for x in range(Xmax):
                for y in range(Ymax):
                    for d in self.__maze.COMPASS.keys():
                        self.__robot = np.array([x, y])
                        self.move_robot(d)
                        n_x = self.robot[0]
                        n_y = self.robot[1]
                        line = str(y*Xmax + x) + " " + str(d) + \
                            " " + str(n_y*Xmax + n_x)
                        output.write(line + "\n")

    def set_goal(self, goalId):
        Xmax = len(self.maze.maze_cells)
        x = int(goalId % Xmax)
        y = int(goalId / Xmax)
        self.__goal = np.array((x, y))
        self.update()

    def update(self, mode=None):
        for i in range(self.maze.MAZE_H*2+1):
            print("_", end="")
        print("")
        for i in range(self.maze.MAZE_H):
            print("|", end="")
            lower = "|"
            for j in range(self.maze.MAZE_W):
                letter = " "
                snd = ""
                if self.__robot[0] == j and self.__robot[1] == i:
                    letter = "R"
                elif self.__goal[0] == j and self.__goal[1] == i:
                    letter = "G"
                if self.maze.is_open(np.array([j, i]), 'E'):
                    snd = " "
                    print(letter+" ", end="")
                else:
                    snd = "|"
                    print(letter + "|", end="")
                if self.maze.is_open(np.array([j, i]), 'S'):
                    lower = lower + " " + snd
                else:
                    lower = lower + "_" + (snd if snd != " " else "_")
            print()
            print(lower)
        print("")
        print("")

    def quit_game(self):
        self.__game_over = True

    @property
    def maze(self):
        return self.__maze

    @property
    def robot(self):
        return self.__robot

    @property
    def entrance(self):
        return self.__entrance

    @property
    def goal(self):
        return self.__goal

    @property
    def game_over(self):
        return self.__game_over
