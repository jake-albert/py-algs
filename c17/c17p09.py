import matplotlib.pyplot as plt

# c17p09

# Kth Multiple: Design an algorithm to find the Kth number such that the only
# prime factors are 3, 5, and 7. Note that 3, 5, and 7 do not have to be 
# factors, but it should not have any other prime factors. For example, the 
# first several multiples would be (in order) 1, 3, 5, 7, 9, 15, 21.  

##############################################################################

# The most brute-force approach would involve finding the prime factorization 
# of every number from 1 up, and returning the Kth integer that factors only 
# to 3, 5, and 7. Finding the prime factors of a number x takes O(sqrt(x)) 
# time--is there a faster way to verify whether a number has the desired 
# property or not?

# Using O(K) memory to store previous valid numbers that have been found, we 
# can actually verify a new number x in O(1) time by checking if, for each 
# of the primes p, x evenly divides p and x/p is also a valid number.
 
# This trick allows us to find the Kth valid number in O(f(K)) time, where 
# f(K) is the Kth valid number. How fast this function grows is discussed
# below, but we can at least double the runtime by checking only odd values:

def f1(K):
    """Returns the Kth number with only 3,5,7 as prime factors.
    
    Args:
        K: A positive int.
    
    Returns:
        An int.
        
    Raises:
        ValueError: K is not positive.
    """
    FACTORS = (3,5,7)    
    return get_k_vals(K,FACTORS)[-1]
    
# If we are interested only in the Kth integer, there is no need to store and 
# return the whole list of the 1-Kth numbers, but I use the list to test
# against my more optimized solution. 
    
def get_k_vals(K,FACTORS): 
    """Returns a list of the first K valid integers."""
    if K <= 0:
        raise ValueError("K must be positive.")
        
    memo_set = set([1])
    test_val = 1
    out_list = [1]
    
    while len(memo_set) < K:
        
        test_val += 2
            
        for factor in FACTORS:  # Attempt smaller factors first.
            if test_val % factor == 0 and test_val // factor in memo_set:
                memo_set.add(test_val)
                out_list.append(test_val)
                break
        
    return out_list    
        
# The main reason this approach runs so slowly is that valid numbers become
# extremely sparse as K increases. In fact, the output value f(K) seems to
# grow exponentially, or at least very quickly:

#            f1(100) is      33,075
#            f1(200) is     900,375
#            f1(300) is   9,568,125

# Plotting f(K) as K increases shows what looks like exponential behavior. (I
# use my optimized function f2, not f1, to do this more feasibly.) This makes 
# sense, given that new values are created by taking previous values and 
# increasing the exponent of either 3,5, or 7 in their prime factorization.
    
def plot_f_of_k():
    """Saves a plot of f(K) vs. K to current directory."""
    START, STOP, STEP = 50, 1001, 50

    ks = range(START,STOP,STEP)
    plt.plot(ks,[f2(k) for k in ks])
    plt.savefig("c17p09.png")
    plt.close()

# Any approach that tests ALL numbers in a given range (or even just all ODD
# numbers), then, becomes unfeasible when K increases to beyond a few hundred,
# even if the approach can verify each number in O(1) time.

# My better approach below works by directly FINDING each valid number in O(1) 
# time, thus decreasing runtime to O(K). We know that f(K) is in the stream of
# numbers 3,6,9,12,15,..., but even more narrowly that it is in ODD multiples 
# of 3 (3,9,15,21,...), 5 (5,15,25,35,...) and 7 (7,21,35,49,...).

# One way to exploit this fact is to maintain three streams that "spit out"
# those multiples in order, and pick the smallest of the three at each step. A
# problem, though, is that some of these values still need to be ignored. For 
# example, 33 is an odd multiple of 3, but has a prime factor of 11, which is 
# not allowed. 

# A workaround to this solution requires O(K) space to store previous valid 
# values. Rather than have the three streams spit out ALL odd multiples of 3,
# 5, and 7, we can have them spit out only multiples of those prime factors by 
# previously calculated valid numbers.

