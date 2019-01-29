from operator import le, ge

# c16p24

# Pairs with Sum: Design an algorithm to find all pairs of integers within an
# array which sum to a specified value. 

##############################################################################

# First, we must clarify how to handle duplicate elements in a list that sum 
# to the same value, such as in the list [1,1,2] for sum 3. Should the 
# function return (1,2) once, sticking only to unique pairs of values, or
# twice to indicate that there are two pairs of ELEMENTS that sum to 3?

# For this problem I chose the first option, but still assume that duplicate 
# integers can be present in the input.

# There is an O(N^2) solution that involves summing each pair of values and 
# returning each pair that sums to the value. There is also an O(NlogN) 
# solution that involves SORTING the list first, and then traversing from both
# front and back with two read heads. This second part runs in linear time, so 
# the time bottleneck is from sorting.

# For example, when the sum is 3, and the list sorts to [-6,-5,-1,7,8,9,15], 
# we start with read heads on -6 and 15. They sum to 9, which is larger than 
# the desired sum of 3, so we now know that 15, the largest value in the list,
# cannot possibly be part of a pair that sums to 3, as even when it is summed 
# with the lowest value in the list, it exceeds 3. So we move to -6 and 9, 
# which sum to 3. And this allows us to move inward on both ends to -5 and 8, 
# and so on. 

# This approach takes would be in O(NlogN) time and O(1) space if we sort in 
# place with quicksort. If the array is PROVIDED sorted, then the solution 
# runs in O(N) time. Since we can detect sortedness in O(N) time, we can 
# check for sortedness to determine whether to sort first or not.

# But there is also an O(N) approach on an unsorted list that requires hashing
# each value in the array, so it also requires also O(N) space.

# The below function takes a balance between optimizing for time and space. It 
# runs the O(N) time, O(1) space algorithm on sorted inputs (regardless of 
# whether they are increasing or decreasing), and runs the O(N) time, O(N)
# space algorithm on other inputs. To optimize time only, it could eschew the 
# check for sortedness and eat the O(N) memory cost on all inputs, and to 
# optimize space only, it could sort every input in place in order to run the 
# O(1) space algorithm.

def f1(lst,val):
    """Returns a set of tuples representing all unique pairs of 
    integers in an input list that sum to a value.
    
    Args:
        lst: A list of integers.
        val: An integer.
        
    Returns:
        A set of tuples of integers, each tuple in increasing order.
    """
    
    # There are no pairs of values in a list with 0 or 1 values, so 
    # we can return an empty set immediately.
    
    if len(lst) < 2:
        return set()               

    sorted, inc = is_sorted(lst)    
        
    if sorted:
        return find_pairs_sorted(lst,val,inc)
    else:
        return find_pairs_unsorted(lst,val)
        
def is_sorted(lst):
    """Determines in O(N) time whether a list is sorted. Assumes that 
    the list is of at least length 2.
    
    Args:
        A list of integers.
    
    Returns: 
        A Boolean indicating whether the list is sorted or not, and 
        a Boolean indicating whether, if sorted, it is in increasing 
        or decreasing order.
    """
    
    # Continue through the list until reaching an index whose value 
    # differs from the value at the following index. Determine there 
    # whether to test for increasing or decreasing order and attempt
    # to verify the rest of the list.
    
    for i in range(0,len(lst)-1):    
        if lst[i] == lst[i+1]:
            continue
       
        if lst[i] < lst[i+1]:
            cmp = le
            inc = True
        else:
            cmp = ge
            inc = False
        break
    
    for j in range(i+1,len(lst)-1):
        if not cmp(lst[j],lst[j+1]):
            return False, inc
    return True, inc
 
def find_pairs_sorted(lst,val,inc):
    """Returns a set of tuples representing all unique pairs of 
    integers in an input list that sum to a value. Assumes that the 
    list is sorted.
    
    Args:
        lst: A list of integers.
        val: An integer.
        inc: A Boolean. True if in increasing order, False otherwise.
        
    Returns:
        A set of tuples of integers, each tuple in increasing order.
    """
    output = set()
    
    # Create read heads on each end of the sorted list, and "pinch" in
    # from both sides until all possible pairs have been tested.
    
    left, right = 0, len(lst)-1
    while left < right:
    
        sum = lst[left] + lst[right]
        if sum < val:  # The smaller of the values cannot be in a pair. 
            if inc: left += 1 
            else: right -= 1
        elif sum > val:  # The larger of the values cannot be in a pair.
            if inc: right -= 1 
            else: left += 1
        else:
            output.add((min(lst[left],lst[right]),max(lst[left],lst[right])))
            left += 1
            right -= 1
    
    return output

def find_pairs_unsorted(lst,val):
    """Returns a set of tuples representing all unique pairs of 
    integers in an input list that sum to a value. 
    
    Args:
        lst: A list of integers.
        val: An integer.
        inc: A Boolean. True if in increasing order, False otherwise.
        
    Returns:
        A set of tuples of integers, each tuple in increasing order.
    """
    output_set, search_set = set(),set()
    
    # Each integer we see has either 1) not been designated as a 
    # "partner" to some other integer, in which case we determine what
    # integer would be its "partner" and add that to the set of 
    # "partners", or 2) has been designated as a "partner", in which 
    # case we add the pair to the output.
    
    for elem in lst:
        partner = val - elem  # The int that sums with elem to val.
        if elem in search_set: 
            output_set.add((min(elem,partner),max(elem,partner)))
        else:
            search_set.add(partner)
            
    return output_set
    
# For increased confidence that the solution is correct, we could write the
# O(N^2) brute-force solution to test f1 against over large numbers of input.
# Might revisit this later.