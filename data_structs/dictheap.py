from .heap import MyHeap
from operator import le, ge

# A special data structure I designed for c17p18. 

# Say that we must maintain the names of many people. Each person has some
# associated number, and we need to be able to return in O(1) time the name of
# whichever person has the lowest number. Storing the people in a min heap 
# with their numbers as a comparison key seems like the best approach, but 
# there is a catch. Any person's number can change at any time. It can 
# increase or decrease by any amount, and we are informed of these changes by
# a stream of updates:

# >>> John's new number is 24.
# >>> Marcia's new number is 33.
# >>> Teresa's new number is 277.
# >>> Nia's new number is 78.
# >>> Nia's new number is 22.
# >>> John's new number is 88.
# >>> Nia's new number is 691.
# >>> John's new number is 80.
# >>> ...

# A dictheap acts like both a dictionary and a heap. The dictionary
# functionality of a dictheap allows us to find any element stored in O(1) 
# time, while the heap functionality ensures that the heap property is
# maintained in O(logN) time after any updates are made.

# Here, the word "key" can mean 1) the role that an element (a person's name 
# in the above example) plays when we get its associated value (the number)
# using the the dictionary, and 2) the role this associated value plays as the 
# object of comparison operations within the heap. To disambiguate these 
# meanings, I use the word "heap_key" for meaning #2.

# The dictheap does not store duplicate elements; it interprets any attempt 
# to push an element/heap_key pair onto the heap when an element is already 
# in the list as an attempt to reassign the heap_key to that element. 

class DictHeapItem:
    """The objects stored in a dictheap.
    
    Attributes:
        element: Any hashable object (ints, strings, Python object 
          instances, tuples....).
        heap_key: Any object that can supports comparison operations.
    """
    
    def __init__(self,element,heap_key):
        self.element = element
        self.heap_key = heap_key

    def __le__(self,other):
        return le(self.heap_key,other.heap_key)
        
    def __ge__(self,other):
        return ge(self.heap_key,other.heap_key)
            
class DictHeap(MyHeap):
    """The superclass for MinDictHeap and MaxDictHeap. Inherits from 
    MyHeap which supports standard heap push, pop, replace, and peek.
    
    Attributes:
        array: A list. array[0] represents the top of the heap, and for
          any item at index i, its two children (if they exist) are at 
          indices 2*i+1 (left) and 2*i+2 (right). 
        cmp: A comparator function. By the heap property, holds True 
          for every parent with respect to both of its children. <= 
          for a MinHeap, and >= for a MaxHeap.
        element_to_index: A dictionary that maps element objects as 
          keys to the index in array where that element can be found.
    """
    
    def __init__(self,cmp):
        """Inits an empty dictheap."""
        self.array = []
        self.cmp = cmp
        self.element_to_index = {}
    
    def __contains__(self,lookup):
        """Returns True iff an element is stored somewhere in array."""
        return lookup in self.element_to_index
    
    def push(self,element,heap_key):
        """If element is not in dictheap, inserts a new DictHeapItem.
        Otherwise, updates the heap_key to the element.""" 
        if element in self:
            self.replace_heap_key(element,heap_key)
        
        self._reassign_item_at(len(self.array),element,heap_key)
        self._send_up_end_val()

    def pop(self):
        """Removes and returns the top DictHeapItem on the heap.
        
        Raises:
            IndexError: heap is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot remove value from empty heap.")
        elif len(self) == 1:
            del self.element_to_index[self.array[0]]
            return self.array.pop()
    
        return_item = self.array[0]
        del self.element_to_index[return_item.element]
        self._reassign_item_at(0,self.array.pop())
        self._send_down_top_val()
                
        return return_item

    def replace(self,element,index):
        """Replaces the top DictHeapItem of the heap with a new one, 
        and swaps this new value down to ensure that the heap property
        holds.
        
        Raises:
            IndexError: heap is empty.
        """
        if self.is_empty():
            raise Exception("Cannot remove tuple from empty heap.")     
    
        del self.element_to_index[self.array[0].element]
        self._reassign_item_at(0,element,index)
        self._send_down_top_val()
     
    def replace_heap_key(self,element,heap_key):
        """Given an element assumed to be in the dictheap, assigns it 
        a new heap_key and swaps through heap as much as is required 
        to maintain heap property.
        
        Raises:
            KeyError: element is not in dictheap.
        """
        index = self.element_to_index[element]
        
        if heap_key < self.array[index].heap_key:
            self.array[index] = DictHeapItem(element,heap_key)
            self._send_up_val(index)
        
        elif heap_key > self.array[index].heap_key:
            self.array[index] = DictHeapItem(element,heap_key)
            self._send_down_val(index)
            
    def _swap(self,i1,i2):
        """Swaps two elements' positions in array, and the resulting
        indices in the dictionary. Overwrites bass class _swap method.
        
        Args:
            i1,i2: Int indices to elements in array.
            
        Raises:
            IndexError: i1 or i2 is out of range.
        """
        item1,item2 = self.array[i1],self.array[i2]        
        self.array[i1], self.array[i2] = item2,item1
        
        self.element_to_index[item2.element] = i1
        self.element_to_index[item1.element] = i2
        
    def _reassign_item_at(self,i,element,heap_key):
        """Sets the DictHeapItem at index i in the array to have new 
        element and heap_key, and updates the dictionary.
        
        Raises:
            IndexError: i is out of range.
        """       
        new_item = DictHeapItem(element,heap_key)
        
        if i == len(self.array):
            self.array.append(new_item)
        else:
            self.array[i] = new_item
        
        self.element_to_index[element] = i    
        
class MinDictHeap(DictHeap):
    """A min dictheap. See base class for details."""
    
    def __init__(self):
        """Inits an empty MinDictHeap."""
        super(MinDictHeap,self).__init__(le) 
        
class MaxDictHeap(DictHeap):
    """A max dictheap. See base class for details."""
    
    def __init__(self):
        """Inits an empty MaxDictHeap."""
        super(MaxDictHeap,self).__init__(ge) 