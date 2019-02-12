from operator import xor, add, mul
from functools import reduce
from math import sqrt, factorial, log2
from random import shuffle

# c17p19

# Missing Two: You are given an array with all the numbers from 1 to N 
# appearing exactly once, except for one number that is missing. How can you 
# find the missing number in O(N) time and O(1) space? What if there were two
# numbers missing? 

##############################################################################

# When one number is missing, the approach is straightforward. We know that 
# the numbers from 1 to N sum to (N)(N+1)/2, so all we can just sum the values
# in the list and subtract to find its difference with the expected sum.

# Are memory requirements here actually O(1), though? It is true that we use
# only one int object to store the sum, but of course the space required for 
# this int gets larger as the sum increases, since Python ints have no
# limiting bit length. Pedantically, then, O(log(N^2)) memory is required to 
# store the sum, which simplifies to O(logN) since the constant power inside a
# log is the same as multiplying by a constant factor.

# If, on the other hand, we assume we are storing the sum value using unsigned
# 32-bit integers, the highest value we can hold is around 4.3 billion, so we
# can handle only inputs with N such that (N)(N+1)/2 is less than this value. 
# If we can assume that N is always within this range (or any range, for that 
# matter), then it would be fair to argue that the algorithm uses O(1) space.

def f1(lst):
    """Returns the missing integer in a list.

    Args:
        lst: A list of ints 1 through some number N, with one number in
          that range missing.
          
    Returns:
        An int.
    """
    n = len(lst) + 1
    return (n)*(n+1)//2 - sum(lst)
    
# Another approach that works with one number missing is to use the bitwise
# XOR function for all of the values rather than the sum. We know that if we
# repeatedly XOR values together, and then we take a number with a 0 bit at 
# some position out from that agglomeration, then there is no change at that
# position. If it is a 1 bit, then the bit flips. 

# If we XOR all of the values 1 to N that we EXPECT to be in the list (x1) and
# XOR all of the values actually in the list (x2), then (x1 XOR x2) results in
# a number that has a 0 any time when bits match up between x1 and x2 (that is, 
# where there was no change from x1 to x2) and a 1 any time the bit flipped. 
# This number is the missing value.

# The below function requires twice as many calculations as the above since it
# is repeatedly calling XOR over O(N) values twice as opposed to finding a 
# single value for the expected sum above, but XOR should be a faster 
# operation than addition so the function might be faster. Might revisit to 
# test later.
 
# Provided we use an iterator like range() that does not actually use O(N) 
# memory to generate all of the numbers from 1 to N, then the only space that
# is needed is the O(logN) for the bits that must hold the highest value of N.
# Again, though, if we have some realistic expectation of a highest possible 
# value for N, we can argue that this is in O(1) space.

def f2(lst):
    """See f1 docstring."""
    
    # N is equal to len(lst)+1, so we call range with upper limit N+1.
    
    return reduce(xor,range(1,len(lst)+2)) ^ reduce(xor,lst)
    
# The REASON that both of these functions work is not because there is
# something special to the XOR operator, or to addition, but that both of 
# these agglomeration functions produce a single value from the input values 
# that, when combined in some other way with the agglomeration of all expected
# values from 1 to N, produce a UNIQUE value that we can use to determine the 
# missing value. To get a solution when there are TWO missing values, then we
# will need to find some other function, for every TWO distinct values from 1 
# to N that could be missing, produce different results. 

# Clearly, we cannot use addition alone as we did above. If we find, as above, 
# the sum S of expected values (N)(N+1)/2, then there are possibly many unique
# pairs of integers <= N that sum to S. For instance, [1,2,3,4,6,7,9,10] is
# missing 5 and 8, which sum to 13, and (10)(11)/2 = 55 minus the sum in the 
# list does correctly give us 13 as well, but there are several valid pairs of 
# integers: (3,10), (4,9), and (5,8).

