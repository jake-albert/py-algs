from operator import sub, mul, floordiv

# c16p09

# Operations: Write methods to implement the multiply, subtract, and divide
# operations for integers. The results of all of these are integers. Use only
# the add operator. 

##############################################################################

# We can subtract integers by repeatedly adding 1 and counting how many times 
# this must be done. This runs in O(|A-B|) time. This can be made more 
# efficient by incrementing by a value that starts at 1 but then doubles 
# itself on each iteration by adding itself to itself, and resetting on 
# "overflows" to 1 before starting again. Might revisit this later.

def my_sub(a,b):
    """Returns the value of a - b.
    
    Args:
        a: An int.
        b: An int.
    """ 
    min_val, max_val = min(a,b), max(a,b)
    res = 0

    change_val = 1 if a>b else -1
    while min_val < max_val:
        min_val += 1
        res += change_val
    return res
 
# We have now "unlocked" negating integers.
 
def neg(a):
    """Returns -1 * a.
    
    Args:
        a: An int.
    """
    return my_sub(0,a)
 
# We can multiply integers by repeatedly adding the first integer to a running
# sum the second integer number of times. Important to check whether values 
# are positive or negative. (Another faster approach would involve repeated 
# doubling of the first integer rather than summing to itself, but the below 
# focuses only on repeated addition by the same value.)

def my_mul(a,b):
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
            res += (added)
        return neg(res)

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
  
def my_floordiv(a,b):
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
    # need, so for simpler arithmetic we ensure that a and b are equal
    # to their absolute values.
    
    pos = True
    if a < 0: 
        a = neg(a)
        pos = not pos      
    if b < 0:
        b = neg(b)
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
    # cases where pos is False (ex. -8 // 3), account for the negative
    # floor by adding one to cur before negating (2 -> -3).
    
    if pos:
        return res
    else:
        return neg(res) if even_div else neg(res+1)
        
def test():
    """Tests some inputs."""   
    sub_cases = [( 5, 4),  #   1
                 ( 5,-4),  #   9
                 (-5,-4),  #  -1
                 (-5, 4),  #  -9
                 
                 ( 0, 1),  #  -1
                 (-6, 0),  #  -6
                 (18,18)]  #   0
                 
    mul_cases = [( 5, 4),  #  20
                 ( 5,-4),  # -20
                 (-5,-4),  #  20
                 (-5, 4),  # -20
                 
                 ( 0, 4),  #   0
                 (-5, 0)]  #   0
    
    div_cases = [( 5, 2),  #   2
                 (-5, 2),  #  -3
                 ( 5,-2),  #  -3
                 (-5,-2),  #   2
                 
                 (-8, 2),  #  -4
                 (-8, 3)]  #  -3
                 
    for my_fun, py_fun, cases in zip([my_sub,my_mul,my_floordiv],
                                     [sub,mul,floordiv],
                                     [sub_cases,mul_cases,div_cases]):
        for input in cases:
            my, py = my_fun(*input), py_fun(*input)
            try:
                assert my == py
            except:
                print(f"i: {input}, o: {my}, returned: {py}")