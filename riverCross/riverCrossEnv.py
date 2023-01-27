import gym
from gym import error, spaces, utils
from gym.utils import seeding
from functools import reduce


class RiverCrossEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    passengerToState = ["cabbageSide", "goatSide","wolfSide", None]
    directionToDestinationSide = [1,0]
    
    def __init__(self):
        self.observation_space = spaces.Dict({
                # 0: left
                # 1: right
                "farmerSide": spaces.Discrete(2),
                "cabbageSide": spaces.Discrete(2),
                "goatSide": spaces.Discrete(2),
                "wolfSide": spaces.Discrete(2),
            })
    
        self.action_space = spaces.Dict({
                # 0: left to right
                # 1: right to left
                "direction": spaces.Discrete(2),
                # 0: Cabbage
                # 1: Goat
                # 2: Wolf
                # 3: empty
                "passenger": spaces.Discrete(4)
            })
        self.state = {
                "farmerSide": 0,
                "cabbageSide": 0,
                "goatSide": 0,
                "wolfSide": 0,
                }

    def step(self, action):
        if (not(self._check_action(action))):
            return self.state, self._get_reward(), self._is_end(), {}

        self.state = self.state.copy()
        
        newBoatSide = RiverCrossEnv.directionToDestinationSide[action["direction"]]
        
        self.state["farmerSide"] = newBoatSide
        
        passenger = RiverCrossEnv.passengerToState[action["passenger"]]
        if (passenger is not None):
            self.state[passenger] = newBoatSide
        
        self._check_state(self.state)        
        return self.state, self._get_reward(), self._is_end(), {}
        
    
    def _check_action(self, action):
        if (not(self.action_space.contains(action))):
            raise Exception('Action not in action_space') 
            
        if (action["direction"]!=self.state["farmerSide"]):
            return False
            
        if (action["passenger"]!=3 
            and self.state[RiverCrossEnv.passengerToState[action["passenger"]]]
                !=action["direction"]):
            return False

        return True
        
    def _check_state(self, state):
        if (not(self.observation_space.contains(state))):
            raise Exception('State not in observation_space') 
    
    def _get_reward(self):
        toCheck = ["farmerSide", "cabbageSide", "goatSide","wolfSide"]
        win = reduce(lambda x, y: x and y ,map(lambda x: self.state[x]==1, toCheck), True)
        if win:
            return 1
        else:
            return 0
        
    def _is_end(self):
        return (self.state["farmerSide"]!=self.state["goatSide"] # farmer is not with the goat
                and (
                        self.state["goatSide"]==self.state["wolfSide"] # the wolf eats the goat
                        or self.state["goatSide"]==self.state["cabbageSide"] # the goat eats the cabbage
                        )
                ) or 0<self._get_reward() # win

    def reset(self):
        self.state = {
                "farmerSide": 0,
                "cabbageSide": 0,
                "goatSide": 0,
                "wolfSide": 0,
                }
        return self.state
    

    def _render(self, _state, mode='human', close=False):
        if close:
            return
        base = "__ "
        
        toCheck = ["cabbageSide", "goatSide","wolfSide"]
        
        bySide = [[x for x in toCheck if _state[x]==i] for i in [0,1]]
        
        toChar = {
                "cabbageSide": "C",
                "goatSide": "G",
                "wolfSide": "W",
                }
        
        [side0, side1] = [[toChar[bySide[s][i]] if i<len(bySide[s]) else base[i] for i in range(0, len(base))] 
            for s in [0,1]]
        
        ret = "".join(side0 + ["<" if _state["farmerSide"]==0 else ">"] + side1[::-1])
        
        return ret

    def render(self, mode='human', close=False):
        print(self._render(self.state, mode, close))
        






