# For example, say that f(K) has been found for K = 8, and now we must solve 
# for K = 9. At this point, the lowest multiples of the factors with some 
# lower valid number that have NOT yet been added are 3*9 = 27, 5*5 = 25, and 
# 7*5 = 35. The lowest of these is 25, so we add 25 to the list of valid
# numbers and "shift" the 5 multiples one to the right, giving 5*7 = 35.

#     K |   1   2   3   4   5   6   7   8  ...
#   f(K)|   1   3   5   7   9  13  15  21  ...
# --------------------------------------------
# 3*f(K)|   3   9  15  21  27  ...............
#                           ^
# 5*f(K)|   5  15  25  35  ....................
#                   ^-->^
# 7*f(K)|   7  21  35  .......................
#                   ^

# Because we always take the lowest possible value or values, we never "skip"
# valid numbers and correctly find every valid number.

# Runtime in total is O(K). O(1) memory is required for each "stream", as I 
# store only one value from each stream at a time, but altogether O(K) space 
# is used to keep the running list of valid numbers.

# My below solution is generalized to handle any number of prime factors. In 
# fact, even when factors are not necessarily prime, the class outputs
# meaningful information; namely, the Kth integer that can be expressed as 
# the product of non-negative integer powers of any list of "factors".

class MultiplesStream:
    """Simulates a stream of multiples of a specific factor.
    
    Attributes:
        factor: The factor (ex. 3, 5, or 7).
        index: The index to the list of valid vals.
        value: The value of factor * valid_vals[index]
    """
    
    def __init__(self,factor):
        """Inits a stream with its first value of factor * 1."""
        self.factor = factor
        self.index = 0
        self.value = factor

class ValidGenerator:
    """Generates numbers whose only prime factors are specified.
    
    Attributes:
        valid_vals: A list of valid integers.
        streams: A list of MultiplesStream instances.
    """
    
    def __init__(self,factors):
        """Inits a ValidGenerator with only the first number.
        
        Args:
            factors: Any iterable of ints.
        """
        self.valid_vals = [1]
        self.streams = [MultiplesStream(factor) for factor in factors]
        
    def get_kth_val(self,K):
        """Finds increasing valid numbers until K are in the list.
        
        Args:
            K: A positive int.
            
        Raises:
            ValueError: K is not positive.
        """
        if K <= 0:
            raise ValueError("K must be positive.")
        
        while len(self.valid_vals) < K:
            self._find_next_val()
            
        return self.valid_vals[-1]
            
    def _find_next_val(self):
        """Appends the next valid number to valid_vals."""
        cur_min = float("inf")
        updates = []
        
        for stream in self.streams:
        
            # We create a NEW list of streams to update anytime that a
            # stream's value represents a new minimum. 
        
            if stream.value < cur_min:
                cur_min = stream.value
                updates = [stream] 
            elif stream.value == cur_min:
                updates.append(stream)
        
        self.valid_vals.append(cur_min)
        
        for stream in updates:
            stream.index += 1
            stream.value = stream.factor * self.valid_vals[stream.index]

def f2(K):
    """See f1 details."""
    FACTORS = (3,5,7)
    gen = ValidGenerator(FACTORS)
            
    return gen.get_kth_val(K)
    
# To test, rather than call f1 and f2 repeatedly on increasing K values, which
# duplicates a lot of work, I construct a list once by each function of all 
# valid numbers from f(1) to f(K) and compare those lists.
    
def test(K):
    """Tests outputs 1-K of f2 approach against f1 approach."""
    
    FACTORS = (3,5,7)
    
    numbers_1 = get_k_vals(K,FACTORS)
    
    gen = ValidGenerator(FACTORS)
    gen.get_kth_val(K)
    numbers_2 = gen.valid_vals
    
    assert numbers_1 == numbers_2