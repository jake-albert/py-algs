class Stack:
    """Stack class implemented using the Python List object.
    
    Attributes: 
        items: A List of items in the stack.
    """
    
    def __init__(self,loads=None):
        """Inits a Stack instance. Empty by default but may be
        loaded with multiple values."""
        self.items = []
        if loads is not None:
            for load in loads:
                self.push(load)
        
    def push(self, item):
        """Pushes an item onto the stack in O(1) time."""
        self.items.append(item)
        
    def pop(self):
        """Pops an item off of the stack in O(1) time."""
        if self.is_empty():
            return None
        return self.items.pop()
    
    def peek(self):
        """Returns the top item without changing the stack."""
        if self.is_empty():
            return None
        return self.items[len(self.items)-1]
        
    def is_empty(self):
        """Returns a Boolean."""
        return self.items == []
        
    def display(self):
        """Traverses the List used to implement a Stack instance and 
        prints all items from top to bottom in O(N) time. Stack 
        instance is unchanged."""
        print("top <|", end=" ")
        for index in range(len(self.items)-1, -1, -1):
            print(self.items[index], end=" ")
        print("<| bottom")