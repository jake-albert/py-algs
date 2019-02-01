import sys
sys.path.append('..')
from data_structs import MaxHeap, MinHeap, MyMaxHeap, MyMinHeap
from random import randint

# p03

# Heap Tests: Some tests on the heap implementations.

##############################################################################

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