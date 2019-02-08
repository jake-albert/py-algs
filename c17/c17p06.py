# c17p04

# Count of 2s: Write a method to count the number of 2s that appear in all the
# numbers between 0 and n (inclusive).
#
# EXAMPLE
# Input: 25
# Output: 9 (2,12,20,21,22,23,24,25. Note that 22 counts for two 2s.)

##############################################################################

# I assume for this problem that the input can only be a non-negative integer.

# First, a brute force counter (useful to test the correctness of my optimized
# function). Because we check each digit of every number from 2 to n, the time
# complexity is O(N*log10(N)), where N is the input integer. Pedantically, 
# though, if we express complexity as a function of the BIT LENGTH of the
# input, which is log2(N), runtime is in O((2**N)*N), which is not ideal.

def f1(n):
    """Returns the number of 2s in all integers from 0 to n inclusive.
    
    Args:
        n: A non-negative int.
    
    Returns:
        An int.
    """    
    total = 0
    
    for i in range(2,n+1):
        total += get_two_digits(i)
        
    return total
    
def get_two_digits(x):
    """Returns the number of 2 digits in some integer x."""
    twos = 0
 
    while x > 0:
        if x%10 == 2:
            twos += 1
        x //= 10
 
    return twos

# Fortunately, there is a O(1) way to count all 2 digits in a specific PLACE
# (like tens, hundreds, thousands, etc) for all the integers 0 to N. 

# Say that N is 1422 and we want to know how many 2's are in the tens places 
# of 0,1,2,3,4,...1422. We first know that in every grouping of numbers with 
# the same values in the hundreds place and above, there are ten 2's in the 
# tens place. For example, for all numbers with the same prefix "94" before 
# the tens digit, these 2's in the tens place come from:

# {94}20,{94}21,{94}22,{94}23,{94}24,{94}25,{94}26,{94}27,{94}28,{94}29
#     ^      ^      ^      ^      ^      ^      ^      ^      ^      ^      

# Integer dividing 1422 by 100, we find that the numbers 0 through 1422 have
# 140 complete groupings of numbers with the same prefixes before the tens 
# place (ex. 300-399, 1200-1299), and because these each contribute 10 2's 
# each in the tens place, there are 1400 2's so far. But then what about the 
# numbers 1420, 1421, and 1422, which are not part of a complete grouping? 

# Finding 1422 mod 100 gives 22. We can handle the cases as follows:
#     If this number is < 20, then there are no more 2's in a tens place.
#     If this number is >= 20 and <= 29, then we find its difference with 19. 
#       22 - 19 = 3, so there are 3 more 2's in tens places.
#     If this number is > 29, then all ten possible 2's are present.

# The total in the tens place, then, is (10*1422//100) + min(0,max(10,22-19)).

# The algorithm below performs this logic for every place from the ones to the 
# most significant digit of N and thus takes O(log10(N)) time. When expressed 
# as a function of the bit length of the input, or O(log(N)), this is linear.

# I implemented the function iteratively. It requires O(1) space.

def f2(n):
    """Returns the number of 2s in all integers from 0 to n inclusive.
    
    Args:
        n: A non-negative int.
    
    Returns:
        An int.
    """
    DIGIT = 2
    
    comp = 1     # Powers-of-ten component (1,10,100,1000...).
    builder = 0  
    output = 0
    
    while n > 0:
        
        # On each iteration we "shift" the least significant digit 
        # of n over to the most significant digit of builder.
        
        builder += comp*(n%10)  # ex. for n=5234, comp=1, builder is 4,
        n //= 10                # and n reassigned to 523.
    
        # To get the comp place digits equal to DIGIT in n, we include:
        #     1. instances of the DIGIT in a complete grouping, ex. 
        #        523*1 to account for the DIGITs in the ones place from
        #        0 to 5230; and 
        #     2. instances of the DIGIT in an incomplete grouping, ex. 
        #        when digit is 2, max(0,min(1,3)) = 1
        
        output += (n*comp) + max(0,min(comp,(builder-((DIGIT*comp)-1))))
        
        comp *= 10  # The "load" of digits per grouping for next place. 
    
    return output
        
def test(trials):
    """Tests results of f2 against the correct results of f1.
    
    Args:
        trials: A non-negative int. All inputs < trials are tested.
    
    Raises:
        AssertionError: An f2 result is incorrect.
    """
    for n in range(trials):
    
        if n % (max(1,trials//100)) == 0:
            print(f"Testing on n = {n} ({100*n/trials:.0f}%)")
    
        r1, r2 = f1(n), f2(n)
    
        try:
            assert r1 == r2
        except:
            raise AssertionError("Ans: {r1}. Returned: {r2}")