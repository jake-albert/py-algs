class Singly:
    """Singly-linked list class with O(1) access to head.
    
    Attributes:
        head: A Node instance, or None.
        size: An int. Number of nodes in the list.
    """

    class Node:
        """Building block class for singly linked list."""
        
        def __init__(self,value=None,next=None):
            """Inits Node with optional next nodes and value."""
            self.val = value
            self.next = next
    
    def __init__(self,values=None):
        """Inits empty Doubly by default, or loads with values.
        
        Args:
            values: A list of initial values to be stored at Nodes. If 
              not None and non-empty, will be inserted such that the 
              values' order is maintained (item at index 0 will be 
              head, item at index -1 tail.)
        """
        self.head = None
        self.size = 0
        if values is not None:
            for i in range(len(values)-1,-1,-1):
                self.insert_head(values[i])
    
    def display(self):
        """Prints the values at Nodes head to tail in O(N) time. Does 
        not terminate if the list is circular."""
        if self.head is None:
            print("List is empty.")
        else:
            n = self.head
            while n is not None:
                print(n.val, '-->', end=' ')
                n = n.next
            print('|| ({0} items)'.format(self.size))
    
    def insert_head(self,value):
        """Inserts a Node with value at the head in O(1) time.
        
        Returns:
            The new head Node instance.
        """
        new_head = self.Node(value, self.head)
        self.head = new_head
        self.size += 1
        return self

    def is_empty(self):
        """Returns a Boolean."""
        return self.head is None
        
    def remove_head(self):
        """Removes head Node and returns value there in O(1) time. If 
        list is empty, returns None."""
        if not self.head is None:
            old_head = self.head
            self.head = self.head.next
            self.size -= 1
            return old_head.val
        
    def insert_tail(self, value):
        """Inserts a Node with value at the tail in O(N) time.
        
        Returns:
            The new tail Node instance.
        """
        new = self.Node(value, None)
        cur = self.head
              
        # On an empty list, the tail is the head.
              
        if cur is None:
            self.head = new
            self.size += 1
            return new
        
        # Otherwise, traverse the full list to the tail.
        
        while cur.next is not None:
            cur = cur.next
        cur.next = new
        self.size += 1
        return new 
        
    def delete_one(self, value):
        """Deletes the node closest to the head of the list with a 
        given value, and makes no change if no such node exists. Runs
        in O(N) time worst case as it must traverse the entire list.""" 
        if self.size == 0:
            return
        
        # Delete and return immediately if first node matches value.
        
        cur = self.head
        if cur.val == value:
            self.head = cur.next
            self.size -= 1
            return
        
        # Otherwise, traverse entire list.
        
        while cur.next is not None:
            if cur.next.val == value:
                cur.next = cur.next.next
                self.size -= 1
                return
            cur = cur.next
        return