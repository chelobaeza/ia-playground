
class PriorityQueue(): 

    def __init__(self): 
        self.queue = [] 
  
    def __str__(self): 
        return ' '.join([str(i) for i in self.queue]) 

    def is_empty(self): 
        return len(self.queue) == 0

    def push(self, data, cost): 
        for i in range(len(self.queue)): 
            if cost <= self.queue[i][1]: 
                self.queue = self.queue[:i] + [(data, cost)] + self.queue[i:]
                return
        self.queue = self.queue + [(data, cost)]
  
    def pop(self): 
        if(self.is_empty()):
            return None
        return self.queue.pop(0)

    def update(self, data, new_cost):
        self.remove(data)
        self.push(data, new_cost)

    def remove(self, data):
        if(self.is_empty()):
            return
        
        for i in range(len(self.queue)): 
            if(data == self.queue[i][0]):
                self.queue = self.queue[:i] + self.queue[i+1:]
                return
    
    def __contains__(self, key):
        list_of_items = [(x[0]) for x in self.queue]
        return (key) in list_of_items