# Another way to express this is that for some pair of integers X,Y such that 
# X < Y and X+Y = S, there are infinite integers A such that (X-A)+(Y+A) = S,
# because X-A+Y+A = X+Y is tautologically true no matter WHAT value A takes. 
# And when there are numbers 1 through N to deal with, there are O(N) possible
# A values that could yield pairs X and Y within range. 

# We can try using multiplication to disambiguate. Say we have a pair of 
# integers X and Y that add to S, and another pair of integers X-A and Y+A 
# that also add to S. Is it possible for X*Y to equal (X-A)*(Y+A)? What must
# A be for this to be true? Solving for A in the equation X*Y = (X-A)*(Y+A), 
# I found that A equals X-Y, but the integers X-(X-Y) and Y+(X-Y) are simply 
# the same pair of integers, Y and X. This implies that the pair of integers
# X and Y are the only pairs that both sum to S and have some product P.

# In the below function we find the sum and product of the missing numbers and 
# algebraically solve for the missing numbers. To find the product of the
# missing numbers, we first find the factorial of N, which gets large quite
# quickly. The number of bits to store N! is in O(log(N!)) which is in 
# O(Nlog(N)). Like above, if N is limited to some value, this is technically 
# O(1) space, but given that a 32-bit unsigned integer can hold only up to 
# 12!, this solution does not seem to meet the spirit of the problem when it 
# asked for O(1) space.

def f3(lst):
    """Returns the missing two integers in a list.

    Args:
        lst: A list of ints 1 through some number N, with two numbers
          in that range missing.
          
    Returns:
        A tuple of ints.
    """
    n = len(lst) + 2

    # There is actually way to do these calculations that is less 
    # memory intensive over many inputs. Start with the identities of 0
    # for addition and 1 for multiplication, and then for each number X
    # from 1 to N, add/multiply by that number X and sub/divide away 
    # the Xth number in the list (when X is in range of the list).
    
    # Worst-case memory performance is still the same, and it would be
    # important to handle division with floats or the Fractions library
    # properly, but on input lists such as [1,2,3,4...23,24,27,28] the
    # running product never exceeds 1000, as opposed to 28! which is 
    # larger than 10^29.
    
    S = (n)*(n+1)//2 - reduce(add,lst)
    P = factorial(n) // reduce(mul,lst)
    
    disc = sqrt(S*S-4*P)  # Discriminant of the quadratic equation.
    return int((S-disc)/2), int((S+disc)/2)
    
# It is possible to avoid using such big numbers above by summing the base-2
# logs of all of the numbers rather than multiplying them. Since log(X) + 
# log(Y) is equal to log(X*Y), if we exponentiate by 2 at the end we will end 
# up with the same product without ever dealing with factorials. 

# Just because we avoid using large numbers does not automatically mean that 
# we have negligible memory constraints, though. Using logs requires that we 
# store floats, and these floats must have enough bits to store sufficiently 
# precise numbers that we get correct results after rounding. Might revisit 
# later to determine for different levels of precision what the largest N is
# on which we can still expect correct results.

# With the standard Python float, which is accurate to 53 bits or about 16 
# decimal places, the below function fails on inputs where N is as low as 
# 71,431 or so. More rigorous testing would be needed to find out on exactly
# what kinds of inputs this is secure, but 
    
def f4(lst):
    """See f3 docstring."""
    n = len(lst) + 2
    
    S = (n)*(n+1)//2 - reduce(add,lst)
    P = round(2 ** (reduce(add,logs(range(1,n+1))) - reduce(add,logs(lst))))
    
    disc = sqrt(S*S-4*P)  # Discriminant of the quadratic equation.
    return int((S-disc)/2), int((S+disc)/2)
  
def logs(it):
    """Yields logs of iterator items 1-by-1 rather than O(N) list."""
    for item in it:
        yield log2(item)

# Is there another way that we can aggregate numbers using both addition and 
# XOR, given that both of these operations were useful when one number was 
# missing? We are able to in O(N) time and O(1) space find what the missing
# two numbers sum to, as well as what they XOR to. Perhaps we can take 
# advantage of the fact that bitwise addition is very similar to XOR? 

