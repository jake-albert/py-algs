import sys
sys.path.append('..')
from data_structs import MinDictHeap
from random import shuffle, randint

# c17p18

# Shortest Supersequence:  You are given two arrays, one shorter (with all
# distinct elements) and one longer. Find the shortest subarray in the longer
# array that contains all the elements in the shorter array. The items can 
# appear in any order.
#
# EXAMPLE
# Input {1, 5, 9} | {7, 5, 9, 0, 2, 1, 3, 5, 7, 9, 1, 1, 5, 8, 8, 9, 7}
#                                         ¯¯¯¯¯¯¯¯¯¯ 
# Output: [7, 10] (the underlined portion above)

##############################################################################

# Say that N is the length of the longer list, and M is the length of the 
# shorter list.

# The most brute-force option is to check in each of the O(N^2) subarrays of 
# the longer sequence for the supersequence property. If no information is 
# shared between checks, each subarray can be checked in O(N) time while a 
# running minimum supersequence value is kept, leading to O(M+N^3) total 
# runtime. (M is from hashing each of the elements in the shorter list for O(1)
# membership checks.) A better option is to, for all of the subarrays that 
# start at some index i, move forward through the list from i until all
# elements in the shorter subarray have been seen to find the shortest 
# supersequence that begins at i. Doing this for all i while keeping track of 
# only the global shortest supersequence takes O(M+N^2) time and O(M) space.

# The optimized approach below takes advantage of the fact that if we know the
# shortest subsequence that ENDS at i for all i up to the index x-1, then we
# can easily determine the shortest supersequence that ends at x, provided we
# have some extra information available.

# For example, on the example input, where shorter is [1,5,9] and longer is:

#  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
#  --------------------------------------------------- 
#  7  5  9  0  2  1  3  5  7  9  1  1  5  8  8  9  7

# We know that a for each "next" index x to the right of index x-1, the 
# shortest supersequence ending at x will be shorter than the one ending at 
# x-1 in just ONE case. Say we know that the shortest supersequence ending at 
# index 5 is [5,9,0,2,1]. The shortest ending at 6 is simply that same 
# subarray with longer[6], or 3, appended at the end, but this is longer than 
# before and not worth tracking. 3 is not in shorter, so what is the use? 
# In fact, even if this value were a 1 or a 9, the shortest supersequence 
# ending at index 6 only gets longer, because we still need the 5 at index 1.

# In contrast, the shortest supersequence ending at index 10 DOES improve on 
# the shortest ending at 9, [1,3,5,7,9]. longer[10] is 1, which is the 
# earliest element from shorter that appears in the supersequence ending at 9,
# and "replacing" it with the one at index 10 results in a subarray [5,7,9,1].
# If this value at longer[10] were a DIFFERENT element in shorter, then there 
# would not be any improvement, as we would still need that 1 from longer[5].

# As we traverse through longer, then, we must keep track of, for each element
# S in shorter, the index of its MOST RECENT position; that is, the largest 
# index j <= the current index in longer for which longer[j] is S. This
# requires updating an element's most recent position to the current index 
# whenever we find another occurrence of that element in longer. 

# Before the update, though, we look at those most recent positions for each 
# S and check whether or not the current value in longer matches the LEAST 
# RECENT of these most recent positions, and "replace" that element with the
# one at current if there is a match, like when going from index 9 to index 10
# in the above example. If the resulting supersequence is shorter than we have
# seen before, we store that as the new shortest supersequence. 

# How long one of these steps takes depends on the data structure we use to 
# track that information. We can update the most recent indices for elements
# in shorter in O(1) at each new index if we keep them in a dictionary, but
# finding the least of these values at each step would require traversing
# through the full dictionary in O(M). This would lead to a total runtime of 
# O(N*M), which might be acceptable when that M is expected to be small.

# On the other hand, it seems that keeping indices in a heap structure could 
# be helpful given that it maintains minimums over inserting new elements in 
# O(logM) time, but what about modifying elements within the heap, as we will 
# need to do in this problem? I wrote a special data structure for this 
# problem that I call a "dictheap" that combines the best features of both a 
# dictionary and a heap. A dictheap has both A) n list that preserves the heap
# property, and B) a dictionary that maps keys to indices in the list where 
# the values to that key are stored.

# At each step, then, we are able to 1) check the minimum value in the
# dictheap (which represents the least recent among the most recent 
# occurrences of each element in shorter) to see whether or not the value at 
# the current index in longer can replace it, and 2) if the current index 
# matches any element in S, reassign its most recent index within the dictheap
# while maintaining the heap property in O(logM) time. So total runtime is 
# O(NlogM+M), with O(M) space needed for the dictheap. 

# When there are multiple shortest supersequences in the input, I assume that
# returning only one is acceptable.
        
