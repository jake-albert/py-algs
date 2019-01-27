# c16p11

# Diving Board: You are building a diving board by placing a bunch of planks
# of wood end-to-end. There are two types of planks, one of length shorter and 
# one of length longer. You must use exactly K planks of wood. Write a method 
# to generate all possible lengths for the diving board. 

##############################################################################

# It may be the case that shorter and longer can be both int or float types.
# If both shorter and longer can be assumed to be positive integers, then  
# the below algorithm uses range() to work in O(K) time. It first takes the 
# case of all K planks being of shorter length, then increases the length 
# by the amount that it would increase were one shorter plank replaced with 
# one longer plank. Since all K possible lengths must be generated, this 
# is the best conceivable runtime.  

def f1(k,shorter,longer):
    """Returns a list of all possible lengths of a board that can be 
    made out of exactly K planks, selecting from only two possible 
    lengths of planks.
    
    Args:
        k: A positive integer representing the number of planks.
        shorter: A positive integer length of the shorter plank.
        longer: A positive integer length of the longer plank.
        
    Returns:
        A list of all possible lengths as integers.
    """
    if k == 0: return [0]
    
    # Each time one longer plank replaces one shorter plank, the total 
    # length of the board increases by (longer-shorter)
    
    output = list(range(k*shorter,k*longer,longer-shorter))
    output.append(k*longer)
    return output

# The more general algorithm for any real number inputs below eschews the 
# range() function, which cannot be called with float arguments.

def f2(k,shorter,longer):
    """Returns a list of all possible lengths of a board that can be 
    made out of exactly K planks, selecting from only two possible 
    lengths of planks.
    
    Args:
        k: A positive integer representing the number of planks.
        shorter: A number that represents the length of the shorter plank.
        longer: A number that represents the length of the longer plank.
        
    Returns:
        A list of all possible lengths. If both shorter and longer are 
        integers, then these lengths are integers. Otherwise, they are 
        floats.
        
    Raises:
        ValueError: At least one of k, shorter, and longer is incorrect. 
    """  
    if shorter <= 0 or longer <=0:
        raise ValueError("shorter and longer must be positive")
    if shorter >= longer:
        raise ValueError("shorter must be shorter than longer")        
    if k < 0:
        raise ValueError("k must be positive.")
    elif k == 0:
        return [0]
    else:
        if isinstance(k,float) and not k.is_integer():
            raise ValueError("k must be an integer.")
     
    # Each time one longer plank replaces one shorter plank, the total 
    # length of the board increases by (longer-shorter)
     
    output = []
    option = k*shorter
    while option <= k*longer:
        output.append(option)
        option += longer-shorter
    
    return output