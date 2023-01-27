from Tic_Tac_Toe import TicTacToe
from Agent import Agent

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


class AgentExpectimax(Agent):
    def __init__(self, player=1, max_depth: int = 10):
        super().__init__(player)
        self.max_depth = max_depth

    def policy(self, board: TicTacToe):
        self.idx = 0
        pos, value = self.expectimax(board, self.player, self.max_depth)
        return pos, value 

    def expectimax(self, board: TicTacToe, player: int, depth: int):
        #Animación para que se vea lindo
        print(animation[int(self.idx/300) % len(animation)], end="\r")
        self.idx += 1

        
        #TODO: Completar

        #Caso base


        #Casos no base
        actions = board.get_available_cells()
        action_nodes = []
        for action in actions:
            child_node = board.clone()
            child_node.insert_symbol(action, player)
            action_nodes.append((action, child_node))

        value = 0
        chosen_action = None        
        if player != self.player: # Expecti
            #Calcular valor promedio de las acciones del oponente
            pass
        else: #max
            #Buscar acción que maximiza el valor
            pass

        return chosen_action, value
