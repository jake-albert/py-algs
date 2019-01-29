# c16p05

# Factorial Zeros: Write an algorithm which computes the number of trailing 
# zeros in n factorial. 

##############################################################################

# The number of trailing 0's in n factorial is equal to the minimum of the
# power of 2 and the 5 power of 5 in the prime factorization of that factorial.

# For EVERY positive integer n, the prime factorization of n! will have MORE
# 2's in it than 5's. So the limiting factor is 5. We need only find the 
# number of 5's in the prime factorization and return that value.

# Consider 12!, which is equal to 12 times 11 times, and so on. The number of
# 5's multiplied during this process is 2: One from the 10 and one from the
# 5. So we find 12 // 5 and determine it to be 2, and return.

# BUT we must not also forget that 25 will contribute 2 5's, and that 125 
# will contribute 3 5's, and so on. So for 26!, the correct number of 5's is 
# equal to 5 (from 5,10,15,20,25) plus 1 (the 'second' 5 from 25). 

# The algorithm performs a set of constant-time operations once for every
# power of 5 that is less than or equal to the input. If the input size is of
# fixed length, like a 32-bit unsigned integer, then it will take ceiling of log
# base 5 of 4.3 billion or around 14 steps at most, so we can even argue that 
# it will run in constant time. For arbitrarily long input, it runs in O(logN), 
# with the log base 5 instead of log base 2, which is in linear time to the 
# length of the input. No more than constant space requirements.

def f1(n):
    """Computes the number of trailing zeros in n factorial.
    
    Args:
        n: A non-negative integer.  
        
    Raises:
        ValueError: n is negative.
    """
    if n < 0:
        raise ValueError("Input must be non-negative.")
    
    divisor = 5
    count = 0
    
    # Perform integer division on n by first 5, then 25, and so on 
    # until we have reached a divisor larger than n. At each step, the 
    # result of this division is added to the total count.
    
    count_for_divisor = n // divisor 
    
    while count_for_divisor > 0:
        
        count += count_for_divisor
        divisor *= 5
        count_for_divisor = n // divisor
    
    return count
    
def test():
    """Tests some sample inputs.
    """
    pairs = [(5,1),
             (12,2),
             (67,15)]
             
    for input, output in pairs:
        assert f1(input) == output