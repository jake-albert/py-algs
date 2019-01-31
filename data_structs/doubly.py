class Doubly:
    """Doubly linked list class with O(1) access to both head and tail.
    
    Attributes:
        head: A Node instance, or None.
        tail: A Node instance, or None.
        size: An int. Number of nodes in the list.
    """
    
    class Node:
        """Building block class for doubly linked list."""
        
        def __init__(self,value=None,next=None,prev=None):
            """Inits Node with optional next, prev nodes and value."""
            self.val = value
            self.next = next
            self.prev = prev
            
    def __init__(self,values=None):
        """Inits empty Doubly by default, or loads with values.
        
        Args:
            values: A list of initial values to be stored at Nodes. If 
              not None and non-empty, will be inserted such that the 
              values' order is maintained (item at index 0 will be 
              head, item at index -1 tail.)
        """ 
        self.head = None
        self.tail = None
        self.size = 0
        if values is not None:
            for value in values:
                self.insert_tail(value)
    
    def is_empty(self):
        """Returns a Boolean."""
        return self.head is None
    
    def display(self):
        """Prints the values at Nodes head to tail in O(N) time. Does 
        not terminate if the list is circular."""
        if self.head is None:
            print("List is empty.")
        else:
            n = self.head
            while n is not None:
                print(n.val, '<->', end=' ')
                n = n.next
            print('|| ({0} items)'.format(self.size))
    
    def insert_head(self,value):
        """Inserts a Node with value at the head in O(1) time.
        
        Returns:
            The new head Node instance.
        """
        new_head = self.Node(value,self.head,None)
        if self.head is not None:
            self.head.prev = new_head
        else:
            self.tail = new_head
        self.head = new_head
        self.size += 1
        return new_head
        
    def insert_tail(self,value):        
        """Inserts a Node with value at the tail in O(1) time.
        
        Returns:
            The new tail Node instance.
        """
        new_tail = self.Node(value,None,self.tail)
        if self.tail is not None:
            self.tail.next = new_tail
        else:
            self.head = new_tail
        self.tail = new_tail
        self.size +=1
        return new_tail
            
    def remove_tail(self):
        """Removes tail Node and returns value there in O(1) time. If 
        list is empty, returns None."""
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
    
    def move_to_head(self,node):
        """Moves Node from current position to head in O(1) time."""
        if node.prev is not None:
            
            # If node is tail but not head, then the linked list's tail
            # must be reassigned. Otherwise, "skip" node moving from 
            # tail to head.
            
            if node.next is None:
                self.tail = node.prev
            else:
                node.next.prev = node.prev
                
            # "Skip" node moving from head to tail, and set at head.
            
            node.prev.next = node.next
            node.prev = None      
            node.next = self.head
            node.next.prev = node
            self.head = node