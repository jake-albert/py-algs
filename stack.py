# Stack class implemented using a List object

class Stack:

    # optional loading of items onto stack during initialization
    def __init__(self, loads=None):
        self.items = []
        if loads is not None:
            for load in loads:
                self.push(load)
        
    def push(self, item):
        self.items.append(item)
        
    def pop(self):
        if self.isEmpty():
            return None
        return self.items.pop()
    
    def peek(self):
        if self.isEmpty():
            return None
        return self.items[len(self.items)-1]
        
    def isEmpty(self):
        return self.items == []
        
    # since the stack is implemented using an accessible list, it is possible to 
    # write this O(n) display method without modifying the stack for debugging
    def display(self):
        print("top <|", end=" ")
        for index in range(len(self.items)-1, -1, -1):
            print(self.items[index], end=" ")
        print("<| bottom")