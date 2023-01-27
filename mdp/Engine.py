import gym
import numpy as np

_cool = 'Cool'
_warm = 'Warm'
_hot = 'Hot'
_overheated = 'Overheated'

_slow = 'slow'
_fast = 'fast'

class Engine(gym.Env) :
    
    def __init__(self) :
        self.action_space = [_slow, _fast]
        self.observation_space = [_cool, _warm, _overheated]
        self._state = ''
        # Rewards
        self._R = { _cool : { 
                    _slow : { _cool : 1 , _overheated : -100 }, 
                    _fast : {_cool: 1 , _warm:10, _overheated:-100} 
                    },
                    _warm : {
                        _slow:{_cool: 1, _warm: 2, _overheated:-100},
                        _fast:{_hot:10, _overheated:-100}
                    },
                    _hot : {
                        _slow:{_cool:1, _warm:2, _overheated:-100}
                    }
                 }
        # Probabilities
        self._P = { _cool : { 
                        _slow : { _cool : 8/10 , _overheated : 2/10 }, 
                        _fast : {_cool: 1/8 , _warm:5/8, _overheated:2/8} 
                    },
                    _warm : {
                        _slow:{_cool: 2/5, _warm: 2/5, _overheated:1/5},
                        _fast:{_hot: 1/2, _overheated: 1/2}
                    },
                    _hot:{
                        _slow:{_cool:2/6, _warm:3/6, _overheated:1/6}
                    }
                 }


    def _action_list(self):
        return list(self._P.get(self._state, {}).keys())

    def reset(self):
        self._state = _cool
        return self._state, {'actions': self._action_list()}
        
    def step(self, action) -> tuple[str, int, bool]:  
        if self._state == _overheated : 
            raise Exception('Engine is overheated')
        next_state_probs = self._P[self._state][action]
        next_state = np.random.choice(list(next_state_probs.keys()), size=1, p=list(next_state_probs.values()))[0]
        
        reward = self._R[self._state][action][next_state]
        self._state = next_state
        done = next_state == _overheated
            
        return self._state, reward, done, {'actions': self._action_list()}
        
    def render(self, mode = 'human', close = False) :
        if not(close) :
            print('state:', self._state, 'done:', self._state == 'end')

    
# eng = Engine()
# state, info = eng.reset()
# done = False
# print(state, end='')
# while not done:
#     next_action = np.random.choice(info['actions'], size=1)[0]
#     state, reward, done, info = eng.step(next_action)
#     print(f',{next_action},{reward},{state}', end='')
# print()
