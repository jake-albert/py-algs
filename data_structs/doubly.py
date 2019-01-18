class Doubly:
    ''' Doubly-linked list class. 
    '''
    
    # doubly linked list is made of individual nodes
    class Node:
        
        def __init__(self, value=None, next=None, prev=None):
            if value is None:
                self.val = None
            else:
                self.val = value
            if next is None:
                self.next = None
            else:
                self.next = next
            if prev is None:
                self.prev = None
            else:
                self.prev = prev
                
    # can be initialized to reference objects in a Python list, with the 
    # first value of the list as the head
    def __init__(self, values=None):
        self.head = None
        self.tail = None
        self.size = 0
        if values is not None:
            while len(values) > 0:
                self.insert_head(values.pop())
    
    # print the values of the nodes in order
    def display(self):
        if self.head is None:
            print("List is empty.")
        else:
            n = self.head
            while n is not None:
                print(n.val, '<->', end=' ')
                n = n.next
            print('|| ({0} items)'.format(self.size))
    
    # insert a node with a given value at the head
    def insert_head(self, value):
        new_head = self.Node(value, self.head, None)
        if self.head is not None:
            self.head.prev = new_head
        else:
            self.tail = new_head
        self.head = new_head
        self.size += 1
        return new_head
        
    # insert a node with a given value at the tail
    def insert_tail(self, value):        
        new_tail = self.Node(value, None, self.tail)
        if self.tail is not None:
            self.tail.next = new_tail
        else:
            self.head = new_tail
        self.tail = new_tail
        self.size +=1
        return new_tail
        
    # remove the node at the tail
    def remove_tail(self):
        if self.tail is None:
            return None
        
        self.size -= 1
        return_val = self.tail.val
        
        if self.tail is self.head:
            self.head, self.tail = None, None
        
        else:
            new_tail = self.tail.prev
            new_tail.next = None
            self.tail = new_tail
        
        return return_val
    
    # move a node from its current position to the head
    def move_to_head(self,node):
    
        # make changes only if node is not already head
        if node.prev is not None:
            
            # if node is tail but not head, then prev is new tail
            if node.next is None:
                self.tail = node.prev
            else:
                node.next.prev = node.prev
                
            # regardless, make sure node is now skipped
            node.prev.next = node.next
            node.prev = None
            
            # update node so it is at head now, and update head
            node.next = self.head
            node.next.prev = node
            self.head = node