# Say that X+Y is 17, or [1,0,0,0,1], and A^B is 9, or [1,0,0,1]. We can
# deduce that the 0th bit of X and Y must XOR to 1, and since the carry from 
# the first addition must be 0, that the 1st bits of X and Y are both 0. It 
# is possible to deduce altogether that X and Y are 4-bit numbers of the form
# X = [a4,1,0,a0] and Y = [b4,1,0,b0], where a4^b4 and a0^b0 both XOR to 1. 

# But there are TWO pairs of numbers that fits these criteria, 13 and 4 as 
# well as 12 and 5, so we cannot determine the correct missing numbers from 
# this information.

# More generally, this approach gives us information for each bit in the pair
# of missing numbers whether A) they are both 0, B) they are both 1, or C) 
# they differ from each other. Up to log(N) of the bits can differ from each 
# other, so O(2**log(N)), or O(N), possible pairs of numbers, would need to 
# be tested. But we cannot do this without either using more than O(1) space 
# or taking O(N) time to check each pair, which violates our constraints.
          
# If we are permitted to modify the array, then there is another approach that 
# works by performing a sort of in-place radix sort on the input. Every number
# in the list "belongs" at an index equal to that number's value minus 1. At
# most two of these indices are currently out of range of the list, so we 
# append two "empty" indices to the list.

# [  2 ,  3 ,  1 ,  4 ,  5 ,  9 , 10 ,  7 ]
# [  2 ,  3 ,  1 ,  4 ,  5 ,  9 , 10 ,  7 ,  X ,  X ]

# Every number that we encounter in the list either A) is already at the 
# correct index (ex. 4 and 5 above), B) belongs in one of the new indices that
# resulted from the append (ex. 9 and 10), C) belongs where one of the numbers 
# in case B) was originally (ex. 7), or D) is part of a closed loop with other
# numbers that can be shifted around circularly (ex. 1,2,3). 

# We can perform these shifts in O(N) time by progressing through the list and 
# never moving a number to a different index more than once. Once the sort is 
# complete, the two "empty" indices that remain are the locations of the 
# missing numbers, and one more scan of the list will help find them. 

# [  1 ,  2 ,  3 ,  4 ,  5 ,  X ,  7 ,  X ,  9 , 10 ]

# This approach is generalizable to any problem with list 1 through N that has 
# any number R of missing numbers, and requires O(R) additional space for the 
# extra appended slots. For this problem R is a constant, 2, so space is O(1). 
    
def f5(lst):
    """See f3 docstring. Unlike f3, modifies input list."""
    return find_r_missing_numbers(lst,2)
    
def find_r_missing_numbers(lst,R):
    """Returns the R missing numbers in a list.
    
    Sorts the list in place after appending R empty slots to the list.
    
    Args:
        lst: A list of ints 1 through some number N, with R numbers in 
          that range missing.
          
    Returns:
        A tuple of R ints.
    """
    NO_NUM = -1 
    for _ in range(R):
        lst.append(NO_NUM)
    
    for i in range(len(lst)):
        
        # Empty slots and case A.
        
        if lst[i] == NO_NUM or lst[i] == i+1:
            continue
        
        # Cases B, C and D. Move a number from its current slot,
        # leaving an empty slot behind, to its proper slot, and then
        # move whatever displaced number was there, until there is an
        # empty slot rather than a number to displace.
        
        curr_val = lst[i]
        lst[i] = NO_NUM
        
        while curr_val != NO_NUM:
            next_val = lst[curr_val-1]
            lst[curr_val-1] = curr_val
            curr_val = next_val
        
    return tuple([i+1 for i in range(len(lst)) if lst[i] == NO_NUM])    
    
