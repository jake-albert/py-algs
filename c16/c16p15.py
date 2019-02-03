from random import randint

# c16p15

# Master Mind: The Game of Master Mind is played as follows:
#
# The computer has four slots, and each slot will contain a ball that is red
# (R), yellow (Y), green (G) or blue (B). For example, the computer might have
# RGGB (Slot #1 is red, Slots #2 and #3 are green, Slot #4 is blue).
#
# You, the user, are trying to guess the solution. You might, for example, 
# guess YRGB. When you guess the correct color for the correct slot, you get a
# "hit:' If you guess a color that exists but is in the wrong slot, you get a 
# "pseudo-hit:' Note that a slot that is a hit can never count as a 
# pseudo-hit.
#
# For example, if the actual solution is RGBY and you guess GGRR, you have one 
# hit and one pseudo-hit.
#
# Write a method that, given a guess and a solution, returns the number of 
# hits and pseudo-hits. 

##############################################################################

# The definition above leaves room for one clarification question: can 
# pseudo-hits be "reused" even if the solution has fewer instances of the
# color than was in the guess?

# For example, if the guess is BBYG and the solution RRRB, then there are two
# ways to count pseudo-hits. One would be to say that each of the B's in the 
# guess is a correct color, just in the wrong slot, meaning that the number of
# pseudo-hits is 2. Alternatively, there is a rule that once a slots in the 
# solution of a certain color have been "exhausted" by your guesses, further 
# guesses in the same color do not count as a pseudo-hits. So in the example, 
# there would be only one pseudo-hit.

# Admittedly, the first interpretation is a much more plausible reading of the
# instructions than the second, but I implemented a function that goes by the
# second interpretation since it seemed like slightly more of a challenge.

# This approach takes strings as input and works in only one pass of each.
# Because there are only four slots, the algorithm works in O(1) time with 
# O(1) space requirements.

# I assume that the input is correct (that it has 4 characters each which can
# be only from the set {"R","Y","G","B"}). Could also write a generalized 
# version of this algorithm for arbitrarily long code strings, or more color 
# choices, or both. In those cases, it would be wise to write a separate 
# function to convert strings to lists of integers according to some encoding.

def f1(guess,solut):
    """Returns the number of hits and pseudo-hits in a single guess in 
    the game Master Mind.
    
    Args:
        guess: A string with 4 chars only from set {"R","Y","G","B"}.
        solut: A string representing the correct answer. Also 4 chars,
               only from the set {"R","Y","G","B"}.
               
    Returns:
        A tuple of ints (hits, pseudo_hits). 
    """
    hits = 0   

    # Dictionary maps a character to a running count of times that the
    # character exists in 1. the guess, but does not match the solution 
    # at the same position, and 2. the solution, but does not match the 
    # guess character at the same position. I will call this a "mismatch."
    
    mismatch_counter = {sym : [0,0] for sym in ["R","Y","G","B"]}
    
    for i in range(4):
    
        g,s = guess[i], solut[i]
        
        if g == s:
            hits += 1
        else:            
            mismatch_counter[g][0] += 1            
            mismatch_counter[s][1] += 1
  
    # The total number of pseudo-hits for any given character is the 
    # MINIMUM of the mismatches of that character in the guess string, 
    # and the mismatches of that character in the solution string. Sum
    # over these values for each character to find total pseudo-hits.
        
    p_hits = sum([min(x[0],x[1]) for x in mismatch_counter.values()])    
    return hits, p_hits
    
# Testing on randomly-generated input below.
    
def test(n):
    """Produces output for n randomly generated guess-solution pairs. 
    Correctness may be checked by hand.
    
    Args:
        n: An int number of times to call the function.
    """ 
    for _ in range(n):
        
        guess, solut = random_sequence(), random_sequence()
        print(guess)
        print(solut)
        print(f1(guess,solut))
        
mapping = {0: "R", 1: "Y", 2: "G", 3: "B"} 
        
def random_sequence():
    """Generates one random 4-char sequence of colors."""
    return "".join([mapping[randint(0,3)] for _ in range(4)])