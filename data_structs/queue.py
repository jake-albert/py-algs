from .doubly import Doubly

class LinkedListQueue:
    ''' Queue implemented with a doubly linked list. Note that if loading
    the queue with a list of items during construction, the last item is
    inserted first and thus will be removed last as well. 
    
    '''
    
    def __init__(self, loads=None):
        if loads is not None:
            self.queue = Doubly(loads)
        else:
            self.queue = Doubly()
        
    def add(self, item):
        self.queue.insert_head(item)
    
    def remove(self):
        if not self.is_empty():
            item = self.queue.tail.val
            return self.queue.remove_tail()
    
    def peek(self):
        if not self.is_empty():
            return self.queue.tail.val
        
    def is_empty(self):
        return self.queue.size == 0

from collections import deque
        
class DequeQueue:
    ''' Queue implemented with the optimized deque object. Will raise an 
    exception on attempt to peek or remove while empty.
    '''
    
    def __init__(self):
        self.queue = deque()
        
    def add(self, item):
        self.queue.appendleft(item)
    
    def remove(self):
        return self.queue.pop()
        
    def peek(self):
        return self.queue[-1]
        
    def is_empty(self):
        return len(self.queue) == 0
        
    def __len__(self):
        return len(self.queue)