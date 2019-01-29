from operator import add, sub, mul, truediv
from random import randint

# c16p25

# Calculator: Given an arithmetic expression consisting of positive integers, 
# +, -, * and / (no parentheses), compute the result.
#
# EXAMPLE
# Input: 2*3+5/6*3+15
# Output: 23.5 

##############################################################################

# The text does not seem to give any indication of the format of the input. It
# seems most plausible that this would be a string of characters such as "5"
# or "6+87/23".

# If we are not so concerned with minimizing memory, then we could parse the
# full input string in order to populate some data structure such as a list 
# (for example, ["2","*","13","+","55","/","6","*","3"]), a linked list, or 
# stacks that would (perhaps) make implementing the calculator simpler. With 
# the linked list, for example, we could make one "scan" from left to right 
# that, for each "*" and "/" operator it encounters in a node, replaces the 
# previous node, current operator node, and following node with the result 
# of that computation, and then moves on, and then repeat this process with 
# "+" and "-" until only one node remains. This data structure would, of 
# course, require O(N) space.

# On the other hand, if we are concerned about optimizing memory usage (which 
# admittedly might not be a high priority in most use cases for this problem, 
# but could plausibly become a priority if inputs ever increase to having tens
# of thousands of integers), we can also compute the result using O(1) extra 
# space by carefully reading integers and operator symbols from the string and 
# aggregating them in the correct order. I implement that function.

# (Pedantically speaking, since there is no limit to the size of integers in 
# the input, it is possible that the input string consists of only one integer
# that must be read and stored by the function before returning, so in reality
# we can cap memory requirements only at O(logN), where N is the character 
# length of the input, even though the number of distinct integers and 
# operations that we allocate memory for is in O(1).)

# My function raises a ValueError when the input is invalid; that is, when it 
# cannot match the regex a(ba)*, where a is the string representation of  some
# positive integer, and b is one of "+", "-", "*", or "/".

# ALSO, an important note about associativity. We obviously must be careful to 
# get correct the order of operations in an expression like "3+2*2" and thus 
# cannot blindly calculate operations from left to right. But because we are 
# working with the true division operator and float results, the order that we
# compute results even within a sequence of "mutually associative" operations
# makes a difference as well: 
         
# >>> 69*31/59
# 36.25423728813559
# >>> (69*31)/59
# 36.25423728813559
# >>> 69*(31/59)
# 36.2542372881356
       
# In order to truly replicate the behavior of the Python interpreter, it is 
# important that we greedily compute operations from left to right whenever 
# possible, rather than perform these operatioins in a different order, even 
# though the fractional value of the result would not change (above, 2139/59).

# Alternatively, we could store a running tab of the result to return using 
# Pyhon's Fraction class, and then only at the end output a decimal form. In 
# that case, the relative order of multiplications and divisions would not 
# make a difference. (This appraoch might also be faster, as we would avoid 
# floating-point arithmetic until the end? I would have to look more into how
# the Fraction class implements its operations.)
       
def f1(exp):
    """Given a string representing an artihmetic expression of positive
    integers, computes and prints the result.
    
    Args:
        exp: A string. Should match the regex a(ba)*, where a is some 
        number of digits representing a positive integer, and b is one 
        of "+", "-", "*", or "/".
    
    Returns:
        An float if the division operator is in the input, and an
        integer otherwise.
        
    Raises:
        ValueError: exp is empty or is improperly formed.
        ZeroDivisionError: exp calls for dividing by zero.
    """
    if len(exp) == 0:
        raise ValueError("Empty expression, undefined result.")
    
    output, i = get_next_int(exp,0)
        
    if i == len(exp):
        return output
    
    # At all times, we keep track of a running value for the expression
    # as it is calculated from left to right, the operator and integer 
    # (the "argument") that follow, and the next operator after that 
    # (or None if no such operator exists).
    
    # out   op   arg  nop
    # 55    +    3    *    6   ...
    
    op, i = get_next_op(exp,i)   
    arg, i = get_next_int(exp,i)
    nop, i = get_next_op(exp,i)
  
    while nop is not None:
        
        # We aim to calculate (out op arg) as soon as we possibly can.
        # When op is * or /, we can do this immediately and "shift" op,
        # arg, and nop to the right. But when op is + -, we must first 
        # compute ALL consecutive * or / operatioins from nop to the  
        # right, which might include the final operation in the string.
        
        if (op is add) or (op is sub):
            while (nop is not add) and (nop is not sub):
                narg, i = get_next_int(exp,i)
                arg = nop(arg,narg)
                nop, i = get_next_op(exp,i)
                if nop is None:
                    return op(output,arg)
                        
        output = op(output,arg)
        op = nop
        arg, i = get_next_int(exp,i)
        nop, i = get_next_op(exp,i)
    
    return op(output,arg)
  
def get_next_int(exp,i):
    """Returns the integer beginning at the ith index in a string.
    
    Args:
        exp: A string.
        i: An int index where a positive integer is expected to begin.
        
    Returns:
        The integer value, and a new index 1 to the right of where the 
        integer ends in the string.
        
    Raises:
        ValueError: There is no positive integer at index i.
        IndexError: i is out of range.
    """
    if i == len(exp):
        raise ValueError(f"Integer expected at index {i}.")
    if not exp[i].isnumeric():
        raise ValueError(f"Non-numeric char found at index {i}.")
    
    val = 0
    while i < len(exp) and exp[i].isnumeric():
        val = val*10 + int(exp[i])
        i += 1
    return val, i
 
def get_next_op(exp,i):
    """Returns the operator represented at the ith index of a string, 
    or None if i is at the end of the string.
    
    Args:
        exp: A string.
        i: An int index where an operator symbol is expected.
    
    Returns:
        An function object or None, and min(i+1,len(exp)). 
    
    Raises:
        ValueError: There is an unexpected character at index i.
    """
    if i == len(exp):
        return None, i
    
    if exp[i] == "+":
        return add, i+1
    elif exp[i] == "-":
        return sub, i+1
    elif exp[i] == "*":
        return mul, i+1
    elif exp[i] == "/":
        return truediv, i+1
    else:
        raise ValueError(f"Failed to find valid operator at index {i}.")

 
def test(max_ops,trials,max_int):
    """Tests f1 against the Python interpreter's performance on 
    randomly generated input strings of increasing lengths.
    
    Args:
        max_ops: An int. Number of operations in longest test input.
        trials: An int. Number of strings to test per op count.
        max_int: An int. Highest value that may be part of a string.
    
    Returns:
        None. Prints any input with discrepancies between f1 and 
        interpreter.
    """
    for n_ops in range(max_ops+1):
        for _ in range(trials):
            str = generate_input(n_ops+1,max_int)
            
            if f2(str) != eval(str):
                print("f2 issue:",str)
    
def generate_input(c,max_int):
    """Returns a string represnting an arithmetic expression with c 
    random integers from 1 to max_int (inclusive), and c-1 operations 
    randomly selected from plus, minus, muliply, and divide.
    """
    ops = ["+", "-", "*", "/"]

    builder = []
    for _ in range(c-1):
        builder.append(str(randint(1,max_int)))
        builder.append(ops[randint(0,len(ops)-1)])
    builder.append(str(randint(1,max_int)))
    
    return "".join(builder)