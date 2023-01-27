from Agent import Agent
from GameBoard import GameBoard
import numpy as np


class ExpectiMaxAgent(Agent):
    GOAL = 2048
    
    def __init__(self, smoothness=-2, depth_distribution=None):
        self.player = True
        self.smoothness = smoothness
        self.depht_distribution = depth_distribution or [0,0,0,2,8,14]

    def play(self, board:GameBoard):
        empty_spaces = len(board.get_available_cells())
        depth = np.digitize(16-empty_spaces, self.depht_distribution)
        if depth == 0:
            depth = 1
        print(depth)
        return self.expectimax(board, self.player, depth, -np.Infinity, np.Infinity)[0]
    
    def expectimax(self, board: GameBoard, player: int, depth: int, alpha_max, beta_min):
        #Caso base
        max_tile = board.get_max_tile()
        if max_tile >= self.GOAL:
            return None, np.Infinity          
            
        if depth == 0:
            return None, self.heuristic_utility(board)
        
        value = 0
        chosen_action = None
        if player != self.player: # Expecti
            best_value = np.Infinity
            #Calcular valor promedio de las acciones del oponente
            actions = board.get_available_cells()
            actions_count = 0
            actions_sum = 0
            for action in actions:
                actions_count += 1
                for tile, chance in ((2, .9), (4, .1)):
                    child_node = board.clone()
                    child_node.insert_tile(action, tile)
                    _, expected = self.expectimax(child_node, not player, depth - 1, alpha_max, beta_min)
                    actions_sum += chance * expected
                value = actions_sum / actions_count
                best_value = min(best_value, value)
                beta_min = min(beta_min, best_value)
                if beta_min <= alpha_max:
                    break
            return chosen_action, value  
        else: #max
            #Buscar acción que maximiza el valor
            best_value = -np.Infinity
            actions = board.get_available_moves()
            if actions:
                children_values = []
                for action in actions:
                    child_node = board.clone()
                    child_node.move(action)
                    _, expected = self.expectimax(child_node, not player, depth - 1, alpha_max, beta_min)
                    # child_node.render()
                    # print(f"^^ {expected=} | {action=}")
                    children_values.append(expected)
                    best_value = max(best_value, expected)
                    alpha_max = max(alpha_max, best_value)
                    if beta_min <= alpha_max:
                        break
                action = np.argmax(children_values)
                value = children_values[action]
                chosen_action = actions[action]
            else:  # Sin movimientos => peor value
                value = -np.Infinity
        return chosen_action, value

    def heuristic_utility(self, board: GameBoard):
        """
        Algunas heurisitcas posibles son:\n
            - Calcular el \"smoothness\" del tablero. Esto es porque cuanto mas \"smooth\" el tablero, mas facil es juntar fichas. Para ello debemos:
                - Aplicar la raiz cuadrada al tablero
                - Sumar la diferencia entre cada casilla y la de abajo
                - Sumar la diferencia entre cada casilla y la de la derecha
                - Elevar este resultado a un smoothness_weight a determinar
                - Multiplicar por -1
            - Calcular el valor del tablero. Esto es porque cuanto mas fichas grandes tengo, mas cerca de ganar estoy. Para ello debemos:
                - Elevar el tablero al cuadrado
                - Sumar todos los valores que se encuentran en el tablero
            - Calcular la cantidad de espacios vacios. Esto es porque cuanto mas espacios vacios tengo, menos chance de tener un mal estado. Para ello debemos:
                - Obtener la cantidad de celdas vacias
                - Multiplicar por un empty_weight (recomendable en el orden de las decenas de miles)
        """
        # smoothness
        sqrt_grid = np.sqrt(board.grid)
        y_diff = np.array([sqrt_grid[row] - sqrt_grid[row + 1] for row in range(sqrt_grid.shape[0] - 1)])
        x_diff = np.array([sqrt_grid[:, row] - sqrt_grid[:, row + 1] for row in range(sqrt_grid.shape[0] - 1)])
        sum = y_diff.sum() + x_diff.sum()
        result = -1 * pow(sum, self.smoothness)
        # valor de tablero
        available_cells = len(board.get_available_cells())
        if available_cells > 8:
            pow_grid = np.power(board.grid, 2)
            result *= pow_grid.sum()
        return result
