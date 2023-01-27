from datetime import datetime, timedelta
import gc
from time import time
from GameBoard import GameBoard
from Agent import Agent
from Random_Agent import RandomAgent
from expectimax_agent import ExpectiMaxAgent

def check_win(board: GameBoard):
    return board.get_max_tile() >= 2048


int_to_string = ['UP', 'DOWN', 'LEFT', 'RIGHT']

if __name__ == '__main__':
    avg_win_moves = 0
    avg_lost_moves = 0
    avg_win_time = 0
    avg_lost_time = 0
    win_count = 0
    lost_count = 0
    wins = []
    loses = []
    
    kwargs = {'smoothness': -2, 'depth_distribution': [0,0,0,2,8,14]}
    
    for run in range(10):
        agent: Agent
        board: GameBoard
        agent = ExpectiMaxAgent(**kwargs)
        board = GameBoard()
        done = False
        moves = 0
        board.render()
        start = datetime.now()
        time_start = time()
        while not done:
            action = agent.play(board)
            print('Next Action: "{}"'.format(
                int_to_string[action]), ',   Move: {}'.format(moves))
            done = board.play(action)
            done = done or check_win(board)
            board.render()
            moves += 1
            end_time = datetime.now() - start
            time_end = time()
            print('\nTotal time: {}'.format(end_time))
        print('\nTotal Moves: {}'.format(moves))
        
        duration_sec = time_end - time_start
        if check_win(board):
            print("WON THE GAME!!!!!!!!")
            avg_win_moves += moves
            avg_win_time += duration_sec
            win_count += 1
            wins.append((moves, duration_sec))
        else:
            print("BOOOOOOOOOO!!!!!!!!!")
            avg_lost_moves += moves
            avg_lost_time += duration_sec
            lost_count += 1
            loses.append((moves, duration_sec))
    
    avg_win_moves = avg_win_moves / win_count if win_count else 0
    avg_lost_moves = avg_lost_moves / lost_count if lost_count else 0
    avg_win_time = avg_win_time / win_count if win_count else 0
    avg_win_time = timedelta(seconds=avg_win_time)
    avg_lost_time = avg_lost_time / lost_count if lost_count else 0 
    avg_lost_time = timedelta(seconds=avg_lost_time)
    print("######")
    print(f"weights used: {agent.smoothness=} {agent.depht_distribution=}")
    print(f"WIN: {win_count=} {avg_win_moves=}")
    print(avg_win_time)
    print(f"LOST: {lost_count=} {avg_lost_moves=}")
    print(avg_lost_time)
    print(f"{wins=} \n{loses=}")
