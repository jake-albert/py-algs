from .doubly import Doubly
from collections import deque

class LinkedListQueue:
    """Queue implemented with my doubly linked list class.
    
    Attributes:
        queue: A Doubly instance that simulates the queue.
    """
    
    def __init__(self,loads=None):
        """Inits an empty LinkedListQueueQueue by default. If loads is
        not None and non-empty, loads items into queue such that the 
        first item in loads is the first that will be removed."""
        if loads is not None:
            self.queue = Doubly(loads)
        else:
            self.queue = Doubly()
     
    def __len__(self):
        return self.queue.size
     
    def add(self, item):
        """Adds an item in O(1) time."""
        self.queue.insert_head(item)
    
    def remove(self):
        """Removes and returns the least-recently added item in O(1)
        time. Returns None if queue is empty."""
        if not self.is_empty():
            return self.queue.remove_tail()
    
    def peek(self):
        """Returns the least-recently added item in O(1) time. Returns 
        None if queue is empty."""
        if not self.is_empty():
            return self.queue.tail.val
        
    def is_empty(self):
        """Returns a Boolean."""
        return self.queue.size == 0
        
class DequeQueue:
    """Queue implemented with the Python deque object. 
    
    Attributes:
        queue: A deque object."""
    
    def __init__(self,loads=None):
        """Inits an empty DequeQueue. If loads is not None and 
        non-empty, loads items into queue such that the first item in 
        loads is the first that will be removed."""
        self.queue = deque()
        if loads is not None:
            for load in loads:
                self.add(load)
                
    def __len__(self):
        return len(self.queue)
     
    def add(self,item):
        """Adds an item in O(1) time."""
        self.queue.appendleft(item)
    
    def remove(self):
        """Removes and returns least-recently added item in O(1) time.
        
        Raises:
            IndexError: queue is empty.
        """
        return self.queue.pop()
        
    def peek(self):
        """Returns least-recently added item in O(1) time.
        
        Raises:
            IndexError: queue is empty.
        """
        return self.queue[-1]
        
    def is_empty(self):
        """Returns a Boolean."""
        return len(self.queue) == 0