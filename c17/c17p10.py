from collections import Counter

# c17p10

# Majority Element: A majority element is an element that makes up more than
# half of the items in an array. Given a positive integers array, find the 
# majority element. If there is no majority element, return -1. Do this in
# O(N) time and 0(1) space.
# 
# EXAMPLE
# Input: 1 2 5 9 5 9 5 5 5
# Output: 5 

##############################################################################

# One question is how to handle an empty list as input. I assume that an empty
# list has no majority element, so I return -1.

# Using only O(1) space forbids us from taking the most obvious approach: 
# counting (and thus storing) the number of instances of each element and then 
# determining if any such counts exceed half the length of the list:

def f1(lst):
    """Returns the majority element of a list or -1 if there is none.
    Runs in O(N) time and requires O(N) space.

    Args:
        lst: A list of positive integers.
        
    Returns:
        An int.
    """
    count_to_beat, counter = len(lst)//2, Counter()
    
    for item in lst:
        counter[item] += 1
        if counter[item] > count_to_beat:
            return item
            
    return -1

# When we cannot store information for each of the possible O(N) unique 
# elements in the input, we must pick some constant number of elements to 
# track at a time. Since N can get arbitrarily large, there is not much that
# storing info on 3 or 4 elements would do to help that storing info on just 
# 1 element could not, so we go with 1.

# The most straightforward way to find a majority element using only O(1)
# space would be to, for each index in the list, pick the item at that index
# to track and take O(N) time to count its occurrences in the entire list
# (terminating early if we ever exceed half the list length). But this
# obviously takes O(N^2) time in the worst case where we scan the list fully
# once for each element.
    
# My first attempt to improve on this solution does improve average runtime 
# but unfortunately is not guaranteed to run in O(N) time on every input. We
# correctly take advantage of the fact that when counting instances of some 
# number, moving forward through the list from the first instance of that
# number that we counted, there is no need to continue counting once this 
# number is no longer in the majority. For example, with input:

#                     [ 1, 2, 5, 2, 2, 3, 2, 7, 9, 2, 2, 2]
#                                ^              !

# When we are counting 2's starting at the caret, we should stop counting at 
# the exclamation point, where the 2's for the first time are not the majority
# element. If 2 is a majority element (and it is), then counting forward from 
# some index (and looping around back to index 0 if we hit the end) will show 
# that 2 is a majority element.

def f2(lst):
    """See f1 docstring. Needs O(N^2) time worst-case, O(1) space."""
    count_to_beat = len(lst)//2  # Regardless of whether odd or even #.
        
    for i in range(len(lst)):

        # Begin counting at each index i, but exit early when possible.
    
        val_count, oth_count = 1, 0
        j = increment_by_one(i,len(lst))
        while val_count > oth_count:
                        
            if lst[j] == lst[i]:
                val_count += 1
            else:
                oth_count += 1
                
            if val_count > count_to_beat:
                return lst[i]
            
            j = increment_by_one(j,len(lst))

    return -1

def increment_by_one(index,length):
    """Increments an index by 1, wrapping around to 0 if needed."""
    return 0 if index >= length-1 else index+1
        
# Given an input like one that consists of N/2 5's and then N/1 8's, we see
# that f2 still runs in O(N^2) time. If the input is [5,5,5,5,8,8,8,8], for 
# instance, we see that f2 checks from index 0 to the end of the list, then 
# from index 1 to the second to last element in the list, and so on. To be 
# sure, it improves on the original idea's runtime in many inputs because it 
# exits early from some searches, but asymptotic behavior is the same.
 
# The issue is that when we "rule out" some instance of an element by finding  
# that it no longer makes up more than half of elements in the sublist we have
# (and finding that this is the case as soon as possible -- in other words, 
# when the count of "others" matches the count of the element) all of those 
# elements are part of some sublist with an even number of elements, none of 
# which are majority elements of that sublist:

# [..., 3, 4, ...]
# [..., 7, 7, 5, 6, ...]
# [..., 6, 6, 4, 6, 9, 4, ...]
# [..., 1, 1, 1, 5, 5, 5, ...]

# In fact, scanning the list once in O(N) time in this way divides it into
# consecutive sublists with even numbers of elements, none of which are
# majority elements of that sublist. Only the FINAL sublist might have a 
# majority element, given that we continue searching the "same" sublist as 
# long as its first element is a majority within it:

#                               Ex. A                              NO
#         |             |                   |                   | 
# [ 3, 4, | 3, 3, 5, 6, | 3, 3, 4, 3, 6, 4, | 3, 3, 3, 5, 5, 5, | 3, 5] 
#         |             |                   |                   |      

#                               Ex. B                              YES
#         |             |                   |                   |
# [ 3, 4, | 3, 3, 5, 6, | 3, 3, 4, 3, 6, 4, | 3, 3, 3, 5, 5, 5, | 3]
#         |             |                   |                   |      

#                               Ex. C                              YES
#         |             |                   |                   |
# [ 3, 4, | 3, 3, 5, 6, | 3, 3, 4, 3, 6, 4, | 3, 3, 3, 5, 5, 5, | 7, 7, 7]
#         |             |                   |                   |      

# If the final sublist ALSO "rules out" a majority element, as in A (and which
# can happen only when this final sublist also has even length), then we can
# immediately conclude that there is no majority element in the entire list, 
# since we have successfully demonstrated a partition of the list into 
# sublists without majority elements. The largest number of instances of any 
# one element in such as list is exactly half of the list size -- not enough 
# to be a majority.

# On the other hand, if the final sublist DOES have a majority element, then 
# that majority element MIGHT be the majority element of the full list. It is
# so in B, but not in C. Because we could use no more than O(1) space and thus
# could not track WHICH elements were the most frequent in previous sublists, 
# we must count all instances of this candidate in the list, which requires at
# most one more O(N) read of the data.
    
def f3(lst):
    """See f1 docstring. Runs in O(N) time and O(1) space."""
    count_to_beat = len(lst)//2
    i, x_count, oth_count = 0, 0, 0
    
    while i < len(lst):

        # "New sublist" when current element no longer the majority. 
    
        if x_count == oth_count:
            x, x_count, oth_count = lst[i], 0, 0
                    
        if lst[i] == x:
            if x_count == count_to_beat:  # Earliest possible return.
                return x
            x_count += 1
        else:
            oth_count += 1

        i += 1
        
    if x_count > oth_count:
        return x if count_x(lst,x) > count_to_beat else -1
    
    return -1

# The counting function uses a GENERATOR expression, not a list comprehension,
# which should maintain O(1) space. An alternative to this function would be 
# to simply use a for loop over the list, incrementing a count value by one
# for each hit. This has the advantage of returning early -- as soon as the 
# count exceeds the "count_to_beat". I opted for the below approach, which 
# always reads the full input, thinking that the Python sum and generator 
# expressions would be faster on average than Python's relatively slow for 
# loops. Might revisit later to test this hunch. 

def count_x(lst,x):
    """Returns the number of occurrences of x in lst in O(N) time."""
    return sum((1 if item == x else 0 for item in lst))
               
# Testing this function is interesting. Because f2 and f3 never check more
# than whether or not an element is equal to a current counted element, we can
# test them on lists containing no more than two unique numbers. Whether right
# or wrong, the functions' behavior on [ 1, 1, 1, 7, 7, 7] should be identical
# to their behavior on [ 1, 1, 1, 6, 23, 9] because the "structure" of the 1's
# -- the first and only element that gets set as a counted element -- is 
# identical in both. 

# Similarly, the behavior is identical on [ 1, 1, 4, 1, 4, 4, 1, 4, 1] and 
# [ 1, 1, 5, 1, 2, 9, 1, 3, 1] -- the counter starts new sublists at the same
# indices.

# We generate for a given length L all possible lists with unique "structures" 
# of 1's -- that is, the binary representation of all numbers 0 to 2^L-1 -- 
# and fill the rest with dummy data (here, 0, even though the above problem 
# description calls for inputs of positive integers only).
              
def test(length_limit):
    """Tests f2 and f3 against f1 on all unique lists of 0's and 1's
    with lengths < length_limit.
    
    Args:
        length_limit: A positive int.
        
    Raises:
        AssertionError: At least one of f2 or f3 is wrong.
    """
    for input_length in range(length_limit):
 
        for x in range(2**input_length):
            bin_str = bin(x)[2:]
            input = [0]*(input_length-len(bin_str))
            input.extend((int(char) for char in bin_str))
            
            assert f2(input) == f1(input)
            assert f3(input) == f1(input)