def f1(shorter,longer):
    """Finds a shortest supersequence of shorter in longer.
    
    Args:
        shorter, longer: Lists of any objects that support the equality
          operation, such as ints or strings.
          
    Returns:
        A tuple of the start and end indices in longer of the 
          supersequence, or None if no such supersequence exists.
    """
    
    # If longer is empty, then there is no supersequence. If longer is 
    # not empty but shorter is, then any subarray is trivially a 
    # supersequence, so we arbitrarily return the subarray with only 
    # the first element to return.
    
    if len(longer) == 0:
        return None
    if len(shorter) == 0:
        return (0,0)
        
    start_i, recent_heap = preprocess(shorter,longer)
        
    if start_i == len(longer):  # True iff no supersequence exists.
        return None
        
    # If a supersequence exists, start_i is the lowest index at which 
    # one ends, and the SHORTEST that ends there starts at the least 
    # recent of the most recent occurrences of elements in shorter.
    
    bestsub = (recent_heap.peek().heap_key,start_i)
    
    for i in range(start_i+1,len(longer)):    
    
        if longer[i] not in recent_heap:  # True iff not in shorter.
            continue
        
        # Store the least recent element in shorter before updating
        # the dictheap, which might change this value. 
        
        least_recent_element = recent_heap.peek().element
        recent_heap.replace_heap_key(longer[i],i)
        
        # New supersequence ending at i has a chance of being an
        # improvement iff longer[i] would replace the least recent
        # element in shorter.
        
        if longer[i] == least_recent_element:  
            
            least_recent_index = recent_heap.peek().heap_key
            if (i-least_recent_index) < (bestsub[1]-bestsub[0]):
                bestsub = (least_recent_index,i) 
                
    return bestsub
         
def preprocess(shorter,longer):
    """Identifies the lowest index i in longer such that there is a 
    supersequence of shorter ending at i. In addition, returns a 
    dictheap that stores the greatest indices <= i at which each 
    element in shorter is stored.

    For example, if longer is [1,1,9,6,1,5,7,9,1,5,5] and shorter is
    [1,5,9], then i is found to be 5, and the indices are 4 for "1", 
    5 for "5", and 2 for "9".

    Args:
        shorter, longer: Lists of objects that support equality tests.
        
    Returns:
        An int, and a MinDictHeap instance.
    """
    
    # Update the indices for each element in shorter using a dictionary 
    # so as to minimize calls to the O(logM) heap functions.

    most_recent = {}
    shorter_set = set(shorter)
    
    i = 0
    while i < len(longer):
    
        if longer[i] in shorter_set:
            most_recent[longer[i]] = i
            
        if len(most_recent) == len(shorter):
            break
    
        i += 1
        
    recent_heap = MinDictHeap()
    for element,index in most_recent.items():
        recent_heap.push(element,index)

    return i,recent_heap

def f2(shorter,longer):
    """O(M+N^2) somewhat brute-force version for testing. See f1."""
    
    # If longer is empty, then there is no supersequence. If longer is 
    # not empty but shorter is, then any subarray is trivially a 
    # supersequence, so we arbitrarily return the subarray with only 
    # the first element to return.
    
    if len(longer) == 0:
        return None
    if len(shorter) == 0:
        return (0,0)
    
    bestsub = None
    
    for start_i in range(len(longer)):
        shorter_set = set(shorter)    
        
        for end_j in range(start_i,len(longer)):
            if longer[end_j] in shorter_set:
                shorter_set.remove(longer[end_j])
                
                # Whenever all elements in shorter have been found, we
                # have found the shortest supersequence that begins at
                # start_i, so update bestsub if possible and move on.
                
                if len(shorter_set) == 0:  
                    if bestsub is None:
                        bestsub = (start_i,end_j)
                    elif (end_j-start_i) < (bestsub[1]-bestsub[0]):
                        bestsub = (start_i,end_j)
                    break
                    
    return bestsub    

def test(digits,trials):
    """Tests f1 against f2 over randomly generated inputs.
    
    In each trial, creates a "longer" list that consists of a randomly
    generated number of occurrences of every integer from 0 to digits, 
    then shuffles before calling both f1 and f2 on it and "shorter" 
    lists of arbitrary lengths.
    
    f1 is deemed correct if its output is a supersequence whose length 
    matches the length of the supersequence from f2.
    
    Args:
        digits: An non-negative int.
        trials: A non-negative int.
        
    Raises:
        AssertionError:
    """
    MIN_OCC, MAX_OCC = 2, 20
    
    for trial in range(trials):
        
        if trials > 100 and trial % (trials // 100) == 0:
            p = 100.0 * trial / trials
            print(f"Trial {trial} of {trials}. ({p}%)")
        
        longer = []
        for digit in range(digits+1):
            for _ in range(randint(MIN_OCC,MAX_OCC)):
                longer.append(digit)        
        shuffle(longer)
        
        shorters = [list(range(digits))[:x] for x in [3,4,5,15]]
        
        for shorter in shorters:
            a1,a2 = f1(shorter,longer),f2(shorter,longer)
            assert is_supersequence(shorter,longer,a1)
            assert is_supersequence(shorter,longer,a2)
            assert (a1 is None and a2 is None) or (a1[1]-a1[0] == a2[1]-a2[0])
            
def is_supersequence(shorter,longer,a):
    """Returns a Boolean. a is a tuple of inclusive indices."""
    shorter_set = set(shorter)
    for i in range(a[0],a[1]+1):
        if longer[i] in shorter_set:
            shorter_set.remove(longer[i])
    return len(shorter_set) == 0