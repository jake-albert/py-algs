# start

# we use a linked list/hash table pairing. the list holds key-value pairs, and 
# the hash table gives us O(1) access to a node in the list referenced by the 
# key. There is a redundancy in that keys are stored in both the hash table
# and the linked list, since we need to be able to find the hash table place 
# to delete it.

from doubly import Doubly

class MyCache:

    def __init__(self,maxsize):
        self.size    = 0
        self.maxsize = maxsize
        self.chain   = Doubly()
        self.lookup  = {}
        
    def insert(self,key,value):
        
        # first check if we are replacing a value or not
        if key in self.lookup:
            self.chain.move_to_head(self.lookup[key])
            self.lookup[key].val[1] = value
        
        # if replacing a value, then the size increases by one
        else:
        
            # first remove if necessary the least recently used value
            if self.size == self.maxsize:
                lru_pair = self.chain.remove_tail()
                del self.lookup[lru_pair[0]]
                self.size -= 1
            
            # regardless, add a new node with key value pair to the head
            node = self.chain.insert_head([key,value])
            self.lookup[key] = node
            self.size += 1
    
    def retrieve(self,key):
    
        # make changes only if the key is in the lookup table
        if key in self.lookup:
            self.chain.move_to_head(self.lookup[key])
            return self.lookup[key].val[1]
        
    def display(self):
    
        print("{} slots filled. {} under capacity".format(self.size,self.maxsize-self.size))
        self.chain.display()