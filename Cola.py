from queue import PriorityQueue
import itertools

class ColaFIFO:
    def __init__(self):
        self.cola = []
    
    def empty(self):
        return len(self.cola) == 0
    
    def top(self):
        return self.cola[0] if not self.empty() else None
    
    def pop(self):
        return self.cola.pop(0) if not self.empty() else None
    
    def add(self, item):
        self.cola.append(item)

class ColaLIFO:
    def __init__(self):
        self.cola = []
    
    def empty(self):
        return len(self.cola) == 0
    
    def top(self):
        return self.cola[-1] if not self.empty() else None
    
    def pop(self):
        return self.cola.pop() if not self.empty() else None
    
    def add(self, item):
        self.cola.append(item)

class ColaPrioridad:
    def __init__(self):
        self.cola = PriorityQueue()
        self._count = itertools.count() 
    
    def empty(self):
        return self.cola.empty()
    
    def top(self):
        return self.cola.queue[0][2] if not self.empty() else None
    
    def pop(self):
        return self.cola.get()[2] if not self.empty() else None
    
    def add(self, item, prioridad):
        count = next(self._count)
        self.cola.put((prioridad, count, item))
