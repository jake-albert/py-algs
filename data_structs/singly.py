class Singly:
    ''' Singly-linked list class. 
    '''
    
    # singly linked list is made of individual nodes
    class Node:
        
        def __init__(self, value=None, next=None):
            if value is None:
                self.val = None
            else:
                self.val = value
            if next is None:
                self.next = None
            else:
                self.next = next
    
    # can be constructed to have the values of a Python list, with the first 
    # value of the list as the head
    def __init__(self, values=None):
        self.head = None
        self.size = 0
        if values is not None:
            while len(values) > 0:
                self.insert_head(values.pop())
    
    # print the values of the nodes in order. does not terminate if the list
    # is circular
    def display(self):
        if self.head is None:
            print("List is empty.")
        else:
            n = self.head
            while n is not None:
                print(n.val, '-->', end=' ')
                n = n.next
            print('|| ({0} items)'.format(self.size))
    
    # insert a node with a given value at the head
    def insert_head(self, value):
        new_head = self.Node(value, self.head)
        self.head = new_head
        self.size += 1
        return self

    # check if empty
    def is_empty(self):
        return self.head is None
        
    # if not empty, remove the head and return it
    def remove_head(self):
        if not self.head is None:
            old_head = self.head
            self.head = self.head.next
            self.size -= 1
            return old_head.val
        
    # insert a node with a given value at the tail
    def insert_tail(self, value):
        new = self.Node(value, None)
        
		# case where list is empty
        cur = self.head
        if cur is None:
            self.head = new
            self.size += 1
            return
        
		# otherwise, traverse until at end
        while cur.next is not None:
            cur = cur.next
        cur.next = new
        self.size += 1
        
    # delete the first node in the list with a 
    # given value, and makes no change if no such node exists
    # runs in O(n) time worst-case as it must traverse the entire list 
    def delete(self, value):
        if self.size == 0:
            return
        
        # check if value is at head
        cur = self.head
        if cur.val == value:
            self.head = cur.next
            self.size -= 1
            return
        
        # otherwise, look through rest of list
        while cur.next is not None:
            if cur.next.val == value:
                cur.next = cur.next.next
                self.size -= 1
                return
            cur = cur.next
        return