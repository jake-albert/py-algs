import sys
sys.path.append('..')
from data_structs import MinHeap, MaxHeap
from random import randint

# c17p20

# Continuous Median: Numbers are randomly generated and passed to a method. 
# Write a program to find and maintain the median value as new values are 
# generated.

##############################################################################

# First, there should be agreement about the meaning of "median". If there are
# an odd number of numbers, an agreed-upon definition of is the "middle" 
# number when the whole group of numbers is sorted. But if there are an even 
# number, should we output the arithmetic average of the two "middle" values, 
# arbitrarily pick one of these values, or return any such number between the 
# two, such that there are an equal number of numbers greater than and less 
# than that number? I am going to assume that the arithmetic average option is
# preferred, and return a float for all inputs for consistency. 

# From the description, it seems that while new values are generated and 
# passed to whatever data structure I use to maintain the median, no values 
# are ever removed. So the data structure must handle two functions: some 
# insertion that adds a newly randomly generated number, and a get_median that
# returns a median. How efficiently can we do both?
 
# A naive but straighforward option is to keep a linked list of items, then 
# insert a new node in the proper, sorted spot for each new number in O(N) 
# time in the worst case, and then keep track of the "middle" node or two
# nodes so as to be able to return the median in O(1) time. 

# Another option is to keep all of the items in a balanced binary search tree
# so that insertion time takes O(logN) and then returning the median still in
# O(N) time with an in-order traversal of the tree. We also might be able to 
# update the median node in the tree upon each insertion at no extra 
# asymptotic cost so that we can return the median in O(1) time, but this 
# seems more complicated than the following option.

# Using heaps seems like the best approach, given their insertion performance
# on par with trees but simpler approach to identifying the median. We can 
# keep the lesser half of the numbers in a max-heap, and the greater half 
# in a min-heap, maintaining a difference of at most 1 between the sizes of 
# each half. We could return the median in O(1) time by returning the average 
# of the "top" of each heap if they are of equal size, or the "top" of the 
# larger heap if the difference is 1. 

# Adding a new number to the collection involves no more than two calls to 
# the O(logN) methods push() or replace() on a heap that is contains roughly
# half of the numbers. O(N) memory is required to store the numbers.

# We can compare to similar tasks to determine if that memory performance is 
# the best we can do. We can update and return the Xth-highest value instead 
# of the median using O(X) space and O(X) memory. For example, the maximum 
# requires no more than O(1) space and O(1) time for every insert. This is 
# because once a number STOPS being the maximum value, it will NEVER be the 
# maximum again (so long as removing values is not permitted). So there is no 
# need to store any values other than the maximum. On the other hand, numbers 
# that stop being the median, or that never were the median since being
# inserted, CAN become a median later depending on which values are inserted 
# after, so we need to keep track of all of them which suggests that we cannot
# beat O(N) memory. 
       
# The below implementaion differs slightly from the above description in that 
# it keeps the two heaps at the same size at all times, storing the median 
# value when there is an odd total in a separate attribute called "mid". This 
# design makes for far cleaner code than when there is no "mid", but it is 
# difficult to determine which implementation makes fewer calls on average to
# the expensive push() or replace() functions on random inputs. Might revisit
# later to test empirically, but asymptotic performance is the same.
      
class MedianKeeper:
    """Class that maintains a median value as numbers are continually
    added to it. Each insertion takes O(logN) time, and returning the 
    median takes O(1) time. Requires O(N) space.
    
    Attributes:
        lower: A MaxHeap instance. Stores the lower half of values.
        higher: A MinHeap instance. Stores the higher half of values.
        mid: An int or float when there are an odd number of numbers 
          stored, and None otherwise.
        median: A float when MedianKeeper is non-empty, None otherwise.
    """
    
    def __init__(self):
        """Inits an empty MedianKeeper."""
        self.lower = MaxHeap()
        self.upper = MinHeap()
        self.mid = None
    
    def _is_empty(self):
        """Returns a Boolean."""
        
        # Always inserts to lower first, so need to check higher.
        
        return len(self.lower) == 0 and self.mid is None
    
    @property
    def median(self):
        """Returns the median of the inserted values in O(1) time."""
        if self._is_empty():
            return None
        elif self.mid is None:
            return (self.lower.peek()+self.upper.peek()) / 2
        else:
            return float(self.mid)
            
    def insert(self,x):
        """Inserts x in O(logN) time."""
        
        # Very first value inserted becomes the middle value.
        
        if self._is_empty():
            self.mid = x
        
        # When there are an even number of values stored, some value 
        # must be found to go to the middle value. In the best case, 
        # the value is inserted between the two halves in O(1) time. 
        # Otherwise, one call to replace() takes O(logN) time.
        
        elif self.mid is None:
            if x > self.upper.peek():
                self.mid = self.upper.replace(x)
            elif x < self.lower.peek():
                self.mid = self.lower.replace(x)
            else:
                self.mid = x
        
        # When there are an odd number of values stored, both x and the
        # current middle value must be placed in opposite halves. 
        # Always requires two calls to the O(logN) push() method.
        
        else:
            if x <= self.mid:
                takes_x, takes_m = (self.lower,self.upper) 
            else:
                takes_x, takes_m =(self.upper,self.lower)
            takes_x.push(x)
            takes_m.push(self.mid)
            self.mid = None
    
# I test for correctness using an even more straighforward (and slow) solution
# than even the naive solution offered above: maintain a list of numbers, and
# upon each insertion append that number to the end and sort the entire list.
# This requires O(NlogN) time per insertion and would not be wise to use for 
# large sets of numbers, but it is simple to write up. 
    
class SlowMedianKeeper:
    """Inefficient but guaranteed correct MedianKeeper class.
    
    Attributes:
        array: A list.
    """
    
    def __init__(self):
        """Inits an empty SlowMedianKeeper."""
        self.array = []
        
    @property
    def median(self):
        """Evaluates and returns the median as a float."""
        if len(self.array) == 0:
            return None
        elif len(self.array) % 2 == 0:
            mid_ind_left = len(self.array)//2
            return (self.array[mid_ind_left]+self.array[mid_ind_left-1]) / 2
        else:
            return float(self.array[len(self.array)//2])
    
    def insert(self,x):
        """Appends x to the list and sorts the list."""
        self.array.append(x)
        self.array.sort()
        
def test(n):
    """Inserts n random integers into both a MedianKeeper and a 
    SlowMedianKeeper instance, verifying at each insertion that both 
    return the same value as median."""
    MIN_VAL = 1
    MAX_VAL = 1000
    
    slow_keeper, fast_keeper = SlowMedianKeeper(), MedianKeeper()
    
    for _ in range(n):
        val = randint(MIN_VAL,MAX_VAL)     
        slow_keeper.insert(val)
        fast_keeper.insert(val)
        assert slow_keeper.median == fast_keeper.median