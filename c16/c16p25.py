import sys
sys.path.append('..')
from data_structs import Doubly

# c16p25

# LRU Cache: Design and build a "least recently used" cache, which evicts the
# least recently used item. The cache should map from keys to values (allowing
# you to insert and retrieve a value associated with a particular key) and be 
# initialized with a max size. When it is full, it should evict the least
# recently used item. 

##############################################################################

# I use both a linked list and hash table. The list holds key-value pairs, 
# with the most recently used item at the head and the least so at the tail,
# and the hash table gives us O(1) access to the node in the list that matches
# the key. There is a redundancy in that keys are stored in both the hash
# table and the linked list. This is because upon evicting a least recently 
# used node from the list, we must also locate they key to delete from the 
# hash table so that the hash table's size remains capped at max size as well.

# I had to decide how to handle a case of inserting a key-value pair whose key
# alrady exists in the cache. I chose that this cache simpy reassigns the
# value, but also that this counts as a "use" just like retrieval and thus 
# results in the item being placed at the head of the doubly-linked list.

class MyCache:
    """A 'least recently used' cache.
    
    Attributes:
        size: An integer. The current number of items in the cache.
        maxsize: An integer. The capacity of the cache.
        chain: A Doubly linked list instance.
        lookup: A dictionary mapping keys to nodes in the linked list.
    """

    def __init__(self,maxsize):
        """Inits empty MyCache instance. Maxsize specified by user."""
        self.size = 0
        self.maxsize = maxsize
        self.chain = Doubly()
        self.lookup = {}
        
    def insert(self,key,value):
        """Inserts (key,value) pair into the cache.
        
        If key already matches an item in the cache, replaces the old
        value with the new. If cache is at full capacity, evicts the 
        least recently used item to make room for the new. Always 
        returns with the item at the head of the linked list as the 
        most recently used item.
        """
        
        if key in self.lookup:
            self.chain.move_to_head(self.lookup[key])
            self.lookup[key].val[1] = value
        
        else:
        
            if self.size == self.maxsize:
                lru_pair = self.chain.remove_tail() # (key,value)
                del self.lookup[lru_pair[0]]
                self.size -= 1
        
            node = self.chain.insert_head([key,value])
            self.lookup[key] = node
            self.size += 1
    
    def retrieve(self,key):
        """If some key exists in the cache, returns the value. 
        Otherwise, returns None.
        """
        if key in self.lookup:
            self.chain.move_to_head(self.lookup[key])
            return self.lookup[key].val[1]
        
    def display(self):
        """Prints size information and displays the linked list."""
        room_left = self.maxsize-self.size
        print(f"{self.size} slots filled. {room_left} under capacity")
        self.chain.display()
        
def test():
    """Tests a toy example."""
    test_cache = MyCache(3)
    
    test_cache.insert("ATL","Atlanta")
    test_cache.insert("IAH","Houston")
    print(test_cache.retrieve("IAH"))  # "ATL" is now LRU. 
    
    test_cache.insert("DTW","Detroit")
    test_cache.insert("PDX","Portland")  # "ATL" is now evicted.   
    print(test_cache.retrieve("ATL"))  # Should print None.
    
    print(test_cache.retrieve("PDX"))  # "IAH" is still LRU.
    test_cache.insert("IAH","HOUSTON")  # "DTW" is now LRU.
    print(test_cache.retrieve("DTW"))  # "PDX" is now LRU.
    test_cache.insert("TPA","Tampa")  # "PDX" is now evicted.
    print(test_cache.retrieve("PDX"))  # Should print None.
    
    test_cache.display()