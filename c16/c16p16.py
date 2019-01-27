import operator as op
from random import shuffle

# c16p16

# Sub Sort: Given an array of integers, write a method to find indices m and n
# such that if you sorted elements m through n, the entire array would be 
# sorted. Minimize n - m (that is, find the smallest such sequence).
#
# EXAMPLE
# Input: 1, 2, 4, 7, l0, 11, 7, 12, 6, 7, 16, 18, 19
# Output: (3, 9)  

##############################################################################

# I interpret "sorted" here as "sorted in increasing order".

# My first approach achieves the solution in O(N) time, but also uses O(N) 
# space during a preprocessing step that my second approach, which requires
# O(1) space requirements, demonstrates is not necessary. Still, thinking 
# about the solution in terms of the first approach is what helped me realize 
# how to write code for the second.

# To find the left index, we must find the leftmost index whose value is
# greater than some value to the right. In a list that is already sorted 
# (regardless of whetehr or not that list has duplicates) no such index exists
# and this case must be detected. Ex. in [1,3,3,4,5,8,8,9], the value at every 
# index is less than or equal to every value to the right (this is what it
# means, in fact, to be "in order".) On the other hand, in the example input 
# list, [1,2,4,7,10,11,7,12,6,7,16,18,19], while both indices 6 and 7 have 
# values (7 and 12) that are greater than at least one value to their right, 
# the LEFTMOST index with this property is index 3 (value 7), and this marks 
# the left edge of the subarray that must be reordered. 

# Important is to note that this definition works on inputs with duplicate 
# values at the boundary. In [1,2,4,6,6,6,7,6,20], the indices 4, 5, and 6
# hold values that are greater than or equal to some value to their right, but 
# index 7 is the left-most index with a value strictly greater than a value to
# the right, and this marks the correct index for the shortest subarray that
# must be sorted.

# The right index simply the rightmost index whose value is less than some
# value to the left. We can use information from calculating the left index 
# to save a bit of time in doing this. 

def f1(lst):
    """Returns the indices to the shortest subarray that, if sorted, 
    would result in the entire input list being sorted.
    
    Args:
        lst: A list of integers.
        
    Returns:
        A tuple of integer indices, or the None object when input is 
        either empty or already sorted.
    """
    if len(lst) == 0:
        #print("List empty.")
        return
    
    left = get_left_index(lst)
    if left is None:  
        #print("Already sorted.")
        return
        
    right = get_right_index(lst)
    
    return left, right 
    
def get_left_index(lst):
    """Returns the leftmost index in an array whose value is greater 
    than some value to the right.
    
    Args:
        lst: A list of integers.
        
    Returns:
        An integer index, or the None object if no index with the 
        desired property exists.
    """
    
    # Generate a list such that the ith value contains the minimum 
    # value out of all values from index i to the right end of the
    # input. From left to right, check values in input list against
    # values in the the minimum list until the first index whose value
    # is greater the minimum is found.
    
    minlist = generate_extremes_list(lst,True)

    left = 0
    while left < len(lst) - 1 and lst[left] <= minlist[left+1]:
        left += 1
    
    return None if left == len(lst) - 1 else left
    
def get_right_index(lst):
    """Returns the rightmost index in an array whose value is less than 
    some value to the left. Assumes that the array is not already
    sorted and that start is the correct left index.
    
    Args:
        lst: A list of integers.
        
    Returns:
        An integer index.
    """
    
    # Generate a list such that the ith value contains the maximum 
    # value out of all values from index i to the left end of the
    # input. From right to left, check values in input list against
    # values in the the maximum list until the first index whose value
    # is less than the maximum is found.
    
    maxlist = generate_extremes_list(lst,False)
    
    right = len(lst) - 1
    while lst[right] >= maxlist[right-1]:
        right -= 1
    
    return right
    
def generate_extremes_list(lst,mins):
    """When mins is True, generates and returns a list of running 
    miniima from the right end of the input list. Otherwise, generates
    and returns a list of running maxima from the left end of the input
    list.

    Args:
        lst: A list of integers. 
        mins: A Boolean.
        
    Returns:
        A list of integers.
    """ 
    output = [0 for x in range(len(lst))]

    # Track minima from right to left using "less than" operator, and 
    # maxima from left to right using "greater than" operator.
    
    if mins:
        extreme = float("inf")
        order = range(len(lst)-1,-1,-1)
        cmp = op.lt
    else:
        extreme = float("-inf")
        order = range(len(lst))
        cmp = op.gt
  
    for i in order:        
        if cmp(lst[i],extreme):
            extreme = lst[i]
        output[i] = extreme

    return output

# The below approach is superior in runtime (by some constant factor due to 
# less processing of the input) and in memory requirements as it requires only 
# O(1) storage. To find the left index, it tracks a running minimum from right 
# to left, updating the index to output each time it encounters an index whose 
# value is greater than the minimum to the right. To find the right index, it 
# tracks a running maximum from left to right but begins at the left index 
# rather than at 0.   
    
def f2(lst):
    """Returns the indices to the shortest subarray that, if sorted, 
    would result in the entire input list being sorted.
    
    Args:
        lst: A list of integers.
        
    Returns:
        A tuple of integer indices, or the None object when input is 
        either empty or already sorted.
    """
    if len(lst) == 0:
        #print("List empty.")
        return

    left = get_left_index_2(lst)
    if left is None:
        #print("Already sorted.")
        return
        
    right = get_right_index_2(lst,left)
    
    return left, right
    
def get_left_index_2(lst):
    """Returns the leftmost index in an array whose value is greater 
    than some value to the right. 
    
    Args:
        lst: A list of integers.
        
    Returns:
        An integer index, or the None object if no index with the 
        desired property exists.
    """
    minimum = float("inf")
    left = len(lst) - 1
    
    # Update minimum only after checking current index's value against
    # the running minimum.
    
    for i in range(len(lst)-1,-1,-1):
        if lst[i] > minimum:
            left = i
        if lst[i] < minimum:
            minimum = lst[i]   
    
    return None if left == len(lst) - 1 else left
        
def get_right_index_2(lst,start):
    """Returns the rightmost index in an array whose value is less than 
    some value to the left. Assumes that the array is not already
    sorted and that start is the correct left index.
    
    Args:
        lst: A list of integers.
        srart: An integer representing the index to begin searching.
        
    Returns:
        An integer index.
    """  
    maximum = float("-inf")
    right = start
    
    # Update maximum only after checking current index's value against
    # the running maximum.
    
    for i in range(len(lst)):
        if lst[i] < maximum:
            right = i
        if lst[i] > maximum:
            maximum = lst[i]
            
    return right
 
# Some tests on randomized inputs. Confirm only that f1 and f2 are equivalent, 
# not necessarily that they are correct. 
    
def test(n,leng):
    """Tests randomized inputs for equivalency between f1 and f2.
    
    Generates a random shuffled list with values from 0 to i-1, and 
    duplicate values from 0 to i//2-1, n times for every i from 0 to 
    leng-1. Prints output only if the results of calling f1 and f2 
    differ on the same input.
    
    Args:
        n: Int number of trials per length of input list.
        leng: Int upper limit for list generation.
    """      
    for length in range(maxlength):
        input = list(range(length))
        input.extend(list(range(length//2)))
        for _ in range(n):
            shuffle(input)
            if f1(input) != f2(input):
                print(input)