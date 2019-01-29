class Stack:
    ''' Stack class implemented using a List object. '''
    
    def __init__(self, loads=None):
        ''' Constructor with option to load multiple values. '''
        self.items = []
        if loads is not None:
            for load in loads:
                self.push(load)
        
    def push(self, item):
        self.items.append(item)
        
    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop()
    
    def peek(self):
        if self.is_empty():
            return None
        return self.items[len(self.items)-1]
        
    def is_empty(self):
        return self.items == []
        
    # since the stack is implemented using an accessible list, it is possible to 
    # write this O(n) display method without modifying the stack for debugging
    def display(self):
        print("top <|", end=" ")
        for index in range(len(self.items)-1, -1, -1):
            print(self.items[index], end=" ")
        print("<| bottom")