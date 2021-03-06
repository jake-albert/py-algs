from math import floor, ceil    

# c16p07

# Number Max: Write a method that finds the maximum of two numbers. You should
# not use if-else or any other comparison operator. 

##############################################################################

# This first approach exploits the fact that that 0 to the 0th is treated as 
# 1 in python 3. But it does not work when a == b, or with negative values.

def f1(a,b):
    """Returns the maximum of two numbers.
    
    Args:
        a: A positive int or float.
        b: A positive int or float unequal to a.
    
    Returns:
        An int if both inputs are ints, and a float otherwise.
    """  
    return ((0 ** (a // b)) * b) + ((0 ** (b // a)) * a)
    
# The second approach exploits the fact that a-b is negative when b is larger, 
# positive when a is larger, and 0 when a is equal to b.
        
def f2(a,b):
    """Returns the maximum of two numbers.
    
    Args:
        a: An int or float.
        b: An int or float.
    
    Returns:
        A float.
    """
    
    # Set "max" to equal either the max value, or 2a if a equals b. 
    # Then set "min" to either the min value, or 2a if a equals b. 
    # When a>b, a-b>0, so floor(2 to the (a-b)) is greater than 1, 
    # whereas when a<b, a-b<0, so floor(2 to the (a-b)) is 0. 
    
    max = (a * ceil(floor(2 ** (a-b)) / (2 ** (a-b)))) + \
          (b * ceil(floor(2 ** (b-a)) / (2 ** (b-a))))      
          
    min = (b * ceil(floor(2 ** (a-b)) / (2 ** (a-b)))) + \
          (a * ceil(floor(2 ** (b-a)) / (2 ** (b-a))))      
          
    # If min is equal to max, then a equals b, so return max / 2. 
    # Otherwise, return max. 
          
    return max / (ceil(floor(2 ** (min-max)) / (2 ** (min-max))) + 1)
    
# The second approach uses exponentiation so can lead to memory overflow for 
# large inputs. The final approach exploits the fact that int type numbers 
# have a signed bit that can be determined in O(logN) time for large integers. 
# Because Python integers work with arbitrary precision, there is fewer "edge 
# case" handling than would be required if we were working with integers of 
# set length, such as 32-bit signed integers.

# For float inputs, more steps would be needed to get a bit representation of 
# the input involving other Python libraries.
    
def f3(a,b):
    """Returns the maximum of two integers.
    
    Args:
        a: An int.
        b: An int.
    
    Returns:
        An int.
    """
    diff = a-b
    val = (diff)>>(diff.bit_length())  # -1 if b>a, 0 otherwise
    return -1* (val*b + ~val*a)        # ~1 results in 0, so one term removed.