# If we are not allowed to modify the list, I thought of a probabilistic 
# approach with average O(N) performance. Though we cannot tell what the two
# missing numbers are by knowing only the sum, we DO get more information if
# we calculate TWO sums: one of the upper half of numbers in the list, and one
# of the lower half of numbers. Regardless of the order of numbers in the list, 
# we are able to determine which half any number belongs to since 1 through N 
# are supposed to be there.

# If we find that one number is missing from the lower sum, and one from the 
# upper sum, then we can immediately deduce those missing numbers in the same 
# way we did in f1. Otherwise, we can go through the list again, this time 
# narrowing the range of numbers that we sum to those in the half where we
# know both missing numbers are.

# Since the list is unordered, we must scan the entire list each time we sum 
# to hit all of the numbers we want, no matter how small the range is. BUT the
# average number of times we must scan is constant. We start with 1 sweep 
# regardless of which numbers are missing. Say that the first missing number 
# is in some of the numbers 1 through N (either the lower or upper half). 
# The second missing number is in the same half roughly half the time, and 
# in the opposite half the other half of the time. So for roughly half of 
# inputs we make another scan. Following this logic recursively, we see that 
# the full call requires 1 + 1/2 + 1/4 + ... scans, which approaches 2, a 
# constant, as N approaches infinity. 

# So this approach runs in O(N) time, but in the AVERAGE case over UNIFORMLY 
# RANDOMLY DISTRIBUTED inputs. The worst case is when the missing numbers are
# certain pairs of adjacent integers, such as 1 and 2 when N is 1000. In this
# case, the full number of O(log(N)) scans is required, making performance 
# O(NlogN). 

# This behavior makes the approach similar to, unsurprisingly, another
# algorithm that relies on random splits over the input: Quicksort, which has
# average performance of O(NlogN) but worst case O(N^2) runtime over certain
# inputs, like already sorted lists. We tend to be comfortable describing 
# Quicksort as an "O(NlogN) sort", so by that standard I am okay with calling
# the below function an O(N) algorithm, but it would be important to remember 
# that the average performance in "real" contexts where the inputs could skew 
# towards suboptimal cases might be worse.

# I wrote the function iteratively, not recursively, so as to avoid storing 
# instances of execution on a call stack, which would lead to O(logN) space 
# requirements in the worst case.

def f6(lst,timetest=False):
    """See f3 docstring.
    
    When timetest is True, returns the number of scans of that were 
    required during the call for testing purposes. 
    """
    n = len(lst) + 2
    lo, hi = 1, n
    passes = 0
    
    while hi - lo > 1:  # When False, only two numbers remain.
    
        passes += 1
    
        # The split is the INCLUSIVE upper bound of the lower half. 
        
        spl = (lo + hi) // 2
        els, ehs = expected_sums(lo,spl,hi)
        als, ahs = actual_sums(lst,lo,spl,hi)
    
        # If a number is missing from BOTH halves, then we have found
        # both numbers. Otherwise, we decrease the range of candidates.
        
        if als < els and ahs < ehs:
            return passes if timetest else (els-als, ehs-ahs)
        else:
            lo,hi = (lo,spl) if ahs == ehs else (spl+1,hi)
    
    return passes if timetest else (lo, hi)
   
def expected_sums(lo,spl,hi):
    """Returns the expected lower sum and expected higher sum.
    
    Given positive integers lo, spl, and hi, returns the sum of all 
    integers from lo to spl inclusive, and from spl+1 to hi inclusive. 
    For example, if lo is 4, spl is 6, and hi is 9, returns 4+5+6 = 15 
    and 7+8+9 = 24. Applies simple algebra in O(1) time.
    """
    spl_item = (spl)*(spl+1)  # Saved to avoid redundant calculations.
    return (spl_item-(lo)*(lo-1))//2, ((hi)*(hi+1)-spl_item)//2

