import sys
sys.path.append('..')
from data_structs import MyMinHeap, MyMaxHeap
from operator import gt, lt
from collections import Counter
from random import randint, shuffle

# c17p14

# Smallest K: Design an algorithm to find the smallest K numbers in an array.

##############################################################################

# I assume here that we are working with only int type numbers in the input.
# I also assume that when K is larger than the number of numbers in the list,
# we raise an exception rather than, say, return all elements in the list.

# Another important question is: if the input has duplicate elements, are we
# to return the smallest K unique numbers in an array, or count duplicates
# separately? I assume for this problem that we are to do the SECOND option;
# that is, for input K=3 on list [1,1,2,3,4,5], the input should be some 
# permutation of [1,1,2], NOT [1,2,3].

# I assume that we cannot make any assumptions about the bounds of values in 
# the list. If we could (for instance, if we knew only integers from 1 to 100
# could possibly be in the list), then we could perform a bucket sort in O(N)
# time, then iterate through the first K numbers in the sorted list in O(K) 
# time. Without such an assumption, we also could perform a sort like merge
# sort in O(NlogN) time. 

# But we likely should be able to do better than this, given that there is no 
# requirement for the K smallest numbers to be themselves sorted when we 
# return them.

# One option is to keep a max heap that has a size limit of K. We could insert
# into this heap the list's first K elements, and then for each of the
# remaining N-K numbers, replace it with the top value in the heap iff less 
# than that top value. If the heap is implemented with a Python list (as
# below), we need only return that list, or a copy of it.

# A single insertion or replacement in a max heap with max size of K takes 
# O(logK) time, so we can expect the above algorithm to run in O(NlogK) time, 
# which improves on a normal O(NlogN) sort especially wen K is much smaller 
# than N. As an additional improvement, we could use a min heap with max size 
# N-K when K is greater than half of N to find the values to exclude from the 
# list, though this does not change asymptotic performance.

# O(K) space is required for the heap. 

def f1(lst,k):
    """Returns a list of the smallest k numbers in a list in O(NlogK)
    time and O(K) space.
    
    Args:
        lst: A list of ints.
    
    Returns:
        A list of k ints.
        
    Raises:
        ValueError: k is negative or greater than the length of lst.
    """
    if k < 0:
        raise ValueError(f"{k} is negative.")
    elif k > len(lst):
        raise ValueError(f"{k} is larger than length of input list.")
    elif k == 0:
        return []
    elif k == len(lst):
        return lst[:]
    
    # Determine whether the heap will find the K smallest numbers or
    # the N - K largest numbers.    
    
    if k <= len(lst) // 2:       
        size_limit = k
        k_heap = MyMaxHeap()
        cmp = lt
        to_exclude = False        
    else:      
        size_limit = len(lst) - k
        k_heap = MyMinHeap()
        cmp = gt
        to_exclude = True 
    
    # Push numbers onto the heap until its size is the desired value. 
    # Replace the top of the heap afterwards only if appropriate.
    
    for x in lst:
            
        if len(k_heap) < size_limit:
            k_heap.push(x)                
        else:
            if cmp(x,k_heap.peek()):
                k_heap.replace(x)

    return exclude(lst,k_heap.array[:]) if to_exclude else k_heap.array[:]
              
def exclude(lst,exclude_lst):
    """Returns a list of all numbers in lst whose counts have been
    decremented by all counts of numbers in exclude_lst.
    
    Minimum count for any number is 0.
    
    >>> exclude([1,2,1,1,3],[1,7,1,2])
    [1,3]
    
    Args:
        lst, exclude_lst: Lists of ints.
    """
    return list((Counter(lst) - Counter(exclude_lst)).elements())       
                    
# A faster approach to this problem takes advantage of the ability to 
# partition a list in O(N) time into two sublists -- one "left" portion whose
# numbers are all less than or equal to some pivot, and a "right" portion
# whose numbers are all greater than some pivot. This is the same ability
# Quicksort takes advantage of. (But I use a slightly different, "fuzzy" 
# definition for the partitioning index, but we will see why soon.)

