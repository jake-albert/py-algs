import sys
sys.path.append('..')
from data_structs import DequeQueue
from time import time    
from c17p02 import f1 as my_shuffle
import matplotlib.pyplot as plt

# c17p04

# Missing Number: An array A contains all the integers from 0 to N, except for
# one number which is missing. In this problem, we cannot access an entire
# integer in A with a single operation. The elements of A are represented in
# binary, and the only operation we can use to access them is "fetch the jth 
# bit of A[i]," which takes constant time. Write code to find the missing 
# integer. Can you do it in O(N) time? 

##############################################################################
  
# (I assume that the correct interpretation of the problem when an empty list 
# is input is that the list is missing the number 0).

# First, I define a function that allows us to "fetch the jth bit of A[i]".

def get_jth_bit(x,j):
    """Returns the jth bit of some integer x."""
    return 1 & (x >> j)

# If the input list is already sorted in increasing order, then we can easily 
# identify the missing number in O(N) time by checking only the 0th bit of 
# each integer in order. The "gap" where the skipped integer should be will 
# have a sequence of two 0 or 1 0th bits in a row, and we return the index of 
# the number with the second of these bits. For example, if n is 7 and the 
# missing number is 4:
 
# i | A[i] | bits 
# --|------|------
# 0 |   0  |  000  
# 1 |   1  |  001
# 2 |   2  |  010
# 3 |   3  |  011
# 4 |   5  |  101  <==== !!
# 5 |   6  |  110
# 6 |   7  |  111 
    
# But when we cannot assume that the input is sorted, O(N) storage enables us 
# to still find the missing number in O(N) time. Say that n is 15 and the 
# missing number is 6, in a shuffled list:

#  i | A[i] | bits
# ----------------
#  0 |   7  | 0111
#  1 |  11  | 1011
#  2 |   8  | 1000
#  3 |   5  | 0101
#  4 |   9  | 1001
#  5 |  10  | 1010
#  6 |   2  | 0010
#  7 |   4  | 0100
#  8 |   1  | 0001
#  9 |  12  | 1100
# 10 |  13  | 1101
# 11 |  14  | 1110
# 12 |   3  | 0011
# 13 |  15  | 1111
# 14 |   0  | 0000

# Consider the 0th bit. We can expect that if no numbers 0-15 inclusive were
# missing, we would have 16//2 = 8 0's at the 0th position, and 16//2 = 8 1's
# at the 0th position. But if we count 0's and 1's at the 0th position, we see
# only 7 0's and 8 1's. This indicates that the missing number must have a 
# zero bit at the 0th position.

# What next? We could reason by similar logic how many 0's and 1's we expect 
# in the 1st position, and then 2nd, and so on until we have "constructed" the
# correct missing value, but this would require O(NlogN) time, no better than 
# if we were to first sort the values and solve as first described.

# The key is to ELIMINATE half of the values at each bit. When we find that
# the missing number above has a 0 bit at the 0th position, we do not need to 
# look at numbers with a 1 bit there. Doing so means that total runtime is in
# O(N + N/2 + N/4 ...) or O(N) time. We also require O(N) storage.

# I wrote the below function iteratively, which makes the code a little more 
# cumbersome than I think it would need to be if I wrote it recursively. 

def f1(lst):
    """Returns the missing number in a list.
    
    Args:
        lst: A list of all ints 0 to N except for one missing number. 
    
    Returns:
        An int.
    """

    # At each iteration, we remove the values from the "current" queue
    # and sort them into the correct queue based on their jth bit. We 
    # arbitrarily set the zeros queue as first "current".
    
    q_0 = DequeQueue(lst)  
    q_1 = DequeQueue()
    cur_queue = q_0                                                          
    
    j         = 0  
    output    = 0
    
    while 1<<j <= len(lst):
    
        cur_load = len(cur_queue)  # Size of queue changes so store it!                              
        for _ in range(cur_load):
            
            val = cur_queue.remove()           
            if get_jth_bit(val,j):
                q_1.add(val)
            else:
                q_0.add(val)
        
        # Now, only vals with least significant j-1 bits identical to 
        # output are expected to remain (but one is missing). For 
        # example, if len(lst) is 17, the bit 0 has been found to be 
        # "1", and bit 1 "0", then j is 2, and only vals <= 17 and 
        # ending in bits "01" are expected to be left. These start at 1
        # and increase by 2^j. (1,5,9,13,17).
        
        # This number of vals is either even or odd (compare with when 
        # the first two bits are "11", yielding 3,7,11,15) and the 
        # vals' jth bit alternates between 0 and 1. Thus the expected
        # number of vals with a "0" jth bit is either equal to, or one 
        # greater than, the expected number of values with a "1".
       
        # When the expected number of vals are equal, and the missing 
        # number has a "0" jth bit, then q_1 should have more vals than
        # q_0. If the missing number has a "1", then q_0 has more vals.
        
        # When the expected number of vals in q_0 is expected to be one 
        # greater than the number of vals in q_1, then if the missing 
        # number has a "0" jth bit, then q_0 and q_1 should have the 
        # same number of vals. If the missing number has a "1", then 
        # q_0 has more vals.
        
        # It follows, then, that the missing number has a "1" jth bit 
        # iff q_0 has more vals than q_1.
        
        if len(q_0) > len(q_1):  
            output |= (1<<j)
            cur_queue = q_1
            drain(q_0)
        else:
            cur_queue = q_0
            drain(q_1)
            
        j += 1
    
    return output
    
def drain(queue):
    """Removes all items from a queue."""
    while not queue.is_empty():
        queue.remove()       
    
# The below test functions (casually) verified correctness and O(N) runtime.

def test(n,trials):
    """Tests f1 for correctness over randomly generated inputs.
    
    Args:
        n: A non-negative int. See problem description.
        trials: The number of inputs to create and test.
    
    Raises:
        AssertionError: f1 fails to find the correct missing number.
    """
    for trial in range(trials):
        lst = list(range(n))
        my_shuffle(lst)
        ans = lst.pop() if n>0 else 0
        
        res = f1(lst)
    
        try:
            assert ans == res
        except:
            st = f"Incorrect output {res} on {lst} w/ missing {ans}."
            raise AssertionError(st)
            
def time_test():
    """Tests runtime of f1 over inputs of various length and saves a 
    plot of results in the current directory.
    
    Raises:
        AssertionError: f1 fails to find the correct missing number.
    """
    REPETITIONS = 200     # Larger value helps smooth the plot. 
    MIN_LENGTH  = 100
    MAX_LENGTH  = 10001
    STEP        = 100

    sizes = []
    times = []
    
    for n in range(MIN_LENGTH,MAX_LENGTH,STEP):
        
        total_time = 0
        
        for _ in range(REPETITIONS):
        
            lst = list(range(n))
            my_shuffle(lst)
            ans = lst.pop() if n>0 else 0
        
            start = time()
            res = f1(lst)
            finish = time()
            
            assert ans == res
            
            total_time += (finish-start)
        
        sizes.append(n)
        times.append(total_time)
    
    plt.plot(sizes,times)
    plt.savefig("c17p04.png")
    plt.close()