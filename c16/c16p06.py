# c16p06

# Smallest Difference: Given two arrays of integers, compute the pair of 
# values (one value in each array) with the smallest (non-negative) 
# difference. Return the difference. 

# EXAMPLE
# Input: {1, 3, 15, 11, 2}, {23, 127, 235, 19, 8}
# Output: 3. That is, the pair (11, 8).

##############################################################################

# The most straightforward way is to compare each of the M vals in the first 
# array against each of the N vals in the second, returning the min difference
# we find. This can be done in O(MN) time.

# One improvement that we can make to this is sort the two lists, and then  
# upon reading all values from lowest to highest, record a difference only
# when switching from one list to another. On the example input:

# [1,3,15,11,2] and [23,127,235,19,8]

# We sort each getting

# [1,2,3,11,15] and [8,19,23,127,235]

# Then, place read heads at both 1 and 8. We see that the min is 1, and then 2, 
# and then 3, all in the same list. Next is 8, and only then do we change to 
# read from a different list. So we record 8-3 which is 5. Next smallest value
# is 11, and we record 11-8 to find a better difference of 3.

# Important is to remember the case where all values in one list are less than 
# all values in a second list. [1,2,3,4] and [7,8,9,10] has a min diff of 3. 

# Sorts takes O(MlogM + NlogN) time, and reading heads O(M+N) time, so overall 
# the function needs O(mlogm + nlogn) time and requires O(1) assuming the 
# sorts are implemented in place. We assume that the input is correctly formed
# (no non-integer objects in the lists).

def f1(A,B):
    """Returns the difference between the pair of values with the 
    smallest non-negative difference, one from each input array.
    
    Args:
        A: A list of integers.
        B: A list of integers.
    
    Returns:
        An integer difference, or None if at least one of A or B is 
        empty.
    """
    if len(A) < 1 or len(B) < 1: return 
    
    # We sort the lists in place, but if it is required that the 
    # original input not be modified, then copying is required.
    
    A.sort()
    B.sort()
    
    min_diff = float("inf")           
    read_a, read_b = 0, 0     # Heads are indices.
    prev_lst = None           # Previous list with minimum val.
    
    # We can halt when we have reached the end of one list.
    
    while read_a < len(A) and read_b < len(B):
    
        if A[read_a] < B[read_b]:
            cur_lst = A
            cur_val = A[read_a]
            next_a, next_b = read_a+1, read_b
        elif B[read_b] < A[read_a]:
            cur_lst = B
            cur_val = B[read_b]
            next_a, next_b = read_a, read_b+1
        else:  # If the two values are equal, return immediately.
            return 0            
        
        # Check for a min difference only when read head switches.
        
        if prev_lst is not None and cur_lst is not prev_lst:
            diff = cur_val - prev_val
            if diff < min_diff:
                min_diff = diff
                
        read_a, read_b = next_a, next_b
        prev_lst = cur_lst
        prev_val = cur_val
    
    # One last check is required after exiting the loop. Find the 
    # "last value" to check, which is the value at whichever read head
    # has not yet traversed all of its list, and find the difference 
    # between this last value and the previous value seen. Return the 
    # minimum of this difference and the minimum difference seen so far.
    
    last_val = A[read_a] if read_b >= len(B) else B[read_b]
    diff = last_val - prev_val
    return min(diff,min_diff)
    
def test():
    """Tests some example inputs.
    """  
    assert f1([1,3,15,11,2],[23,127,235,19,8]) == 3
    assert f1([5,6,77,35,78,1,45,98],[245,676,111,344,766,800]) == 13