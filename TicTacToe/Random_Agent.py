import numpy as np
from Agent import Agent
from Tic_Tac_Toe import TicTacToe


class RandomAgent(Agent):
    def __init__(self, player: int):
        super().__init__(player)

    def policy(self, board: TicTacToe):
        empty_cells = board.get_available_cells()
        pos = empty_cells[np.random.choice(range(len(empty_cells)))]
        return pos, None