def actual_sums(lst,lo,spl,hi):
    """Returns the actual lower sum and actual higher sum.
    
    Given a list and positive integers lo, spl, and hi, returns the sum
    of all elements in the list from lo to spl inclusive, and from 
    spl+1 to hi inclusive. Runs in O(n) time.
    """
    lo_sum, hi_sum = 0,0
    for num in lst:
        if lo <= num and num <= spl: 
            lo_sum += num
        elif spl < num and num <= hi:
            hi_sum += num
    
    return lo_sum, hi_sum

# The below "speed test" checks how many scans of the list are required and 
# verifies that the behavior predicted above is occurring. 

# For example, with n=50, we see:

# 1225 total trials.              = 50*49/2 unique input pairs
#    min: 1                       ~ Half of inputs require only one pass.
#    max: 5                       Worst case: floor(log(50)) passes.
#    avg: 1.876734693877551

# And with n=1000:

# 499500 total trials.            = 1000*999/2 unique input pairs
#    min: 1                       ~ Half of inputs require only one pass.
#    max: 9                       Worst case: floor(log(1000)) passes.
#    avg: 1.989149149149149       AVG # of passes approaches 2.

def speed_test(n):
    """Tests runtime of f6.
    
    Given an integer N, tests f6's performance over an input list for 
    all unique pairs of missing integers X and Y such that X < Y < =N. 
    Records the number of scans over the list that were required to 
    determine the output, and aggregates and prints statistics of these.
    """
    all_counts = []
    
    for lo in range(1,n+1):
    
        print(f"Testing missing pairs with {lo} as lo...")
    
        for hi in range(lo+1,n+1):
            bob = [x for x in range(1,n+1) if (x!=lo and x!=hi)]     
            all_counts.append(f6(bob,True))
    
    all_counts.sort()
    
    min,max = all_counts[0],all_counts[-1]
    avg = sum(all_counts) / len(all_counts)
    
    print(f"{len(all_counts)} total trials")
    print(f"    min: {min}")
    print(f"    max: {max}")
    print(f"    avg: {avg}")

  
# Interestingly, the book suggested a different "equation-based" approach that
# calculates the sum, and then sum of squares of inputs. This approach does 
# not fail on larger inputs the way f4 did, does not calculate factorials  
# which quickly overflow the way f3 did, so it is the superior equation-based
# function. Like my informal proof above with X-A and Y+A, it can be shown by 
# solving quadratic equations that only unique pairs of integers have both the
# same sum and same sum of squares.

def f7(lst):
    """See f3 docstring."""
    n = len(lst) + 2

    S1 = (n)*(n+1)//2 - reduce(add,lst)
    S2 = reduce(add,squares(range(1,n+1))) - reduce(add,squares(lst))
        
    disc = sqrt(2*S2-S1*S1)  # Discriminant of the quadratic equation.
    return int((S1-disc)/2), int((S1+disc)/2)
  
def squares(it):
    """Yields squares of iterator items 1-by-1 instead of O(N) list."""
    for item in it:
        yield item**2

# We confirm accuracy of f5, f6, and f7 below. (On small inputs, f3 and f4 
# could also be tested, but I am reserving the tests only for the "best" of 
# each of the three types of approaches I worked with for this problem.)
        
def accuracy_test(n,trials):
    """Tests correctness of the best equation-based approach, f7, the
    probabilistic approach, f6, and the sort-based approach, f5.
    
    Given an integer N, tests correctness over an input list for 
    all unique pairs of missing integers X and Y such that X < Y <= N.

    For each pair, a new input list is created and shuffled trials
    times, as f5 has different behavior based on the order of items in 
    the input.
    
    Raises:
        AssertionError: At least one among f5, f6 and f7 is incorrect.
    """
    for lo in range(1,n+1):
    
        print(f"Testing missing pairs with {lo} as lo...")
    
        for hi in range(lo+1,n+1):
            for _ in range(trials):
                lst = [x for x in range(1,n+1) if (x!=lo and x!=hi)]
                shuffle(lst)
                assert (lo,hi) == f7(lst)
                assert (lo,hi) == f6(lst)
                assert (lo,hi) == f5(lst)  # Modifies input so do last.