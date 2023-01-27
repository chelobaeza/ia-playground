import gym
import numpy as np

class DiceGame(gym.Env) :
    
    def __init__(self) :
        self.action_space = ['stay', 'quit']
        self.observation_space = ['in', 'end']
        self.state = ''
        # Rewards
        self.R = { 'in' : { 'stay' : { 'in' : 4.0 , 'end' : 4.0 }, 
                            'quit' : {'end': 10.0 } } }
        # Probabilities
        self.P = { 'in' : { 'stay' : { 'in' : 2/3, 'end' : 1/3 }, 
                            'quit' : { 'end' : 1 } } }

    def reset(self) :
        self.state = 'in'
        return self.state
        
    def step(self, action) :  
        if self.state == 'end' : 
            raise Exception('Game is over')
            
        _state = self.state

        if action == 'quit' : 
            self.state = 'end'
        else :
            success = np.random.binomial(1, 2/3)
            if not(success) : 
                self.state = 'end'
        
        done = self.state == 'end'
        
        reward = self.R[_state][action][self.state]
            
        return self.state, reward, done, {}
        
    def render(self, mode = 'human', close = False) :
        if not(close) :
            print('state:', self.state, 'done:', self.state == 'end')

    