def hoare_partition(A,lo,hi):
    """My variant of Tony Hoare's partition scheme. 
    
    Selects the number at the median index of a list A as a pivot, and
    modifies A such that for some index i, all numbers in A[lo:i] are 
    less than or equal to the pivot, and all numbers in A[i:hi+1] are
    greater than or equal to the pivot.
    
    Args:
        A: A list of ints.
        lo, hi: Int indices to A.
    
    Returns:
        The index i with the above property.
        
    Raises:
        IndexError: At least one of lo or hi is out of range of A.
    """
    piv = A[(lo+hi)//2]
    
    while True:
        
        # "Pinch" lo and hi inwards until both indices are on numbers 
        # that must be swapped, then swap and "pinch" once more.
        
        while A[lo] < piv: lo += 1
        while A[hi] > piv: hi -= 1
            
        if lo > hi:
            return lo
            
        A[lo], A[hi] = A[hi], A[lo]
        lo += 1
        hi -= 1

# Say we partition a list over some arbitrary pivot and see an index of X 
# returned as a result. If X is exactly equal to K, then we can immediately 
# return the numbers indexed from 0 to X-1 inclusive, because they are 
# guaranteed to be less than or equal to all other numbers in the list and 
# thus must be the K smallest values.

# On the other hand, if X is less than K, than we must partition the sublist
# from X to the end of the list in order to find the K-X smallest values that
# have still not been identified.

# Finally, if X is greater than K, we partition the sublist from 0 to X-1 
# inclusive in order to "weed out" the X-K largest values among the X found.

def f2(lst,k):
    """See f1 docstring. Runs in O(N) time and O(1) space."""
    if k < 0:
        raise ValueError(f"{k} is negative.")
    elif k > len(lst):
        raise ValueError(f"{k} is larger than length of input list.")
    elif k == len(lst):
        return lst[:]

    lo, hi = 0, len(lst)-1
   
    while True:
        
        split_index = hoare_partition(lst,lo,hi)

        if split_index == k:
            break      
        elif split_index < k:
            lo = split_index
        else:
            hi = split_index-1
    
    return lst[:split_index]

# This function DOES modify the list in order to operate in only O(1) space
# (except for its copying of the correct values in O(K) space, but we can also
# simply return the correct index rather than copy the K elements if need be.)
# If for whatever reason this is not permitted, we should copy the list first 
# using O(N) space. 
  
# Time requirements depend on the nature of the partition scheme we use. If on
# every input we "narrow" our window by only one index, then the algorithm
# takes O(N^2) time, but on average we expect to "narrow" the window by about
# half, and do not need to process the other half each time, so average 
# runtime is O(N+N/2+N/4...) which is in O(N).
  
# It might be apparent now why I wrote a "fuzzy" partition as opposed to the 
# "sharp" partition used normally -- there might be duplicate numbers in the
# input. A "sharp" partition on some input with duplicate values below:

# [5,5,1,1,1,4,5,1,1,4,1,1,1,4,4,1,1,5]  # Pivot is 1.
# [1,1,1,1,1,1,1,1,1,1,5,4,4,5,5,4,4,5]  # Returned index is 10 (the "5").

# No partition of the sublist from 0 to 9 would ever yield an index like 4 or
# 6, so we would need some extra logic to handle spans of identical values. 
# The book's solution uses a special partition that divides the input into 3 
# groups rather than 2 in order to isolate all values equal to the pivot. On 
# the other hand, the fuzzy partition allows for variable numbers of duplicate
# values to be on the left and right of the partition index, and on inputs 
# with large numbers of duplicates tends to return indices in the middle of 
# those spans as opposed to an index at the end, helping identify K quickly.

# The code is thus far simpler than it would be otherwise, but I might revisit
# later to think about what kinds of inputs each approach runs faster on.

def hoare_partition_strict(A,lo,hi):
    """An example of a "strict" partition scheme.
    
    Adapted from the book's solution. Returns the index i such that
    A[:i] contains only numbers less than or equal to the pivot, and
    such that A[:i] contains only numbers strictly greater than the 
    pivot. If ALL numbers were less than or equal to the pivot, then i
    is thus returned as len(A), which causes f2 -- designed for the 
    fuzzy partition scheme -- to enter an infinite loop. 
    """
    def swap(i,j):
        A[i], A[j] = A[j], A[i]

    piv = A[(lo+hi)//2]
    
    while lo <= hi:
    
        if A[lo] > piv:  # A value that must be in upper part.
            swap(lo,hi)
            hi -= 1
        elif A[hi] <= piv:  # A value that must be in lower part.
            swap(lo,hi)
            lo += 1
        else:
            lo += 1
            hi -= 1
    
    return lo
    
# From testing it became clear that, unsurprisingly, f2 is faster than f1. The
# below function tests both and does not time them separately.  
   
def test(trials):
    """Tests f2, f1 against sort-based solution over random inputs."""
    lst_len = 50
    max_int = 100

    for trial in range(trials):
        
        lst = [randint(1,max_int) for _ in range(lst_len)]
        
        sorted_list = sorted(lst)
        shuffle(lst)
        ans = Counter()
        
        # For each k value, add the next number in the sorted list into
        # the Counter object to derive the correct answer.
        
        for k in range(1,len(lst)):
            ans[sorted_list[k-1]] += 1
            assert Counter(f1(lst,k)) == ans
            assert Counter(f2(lst,k)) == ans