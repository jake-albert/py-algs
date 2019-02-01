import heapq as hq
from operator import le, ge
from random import randint

# A heap can be implemented in Python using the heapq library, which can 
# "heapify" any Python list of values that can be compared and ordered. The
# resulting heap is a MINHEAP. 

def heapq_examples():

    mylist = []
    hq.heapify(mylist)
    hq.heappush(mylist,5)
    hq.heappush(mylist,22)
    hq.heappush(mylist,7)
    print(mylist[0])                 # Reveals top of heap, as 5.
    hq.heappop(mylist)            # Pops off 5 and now top is 7.
    print(mylist[0])                 # 7.

# I used the heapq library to implement a min-heap and max-heap class, making 
# sure to include the replace method that performs the equivalent of a pop 
# followed by a push, but more efficiently. To create a max-heap, I negate 
# values before storing and returning them, which seems to be standard
# practice given that the heapq library does not support the max-heap 
# property. (Adapted from source: https://tinyurl.com/y9t8aqhu)
    
class MinHeap:
    def __init__(self): self.h = []
    def __len__(self): return len(self.h)
    def is_empty(self): return len(self) == 0
    def peek(self): return self.h[0]
    def push(self,x): hq.heappush(self.h,x)
    def pop(self): return hq.heappop(self.h)
    def replace(self,x): return hq.heapreplace(self.h,x)

class MaxHeap(MinHeap):
    @staticmethod
    def neg(x): return -1*x
    def peek(self): return self.neg(self.h[0])
    def push(self,x): hq.heappush(self.h,self.neg(x))
    def pop(self): return self.neg(hq.heappop(self.h))
    def replace(self,x): return self.neg(hq.heapreplace(self.h,self.neg(x)))
    
# I also implemented a heap wihtout the heapq library using a Python list, 
# making sure to implement not only push and pop, but replace as well.

class MyHeap:
    """ The superclass for MyMinHeap and MyMaxHeap. 
    
    Attributes:
        array: A list. array[0] represents the top of the heap, and 
          for any item at index i, its two children (if they exist) 
          are at indices 2*i+1 (left) and 2*i+2 (right). 
        cmp: A comparator function. By the heap property, holds True 
          for every parent with respect to both of its children. <= 
          for a MinHeap, and >= for a MaxHeap.
    """
    
    def __init__(self,cmp):
        """Inits an empty heap."""
        self.array = []
        self.cmp = cmp
    
    def __len__(self):
        return len(self.array)
    
    def is_empty(self):
        """Returns a Boolean."""
        return len(self) == 0
    
    def peek(self):
        """Returns top value, or None if empty."""
        if self.is_empty():
            return None
        return self.array[0]
    
    def push(self,value):
        """Inserts a new value into the heap.""" 
        
        # We first add the value such that it has the greatest index (a
        # position guaranteed to be the "lowest"), and then swap it up
        # with parent values as far as is appropriate.
    
        self.array.append(value)
        index = len(self.array) - 1
        
        while self._has_parent(index):
            parent_index = self._get_parent(index)
            if not self._heap_property_holds(parent_index,index):
                self._swap(index,parent_index)
                index = parent_index
            else:
                break
    
    def pop(self):
        """Removes and returns the top value from the heap while 
        maintaining the heap property.
        
        Raises:
            IndexError: heap is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot remove value from empty heap.")
        elif len(self) == 1:
            return self.array.pop()
    
        # We save the top value to return later, then move to the top 
        # the value was at highest index ("lowest" position). We then
        # swap this value with children as far down as is appropriate.
    
        return_val = self.array[0]
        self.array[0] = self.array.pop()
        self._send_down_top_val()                
        return return_val

    def replace(self,value):
        """Replaces the top value of the heap with value, and swaps 
        this new value down to ensure that the heap property holds.
        
        Raises:
            IndexError: heap is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot remove value from empty heap.")     
    
        self.array[0] = value
        index = 0        
        self._send_down_top_val()
    
    def _has_parent(self,index):
        """Returns True iff the item at index has a parent."""
        return index > 0
        
    def _get_parent(self,index):
        """Returns the index of the parent to the item at index.""" 
        return (index+1)//2 - 1
        
    def _heap_property_holds(self,parent_index,child_index):
        """Returns a Boolean."""
        return self.cmp(self.array[parent_index],self.array[child_index])
        
    def _swap(self,i1,i2):
        """Swaps the values at indices i1 and i2."""
        self.array[i1], self.array[i2] = self.array[i2], self.array[i1]
    
    def _has_left_child(self,index):
        """Returns True iff index has a left child."""
        return index*2+1 < len(self)
     
    def _has_right_child(self,index):
        """Returns True iff index has a right child."""
        return index*2+2 < len(self) 
     
    def _get_left_child(self,index):
        """Returns index where left child is expected."""
        return index*2+1
        
    def _get_children(self,index):
        """Returns indices where left and right children expected."""
        left_index = self._get_left_child(index)
        right_index = left_index + 1
        return left_index, right_index
    
    def _get_contender(self,index):
        """Returns the index to the child that may legally become a 
        parent to the other. Assumes that the item at index has both a
        left and right child."""
        left_index, right_index = self._get_children(index)
        if self._heap_property_holds(left_index,right_index):
            return left_index 
        else:
            return right_index
           
    def _send_down_top_val(self):
        """Successively swaps the value at the top of the heap to lower
        levels until the heap peroperty is satisfied. Assumes that the
        heap satisfies the heap property except for its top value."""   
        index = 0    
        while self._has_left_child(index):

            # Pick the "strongest" of available children to check that 
            # the heap property holds, and swap if necessary.

            if self._has_right_child(index):                
                contender_index = self._get_contender(index)
            else:
                contender_index = self._get_left_child(index)

            if not self._heap_property_holds(index,contender_index):
                self._swap(index,contender_index)
                index = contender_index
            else:
                break
        
class MyMinHeap(MyHeap):
    """A minheap from scratch. See base class for details."""
    
    def __init__(self):
        """Inits an empty MyMinHeap."""
        super(MyMinHeap,self).__init__(le) 
        
class MyMaxHeap(MyHeap):
    """A maxheap from scratch. See base class for details."""

    def __init__(self):
        """Inits an empty MyMaxHeap."""
        super(MyMaxHeap,self).__init__(ge) 

# One way to test a heap's performance is to insert random integers into it 
# and confirm that they get popped off back in sorted order.

def test():
    """Tests the push and pop methods for the heap classes."""
    test_heap(MaxHeap,True)
    test_heap(MinHeap,False)
    test_heap(MyMaxHeap,True)
    test_heap(MyMinHeap,False)
    
     
def test_heap(heap_class,max_test):
    """Tests the push and pop methods for a single heap class.
    
    Args:
        heap_class: A callable class that creates a heap.
        max_test: True if testing for max heap, False for min heap.
    """
    NVALS = 1000
    MIN_VAL = 1
    MAX_VAL = 1000

    h = heap_class()
    vals = [randint(MIN_VAL,MAX_VAL) for _ in range(NVALS)]
    for val in vals:
        h.push(val)
        
    my_sorted_vals = []
    while not h.is_empty():
        my_sorted_vals.append(h.pop())
     
    assert my_sorted_vals == sorted(vals,reverse=max_test)