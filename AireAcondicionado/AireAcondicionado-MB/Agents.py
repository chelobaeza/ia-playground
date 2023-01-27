import numpy as np

class AgentReflex():

    def lookup(self, obs):
        if obs > 9:
            return -3
        elif obs > 5:
            return -2
        elif obs > 2:
            return -1
        elif obs < -2:
            return 1
        elif obs < -5:
            return 2
        elif obs < -9:
            return 3
        else:
            return 0
        
class AgentModelBased():

    def __init__(self):
        self.prev_obs = 0
        
    def lookup(self, obs):
    
        diff = obs - self.prev_obs
        self.prev_obs = obs

        # state hot (obs > 0) & temp rising (obs - prev_obs > 0)
        if obs > 0 and (diff > 0):
            return int(np.maximum(-3.0, -obs))

        # state hot (obs > 0) & temp lowering (obs - prev_obs <= 0)
        if obs > 0 and (diff <= 0):
            return int(np.maximum(-1.0, -obs))

        # state cold (obs < 0) & temp rising (obs - prev_obs > 0)
        if obs < 0 and (diff > 0):
            return int(np.minimum(1.0, -obs))

        # state cold (obs > 0) & temp lowering (obs - prev_obs <= 0)
        if obs < 0 and (diff <= 0):
            return int(np.minimum(3.0, -obs))

        return 0
    
