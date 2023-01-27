import numpy as np
from Tic_Tac_Toe import TicTacToe
from Agent import Agent
from Random_Agent import RandomAgent
from Agent_Minimax import AgentMinimax

def print_winner(winner: int):
    if winner == 0:
        print("Empate")
    elif winner == 1:
        print("Gano jugador 1")
    elif winner == 2:
        print("Gano jugador 2")
    else:
        print("Paso algo raro")
    
agent1 = AgentMinimax(1) #X
agent2 = RandomAgent(2) #0
agents = [agent1, agent2]

tic_tac_toe = TicTacToe()
done = False
winner = -1
i = 0
while not done:
    i = (i+1) % 2
    pos, value = agents[i].policy(tic_tac_toe)
    done, winner = tic_tac_toe.play(pos, agents[i].player)
    tic_tac_toe.render()
print_winner(winner)