from operator import add, sub

# c16p21

# Sum Swap: Given two arrays of integers, find a pair of values (one value
# from each array) that you can swap to give the two arrays the same sum.
#
# EXAMPLE
# Input: [4, 1, 2, 1, 1, 2] and [3, 6, 3, 3}]
# Output: [1, 3] 

##############################################################################

# The total search space is in O(M*N) where M and N are the lengths of each 
# input list. A naive brute force algorithm could, for each of the M*N pairs
# of integers, swap them and then test the sums for equality in O(M+N) time.
# But we can improve on this approach. 

# To do so, we exploit the fact that when we swap some integer a from list A
# with some integer b from list B, the difference of the sums of the lists 
# changes by TWICE the difference between a and b. 

# (Example: if we swap 3 from [1,-4,5,3] with 8 from [-5,8], the first sum 
# changes from 5 to 10, and the second sum changes from 3 to -2. The 
# difference in sums changed from 2 to 10 more than that, 12.)

# We can "reverse engineer" this to find a pair of values that if swapped 
# will result in the difference in sums becoming 0.

# The below function takes at most two scans of each list, halting earlier if 
# it can, for a runtime of O(M+N), and requires O(min(M,N)) of space.

# We should make sure to determine how to handle a case when there is no pair
# of values to swap. Is it preferred we return a special value like -1 or 
# None? Could we print some message? For clarity in the toy example, I chose 
# to print a message and return None.

# We assume that the input lists have only integer elements.

def f1(A,B,verbose=False):
    """Returns a pair of values from two input lists that, if swapped,
    would result in the to lists summing to the same value. Even if 
    multiple such pairs exist, return the first pair and halt.
    
    Args:
        A, B: Lists of integers.
        verbose: A Boolean indicating whether to print commentary.
        
    Returns: 
        A tuple of integers, the first from A and the second from B, or
        None if no such pair exists.
        
    Raises:
        ValueError: At least one of the input lists is empty.
    """
    
    # For this problem, I defined the sum over an empty list as
    # undefined instead of to a value like 0 and chose to raise 
    # an exception as opposed to simply returning None.
    
    if len(A) == 0 or len(B) == 0:
        raise ValueError("Invalid input: lists cannot be empty.")
        
    # Sum the integers in both lists, and determine which list has 
    # the greater sum.
    
    sumA, sumB = 0, 0
    for a in A:
        sumA += a
    for b in B:
        sumB += b
    
    lo_lst, hi_lst = (A,B) if sumA <= sumB else (B,A)
    diff = abs(sumA-sumB)
    
    # If the difference between the sums is odd, there are no two 
    # integers that can be swapped and we may exit early. Otherwise, we 
    # must find a pairs of values in the lists that differ by this 
    # difference//2, because swapping them would "make up" for the 
    # difference between the two lists' sums.
    
    if diff % 2 == 1:
        if verbose:
            print("No such pair.")
        return
    
    # To minimize storage, we identify the shorter of the two lists for
    # copying into a set. We then look to each item in the longer list, 
    # identify a value either diff//2 greater than or less than this 
    # item depending on whether the longer list's sum is greater than 
    # or less than that of the shorter list's, and look up this value 
    # in O(1) time in the shorter list's set.
    
    # (If the sets sum to the same value, we simply look up the same  
    # value in the shorter list's set.)
    
    # We make sure to return the item from A before the item from B.
    
    shrt_lst, long_lst = (A,B) if len(A) < len(B) else (B,A)
    bridge_difference = sub if long_lst is hi_lst else add
    look_for = set(shrt_lst)
    
    for item in long_lst:
        to_find = bridge_difference(item,diff//2)
        if to_find in look_for:
            return (item, to_find) if long_lst is A else (to_find, item)
    
    if verbose:
        print("No such pair.")
    return
    
def test():
    """Tests some inputs and validates them if a pair is found. Does
    NOT validate None values when returned; doing so would require 
    attempting to swap every pair. Test cases far from exhaustive.
    """
    input1 = ([4,1,2,1,1,2],[3,6,3,3])      # (4, 6), or (1, 3) 
    input2 = ([-1,-5,17,3],[-3,21])         # (-5, -3)
    input3 = ([-1,-5,17,3],[1,-7,17,3])     # (17, 17)  
    input4 = ([1,2,3,4],[5,6,7,8])          # No such pair.
    input5 = ([1,2,3,4,0],[5,6,7,8,-6])     # (0,5), or (1,6)

    for input in [input1,input2,input3,input4,input5]:
        pair = (f1(*input))
        print("Result found:",pair)
        if pair is not None:
            s1 = sum(input[0]) - pair[0] + pair[1]
            s2 = sum(input[1]) - pair[1] + pair[0]
            if s1 != s2:
                print("ERROR: ",input,pair)
        
        
        