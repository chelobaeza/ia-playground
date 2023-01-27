import numpy as np
from Tic_Tac_Toe import TicTacToe
from Agent import Agent
import random

animation = [
    "[=     ]",
    "[ =    ]",
    "[  =   ]",
    "[   =  ]",
    "[    = ]",
    "[     =]",
    "[    = ]",
    "[   =  ]",
    "[  =   ]",
    "[ =    ]",
]


class AgentMinimax(Agent):
    def __init__(self, player=1):
        super().__init__(player)

    def policy(self, board: TicTacToe):
        self.idx = 0
        pos, value = self.minimax(board, self.player)
        return pos, value

    def minimax(self, board: TicTacToe, player: int, max_depth=10):
        """
        la funcion de evaluacion actual no pondera la cantidad de movimientos restantes
        para ganar o perder, por lo tanto no es muy precisa.
        """
        
        #Animación para que se vea lindo
        print(animation[int(self.idx/300) % len(animation)], end="\r")
        self.idx += 1   

        #Caso base
        max_depth -= 1
        end, winner = board.is_end()
        if max_depth == 0 or end:
            if end:
                value = -1
                if winner == self.player:
                    value = 1
                elif winner == 0:
                    value = 0
                return None, value  # -1 si pierde 0 empate 1 gano el player
            
            value = self.value_of_node(board, player)
            return None, value
        
        #Casos no base
        
        actions = board.get_available_cells()
        random.shuffle(actions)
        action_nodes = []
        for action in actions:
            child_node = board.clone()
            child_node.play(action, player)
            action_nodes.append((action, child_node))

        value = 0
        chosen_action = None
        
        child_nodes_values = [self.minimax(node, self.next_player(player), max_depth)[1] for _, node in action_nodes]
        if player != self.player: # mini
            #Buscar acción que minimiza el valor
            arg_min = np.argmin(child_nodes_values)
            chosen_action = actions[arg_min]
            value = child_nodes_values[arg_min]
                

        else: #max (player == self.player)
            #Buscar acción que maximiza el valor            
            arg_max = np.argmax(child_nodes_values)
            chosen_action = actions[arg_max]
            value = child_nodes_values[arg_max]
            

        return chosen_action, value
    
    def value_of_node(self, board:TicTacToe, player):
        node = board.clone()
        available_cells = node.get_available_cells()
        self.fill_with_player_play(node, available_cells, player)
        player_play_value = self.get_play_value_of_player(node, player)
        player = self.next_player(player)
        self.fill_with_player_play(node, available_cells, player)
        next_player_play_value = self.get_play_value_of_player(node, player)
        return player_play_value - next_player_play_value
        
    
    def fill_with_player_play(self, node, cells, player):
        for x, y in cells:
            node.grid[x][y] = player
    
    def next_player(self, player):
        return 2 if player == 1 else 1

    def get_play_value_of_player(self, node:TicTacToe, player):
        player_wins_number = 0
        # vertical
        for i in range(3):
            total = [0, 0, 0]  # -, X, O
            total[node.grid[0, i]] += 1
            total[node.grid[1, i]] += 1
            total[node.grid[2, i]] += 1
            if total[player] == 3:
                player_wins_number += 1
        # horizontal
        for i in range(3):
            total = [0, 0, 0]  # -, X, O
            total[node.grid[i, 0]] += 1
            total[node.grid[i, 1]] += 1
            total[node.grid[i, 2]] += 1
            if total[player] == 3:
                player_wins_number += 1
        # diagonal arriba izq, abajo der
        total = [0, 0, 0]  # -, X, O
        for i in range(3):
            total[node.grid[i, i]] += 1
        if total[player] == 3:
            player_wins_number += 1
        # diagonal abajo izq, arriba der
        total = [0, 0, 0]  # -, X, O
        for i in range(3):
            total[node.grid[2-i, i]] += 1
        if total[player] == 3:
            player_wins_number += 1
        return player_wins_number
            