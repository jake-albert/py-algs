# c17p03

# Random Set: Write a method to randomly generate a set of m integers from an
# array of size n. Each element must have equal probability of being chosen. 

##############################################################################

# if we are allowed to modify the list, then this is quite similar to perfoming
# the shuffle from the previous problem, except we halt after making m swaps. 
# That way, it runs in time O(m). 

from random import randint

def f1(lst,m):

    if m > len(lst) or m < 0:
        return

    result = []

    for i in range(m):
        selection = randint(i,len(lst)-1)
        lst[i], lst[selection] = lst[selection], lst[i]
        result.append(lst[i])
    
    return result

# if we cannot modify the list, then we would be able to copy it to another array
# in O(n) time and then pefrom the same algorithm as above, making the overall runtime 
# equal to O(n) time and requiring O(n) space.

# python's random sampling of an element from a set takes O(n) time so we need to 
# avoid that. Another way would be to keep a set of "forbidden" values and repeatedly
# sample randomly from the indices until we have not hit one in the forbidden set. 

# when we first sample to get the first element, there is no forbidden element so 
# expected number of times to sample is 1. Following this, there is another sample 
# to get the next element, and there is a 1 in n chance we hit the same one. So there 
# is a n-1 in n chance we are good, and expected number of calls of n over n-1

# expected total number of calls to get it is equal to the summation from i=0 
# while i<m of (n)/(n-i)

def expectation(n,m):

    ans = 0
    
    for i in range(m):
        ans += n / (n-i)
    
    return ans

# this number is certainly in O(nm), but there might also be a tighter bound.

# As n approaches infinity, the number of calls to randint appraoches m

# another thing to note is that the probablity of any one element being put in 
# the subset is equal to (n-1)C(m-1) / (n)C(m) which equates to m/n. 
    
# from https://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python
# calculates n! / (k! times (n-k)!)
import operator as op
from functools import reduce

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom

from statistics import mean, stdev
    
def test(n,m,trials,f):

    occurrences = {}

    for t in range(trials):
    
        if t % (trials//10) == 0:
            print(f"Trial #{t}")
            
        lst = list(range(n))
        result = f(lst,m)
        
        # sort the result so that the same set has the same signature
        result.sort()
        
        key = tuple(result)
        if key not in occurrences:
            occurrences[key] = 1
        occurrences[key] += 1
    
    tot = ncr(n,m)
    print(f"\n{len(occurrences.items())} distinct shuffles, expected is {n}C{m} or {tot}")
    mu, sigma = mean(occurrences.values()), stdev(occurrences.values())
    print(f"Expected hits per combination is {trials/tot}.\nMean: {mu} StdDev: {sigma}")