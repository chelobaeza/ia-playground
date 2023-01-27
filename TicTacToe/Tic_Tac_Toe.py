import numpy as np


class TicTacToe():
    int_to_string = ["-", "X", "O"]

    def __init__(self):
        self.grid = np.zeros((3, 3), dtype=np.int)

    def render(self):
        """Imprime el tablero en consola"""
        print("===========================")
        print("---------------------------")
        for i in range(3):
            for j in range(3):
                print("|%4s   |" %
                      self.int_to_string[self.grid[i][j]], end="")
            print("")
            print("---------------------------")

    def clone(self):
        """Me devuelve otro board igual"""
        board_clone = TicTacToe()
        board_clone.grid = np.copy(self.grid)
        return board_clone

    def play(self, pos: tuple, value: int):
        """Pos es la posicion donde quiero insertar.\nValue es el jugador, puede ser 1 o 2"""
        if all(value != i for i in [1, 2]):
            raise Exception("You can only insert X(1) or O(2) in the grid. Received: {}".format(value))
        if self.grid[pos[0]][pos[1]] != 0:
            raise Exception("You can only add symbols in empty spaces")
        self.grid[pos[0]][pos[1]] = value        
        return self.is_end()

    def board_is_full(self):
        return len(self.get_available_cells()) == 0

    def get_available_cells(self):
        """Devuelve todas las posiciones en las que se puede agregar una ficha"""
        cells = []
        for x in range(3):
            for y in range(3):
                if self.grid[x][y] == 0:
                    cells.append((x, y))
        return cells

    def random_play(self, pos: tuple, value: int):
        """
        Inserta la ficha en la posicion deseada, e inserta la ficha del rival.\n
        Devuelve: (True/False que indica si termino el juego, 0/1/2 que indica si se empato (0) o el jugador que gano)
        """
        done, winner = self.insert_symbol(pos, value)
        if not done:
            done, winner = self.add_random_tile((value % 2)+1)
        return done, winner

    def is_end(self):
        """
        Devuelve: (True/False que indica si termino el juego, 0/1/2 que indica si se empato (0) o el jugador que gano)
        """
        # vertical
        for i in range(3):
            total = [0, 0, 0]  # -, X, O
            total[self.grid[0, i]] += 1
            total[self.grid[1, i]] += 1
            total[self.grid[2, i]] += 1
            for j in range(1, 3):
                if total[j] == 3:
                    return True, j
        # horizontal
        for i in range(3):
            total = [0, 0, 0]  # -, X, O
            total[self.grid[i, 0]] += 1
            total[self.grid[i, 1]] += 1
            total[self.grid[i, 2]] += 1
            for j in range(1, 3):
                if total[j] == 3:
                    return True, j
        # diagonal arriba izq, abajo der
        total = [0, 0, 0]  # -, X, O
        for i in range(3):
            total[self.grid[i, i]] += 1
        for j in range(1, 3):
            if total[j] == 3:
                return True, j
        # diagonal abajo izq, arriba der
        total = [0, 0, 0]  # -, X, O
        for i in range(3):
            total[self.grid[2-i, i]] += 1
        for j in range(1, 3):
            if total[j] == 3:
                return True, j
                
        return self.board_is_full(), 0

    def add_random_tile(self, value: int):
        empty_cells = self.get_available_cells()
        pos_to_add = empty_cells[np.random.choice(range(len(empty_cells)))]
        return self.insert_symbol(pos_to_add, value)
