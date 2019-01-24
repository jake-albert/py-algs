# c16p9

# Operations: Write methods to implement the multiply, subtract, and divide
# operations for integers. The results of all of these are integers. Use only
# the add operator. 

##############################################################################

# We can subtract integers by repeatedly adding 1 and counting how many times 
# this must be done. This runs in O(a-b) time. I think this can be made more 
# efficient by using a counter that starts with value a, and then doubles 
# itself at each iteration by adding itself to itself until it cannot do this
# any longer. Might revisit this later.

def sub(a,b):
    """Return the value of a - b.
    
    Args:
        a: An int.
        b: An int.
    """
    
    min_val, max_val = min(a,b), max(a,b)
    res = 0

    while min_val < max_val:
        min_val += 1
        res += 1
    return res if a>b else -1*res
        
# We can multiply integers by repeatedly adding the first integer to a running
# sum the second integer number of times. Important to check whether values 
# are positive or negative. (Another faster approach would involve repeated 
# doubling of the first integer rather than summing to itself, but the below 
# focuses only on repeated addition by the same value.)

def mul(a,b):
    """Return the value of a * b.
    
    Args:
        a: An int.
        b: An int.
    """
    
    res = 0
    
    # To ensure we take as few steps as possible, find the value with 
    # the lowest absolute value, and make this the "iterator". The  
    # other value will be the value that we repeatedly add. This makes 
    # a big difference when we are multiplying, say, 2 times 2354657.
    
    num_times, added = (a,b) if abs(a) < abs(b) else (b,a)
    
    # If multiplying by a non-negative number, count down. Otherwise, 
    # count up.
    
    if num_times >= 0:
        while num_times > 0:
            num_times += -1
            res += added
        return res
        
    else:
        while num_times < 0:
            num_times += 1
            res = sub(res,added)
        return res

# For integer division of b into a, we need to confirm how to handle cases
# when a or b or both are negative values. In Python 3, we see the following
# results in interactive mode:
#
#
# >>> 5 // 2
# 2
# >>> -5 // 2
# -3
# >>> 5 // -2
# -3
# >>> -5 // -2
# 2
#
# In other words, the result is the floor() of the float result of the 
# division. We replicate this behavior below without using floor().
  
def div(a,b):
    """Return the value of a // b.
    
    Args:
        a: An int.
        b: An int.
    
    Raises:
        ZeroDivisionError: b is zero.
    """
    
    if b == 0:
        raise ZeroDivisionError
    
    # Ensure that pos is False iff only one of a or b is negative. 
    # this Boolean preserves the only information about sign that we 
    # need, so for simpler arithmatic we ensure that a and b are equal
    # to their absolute values.
    
    pos = True
    if a < 0: 
        a = mul(a,-1)
        pos = not pos      
    if b < 0:
        b = mul(b,-1)
        pos = not pos

    # Repeatedly add the divisor to cur until cur surpasses the 
    # dividend. 
        
    res = 0
    cur = b
    even_div = False
    
    while cur <= a:
        
        if cur == a:
            even_div = True
        
        res += 1
        cur += b
    
    # When pos is False and there is an even division (ex. -8 // 2),
    # return simply the negated value of cur (4 -> -4). In all other 
    # cases where pos is Fasle (ex. -8 // 3), account for the negative
    # floor by adding one to cur before negating (2 -> -3).
    
    if pos:
        return res
    else:
        return mul(res,-1) if even_div else mul(res+1,-1)