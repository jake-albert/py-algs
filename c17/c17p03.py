from random import randint
from operator import mul
from functools import reduce
from statistics import stdev
from c17p02 import get_qs

# c17p03

# Random Set: Write a method to randomly generate a set of m integers from an
# array of size n. Each element must have equal probability of being chosen. 

##############################################################################

# I assume that we have access to a random number generator. (For the purposes
# of this problem, I assume that a call to this RNG takes O(1) time.)

# Rather than return a Python set object, which would remove duplicates if 
# there are duplicates in the input list, I choose to return a list 
# representing the set. 

# If we are allowed to modify the list, then we can simply shuffle the list 
# as was demonstrated can be done in O(N) time, then select the first M
# elements of the list. Better yet, we can simply halt the shuffle from c17p02
# early once M elements have been selected, making runtime O(M) and space 
# requirements O(1).

# To review the approach: We randomly select one element to be swapped with 
# the element in the first slot of the list, then randomly select from the 
# remaining elements one to swap with the second slot, and so on, M times.

# Once this is complete, the first M elements of the list will hold our set.
# We return a copy of the sublist containing those elements.

def f1(lst,M):
    """Generates a list of M elements from a list of size N, with each
    element having an equal probability of being chosen.
    
    Args:
        lst: A list. 
        M: An int.
        
    Returns: A list.
    
    Raises: 
        ValueError: M is either negative or greater than N.
    """
    if M > len(lst) or M < 0:
        raise ValueError("M must be from 0 to len(lst) inclusive.")

    for i in range(M):
        selection = randint(i,len(lst)-1)
        lst[i], lst[selection] = lst[selection], lst[i]
    
    return lst[:M]

# On the other hand, what if we cannot modify the list? One workaround would 
# be to copy the list to another one in O(N) time and then perform the same 
# O(M) algorithm above, overall taking O(N) time and O(N) space.

# A different kind of approach that does not modify the list (or rely on
# copying it) is quite simple: repeatedly select random indices from 0 to N-1
# inclusive until M unique ones have been selected. We maintain a set of 
# already selected indices in the list, so O(M) space is required. 

def f2(lst,M,count=False):
    """See f1 docstring.
    
    When count is True, returns the number of RNG calls it took to
    create the list instead of the list itself.
    """
    if M > len(lst) or M < 0:
        raise ValueError("M must be from 0 to len(lst) inclusive.")

    index_set = set()
    output = []
    if count: calls = 0
    
    while len(index_set) < M:
        if count: calls +=1
        i = randint(0,len(lst)-1)
        
        if i not in index_set:
            index_set.add(i)
            output.append(lst[i])
    
    return calls if count else output
 
# Describing the expected runtime of this approach is trickier. When we first 
# attempt to find an index, the index_set is empty, so there is a 100% chance 
# of the RNG returning an index that has not yet been found. The expected 
# number of calls to the RNG is 1.
 
# Following this, we attempt to sample another unique index, and this time 
# there is a probability of 1/N of failing to find a unique one. Probability 
# of success, then, is (N-1)/N, meaning our expectation of calls to find the 
# second element its inverse, or N/(N-1).
  
# Altogether, then, the expected number of calls to get M unique indices is 
# equal to the summation from i=0 while i<M of (N)/(N-i). This value is in 
# O(M*N/(N-M)), which has interesting behavior in that it approaches O(M) as
# N increases towards infinity. (This makes sense, given that on larger N, the
# probability of the RNG repeating indices becomes smaller.)

# On the other hand, as M approaches N, the expected number of calls increases 
# sharply. This also makes sense -- when all but one index has been selected 
# in a very large list, we should expect N RNG calls in order to return that 
# one index. We could improve on this approach, then, in cases when M is 
# greater than N/2. We could select for N-(M/2) items to EXCLUDE from the list
# and take O(N) time to generate a list from those exclusion indices.

# We empirically (but informally) confirm this expected number of calls below.
# As the number of trials that for each experiment increases, the number of 
# calls to the RNG by f2 approaches the value of the summation:

def expectation(N,M):
    """Calculates the expected number of RNG calls required in f2 to 
    select M elements from N."""
    ans = 0
    
    for i in range(M):
        ans += N / (N-i)
    
    return ans

def expectation_test(max_N=100,trials=100000):
    """Compares number of calls to RNG in f2 with expectations.
    
    Args:
        max_N. Largest list size to test.
        trials. Number of times to test f2 on a unique N,M pair.
    """
    legend = "  N    M     exp     act"
    print(legend)
    print("-"*len(legend))
    
    input = []
    for N in range(1,max_N+1):
        input.append(N)
        
        # Test M only up to half of N, given the discussion above.
        
        for M in range(1,N//2+1):
        
            calls = 0
            for _ in range(trials):
                calls += f2(input,M,count=True)
            exp_calls = expectation(N,M)  
           
            print(f"{N:3}  {M:3}  {exp_calls:6.2f}  {calls/trials:6.2f}")
    
# To see the performance of f1 and f2 on various inputs, we keep track of the 
# number of distinct subsets that can be generated, which is N choose M or 
# N!/(M!*(N-M)!).

def ncr(N,M):
    """Returns (N)C(M). Adapted from: http://tinyurl.com/y36aknv4."""
    M = min(M,N-M)
    numer = reduce(mul,range(N,N-M,-1),1)
    denom = reduce(mul,range(1,M+1),1)
    return numer // denom
 
def test():
    """Tests subset functions over some sample inputs."""
    trials = 1000000
    inputs = [( 5,2),
              ( 7,3),
              (20,2),
              (20,7)]
              
    for N,M in inputs:
        for f in [f1,f2]:
        
            print("-" * 79)
            print(f"{f.__name__} results: Subsets size {M} from {N}.")
            print("----------------------------------")
            test_function(N,M,trials,f)
            
def test_function(N,M,trials,f):
    """Tests a subset function and prints some rudimentary results.

    Args:
        N,M: Ints, as above.
        trials: Number of experiments to perform.
        f: A subset function.
    """
    occurrences = {}

    for t in range(trials):
    
        if trials > 10 and t % (trials//10) == 0:
            print(f"Trial:{t:10} ({100*t/trials:2.0f}%)")
            
        lst = list(range(N))
        result = f(lst,M)
        result.sort()  # All identical subsets have same sorted form.
        
        key = tuple(result)
        if key not in occurrences:
            occurrences[key] = 1
        occurrences[key] += 1
    
    print("\nRESULTS:\n")
    tot = ncr(N,M)
    print(f"Expected distinct subsets: {tot}")
    print(f"Actual distinct subsets  : {len(occurrences.items())}\n")   
    
    print(f"Expected hits per subset           : ~{trials//tot:8}")
    lo_q, med, hi_q = get_qs(occurrences.values())     
    print(f"Lower quartile of subset hits      :  {lo_q:8}")
    print(f"Median                             :  {med:8}")
    print(f"Upper quartile                     :  {hi_q:8}\n")
    
    print(f"Expected probability of each subset: {100/tot:.4f}%")
    sigma = stdev([100*occ/trials for occ in occurrences.values()])
    print(f"StdDev of probabilities: {sigma:.4f}%")
        
    if tot <= 100:  # Do not print all subsets when tot is too large.
        print("")
        print("Subset: Hits (Percentage)") 
        for k,v in sorted(occurrences.items()):
            print(f"{k}: {v:6} ({100*v/trials:7.4f}%)")