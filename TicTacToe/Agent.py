from abc import ABCMeta
from abc import abstractmethod
from Tic_Tac_Toe import TicTacToe


class Agent(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, player):
        self.player = player
        self.other_player = (player % 2) + 1

    #retorna (x,y), valor estimado si existe
    @abstractmethod
    def policy(self, board: TicTacToe):
        pass