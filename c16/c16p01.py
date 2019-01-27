# c16p1

# Number Swapper: Write a function to swap a number in place (that is, without
# temporary variables). 

##############################################################################

# An important first question to consider is whether the input number is of 
# a set type such as int or float, as different approaches may have different
# behavior on different types of input. 

# My first approach takes advantage of the numbers having a set difference and
# thus is correct for both int and float inputs. It runs using a constant 
# number of operations and stores no additional variables.

def f1(a,b):
    """Prints a pair of input numbers, then swaps their values and 
    prints again.
    
    Args:
        a: The first number.
        b: The second number.
    """   
    print(a,b) # Before swapping
    
    a -= b   # "a" now refers to a-b
    b += a   # "b" now refers to b+(a-b) = a 
    a -= b   # "a" now refers to (a-b)-a = -b
    a *= -1  # "a" now refers to b
    
    print(a,b) # After swapping
    
# An additional approach works at the bit level. Two bits in the same position
# must be swapped only when one is 1 and the other 0 -- in other words, only 
# when they XOR to 1. We could traverse the bits of each number, swapping 
# bits when necessary, in an algorithm that runs in O(log(max(a,b))) time.
 
# Of course, we could argue that if the incoming numbers are of a set length,
# such as 32-bit unsigned integers, that this is also an O(1) time solution.
# Like the above, works on both int and float inputs.