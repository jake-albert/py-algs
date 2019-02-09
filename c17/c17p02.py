from random import randint
from math import factorial
from statistics import mean, stdev

# c17p02

# Shuffle: Write a method to shuffle a deck of cards. It must be a perfect 
# shuffle-in other words, each of the 52! permutations of the deck has to be
# equally likely. Assume that you are given a random number generator which is
# perfect.

##############################################################################

# I assume that the perfect random number generator outputs random integers in 
# any specified range. I use Python's randint() function to simulate the RNG, 
# and abstract a deck of cards as a list of length 52. (In fact, this solution
# works to shuffle Python lists of any length.)

# First, we must pick with equal probability some card out of the 52 to occupy
# the "top" of the deck, or the 0th-indexed position in the list. Having done 
# this, we need to pick one of the the remaining 51 cards with equal 
# probability to occupy the second position, and so on. We can do this in 
# place on the list by swapping values. 

# Assuming that each call to randint() returns in O(1) time, this shuffle 
# algorithm runs in linear time to length of the input. Since it is written
# iteratively rather than recursively, it requires O(1) memory.

def f1(lst):
    """Shuffles a list of length N so that all N! permutations are
    equally likely. The list is shuffled in place. 
    
    Args:
        lst: A list of objects.
    """
    for i in range(len(lst)-1):  # No need swap the final value.
        selection = randint(i,len(lst)-1)
        lst[i], lst[selection] = lst[selection], lst[i]

def test(n,trials):
    """Tests the shuffle function and returns some rudimentary results.

    Args:
        n: An int. The length of the list to shuffle.
        trials: An int. The number of shuffles to perform.
    """
    occs = {}

    for t in range(trials):
    
        if trials > 10 and t % (trials//10) == 0:
            print(f"Trial:{t:10} ({100*t/trials:2.0f}%)")
            
        lst = list(range(n))
        f1(lst)
        
        key = tuple(lst)  # Hashable version of the shuffle.
        if key not in occs:
            occs[key] = 1
        occs[key] += 1
    
    print("\nRESULTS:\n")
    fact = factorial(n)
    print(f"Expected distinct shuffles: {fact}")
    print(f"Actual distinct shuffles  : {len(occs.items())}\n")   
    
    print(f"Expected hits per shuffle           : ~{trials//fact}")
    print(f"Expected probability of each shuffle: {100/fact}")
    
    if n <= 5:  # Do not print all shuffles when n! is large.
        print("")
        print("Shuffle: Hits (Percentage)") 
        for k,v in sorted(occs.items()):
            print(f"{k}: {v} ({100*v/trials:.4f}%)")
        
    print("")
    sigma = stdev([100*occ/trials for occ in occs.values()])
    print(f"StdDev of probabilities: {sigma:.4f}%")