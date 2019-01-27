from random import randint

# c16p17

# Contiguous Sequence: You are given an array of integers (both positive and 
# negative). Find the contiguous sequence with the largest sum. Return the
# sum.
#
# EXAMPLE
# Input: 2, -8, 3, -2, 4, -l0
# Output: 5 ( i.e. , { 3, -2, 4}) 

##############################################################################

# An important definition to clarify is the maximum sum in a case where no 
# positive integers exist in the list. I choose not to permit subsequences of 
# length 0 when the input is non-empty and to interpret the maximum sum then
# to be the maximum value in the all non-positive list.

# While both solutions below use dynamic programming concepts to run in O(N) 
# time using O(1) space, the second is far cleaner than the first and should
# be expected to run faster because it on average does less work per integer.

# The first approach treats the input list as a sequence of "globs", or 
# maximally long continguous sequences, of negative and non-neg integers. For
# example, the example array can be though of as an empty negative glob,
# followed by a non-neg glob with 2, then a negative glob with -8, and so on.
# An array like [-5,-6,1,-10,-8,3,-5,-9,2] begins with a negative glob of -5 
# and -6. Otherwise, the maximum sum must be the result of summming over a 
# sub-list that takes the form:

# NON-NEGATIVE_GLOB (NEGATIVE_GLOB NON-NEGATIVE_GLOB)*

def f1(lst):
    """Returns the maximum sum of any contiguous sequence of a list.
    
    Args:
        lst: A list of integers.
        
    Returns:
        An integer, or None if input list is empty.
    """
    if len(lst) == 0:
        return
        
    # Begin by peeling away the leading non-positive integers while
    # storing the non-positive integer with the highest value. If the 
    # entire list is traversed in this step, return that value.
    
    least_neg = float("-inf")
    left = 0
    
    while lst[left] <=0:
    
        if lst[left] > least_neg:
            least_neg = lst[left]
        left += 1
        
        if left >= len(lst):
            return least_neg
            
    # After this step, peel away trailing non-positive integers. If we 
    # have not yet returned by this point, then we know we will encounter
    # at least one positive value.
    
    right = len(lst) - 1
    while lst[right] <= 0:
        right -= 1
    
    # We now have two indices, left and right, that mark the locations
    # of the left-most and right-most positive values in the array. The 
    # first non-negative glob beginning at left is the first candidate 
    # for a maximum sum. The global maximum sum must result from summing 
    # over globs and must END with some non-negative glob.
    
    # For every non-negative glob that is not the first, the maximum sum 
    # that ENDS with it is either the sum from that glob alone, or the 
    # sum of that glob, the preceeding negative glob, and the maximum 
    # sum that ends at the previous glob. One of these maximum sums is 
    # the global maximum. 
    
    i, curmax = get_glob(left,lst)
    bestmax = curmax
    
    while i <= right:
        i, neg = get_glob(i,lst)
        i, pos = get_glob(i,lst)
        curmax = max(pos,curmax+neg+pos)
        bestmax = max(bestmax,curmax)
    
    return bestmax
    
def get_glob(i,lst):
    """Sums the glob of either non-negative or negative values 
    beginning at index i of the input list. 
    
    Args:
        i: An integer index.
        lst: A list of integers.
        
    Returns:
        The first index to the right of the glob, and the sum of 
        that glob.
    """
    
    # Determine from the first value whether we are in a non-neg or neg 
    # glob. Continue to sum as long as within the same glob.
    
    cmp = (lambda x: x >=0) if lst[i] >= 0 else (lambda x: x < 0)  
    sum = 0
    
    while i < len(lst) and cmp(lst[i]):
        sum += lst[i]
        i += 1
    
    return i, sum
    
# The second approach uses similar inductive logic as above but at the ELEMENT
# level as opposed to the GLOB level. The contigous sequence with maximum sum
# is also the best contiguous sequence of all the sequences that end at some 
# index x. As a base case, the sum of the best contiguous sequence that ends 
# at index 0 is simply the value at index 0. For all other indices x, it is 
# either value at x alone, or the sum of x and the sum for the best contiguous
# sequence ending at x-1 (whichever is greater). We calculate each of these 
# sums, and return the maximum.  
    
def f2(lst):
    """Returns the maximum sum of any contiguous sequence of a list.
    
    Args:
        lst: A list of integers.
        
    Returns:
        An integer, or None if input list is empty.
    """
    if len(lst) == 0:
        return

    best,prev = lst[0],lst[0]
    for i in range(1,len(lst)):
        prev = max(lst[i],prev+lst[i])
        best = max(prev,best)
    
    return best
    
# For correctness testing, I wrote a brute-force algorithm that sums each of 
# the O(N^2) contiguous subsequences of a list, altogether running in O(N^3) 
# time. This function takes no shortcuts.

def f3(lst):
    """Returns the maximum sum of any contiguous sequence of a list.
    
    Args:
        lst: A list of integers.
        
    Returns:
        An integer, or None if input list is empty.
    """
    if len(lst) == 0:
        return
 
    def sumrange(a,b):
        output = 0
        for index in range(a,b+1):
            output += lst[index]
        return output
        
    maxsum = float("-inf")
    for i in range(len(lst)):
        for j in range(i,len(lst)):
            maxsum = max(maxsum,sumrange(i,j))
            
    return maxsum
  
def test(trials,n=200):
    """Tests f1 and f2 against the correct f3 on randomized inputs.
    
    For each trial, generates an input list of n random integers from
    -10 to 10 and checks that f1 and f2 return correct values. Prints 
    progress updates and any discrepancies it finds.
    
    Args:
        n: An integer number of trials.
    """
    messups = 0

    for i in range(trials):
        
        if i%10 == 0:
            print("on {}th trial".format(i))
    
        lst = [randint(-10,10) for _ in range(n)]      
        correct_val = f3(lst)
        
        if f1(lst) != correct_val:
            print("f1 result incorrect:",lst)
            messups += 1
        if f2(lst) != correct_val:
            print("f2 result incorrect:",lst)
            messups +=1
            
    print(f"{messups} messups.")