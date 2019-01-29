import sys
sys.path.append('..')
from data_structs import Stack
from itertools import chain

# c16p08

# English Int: Given any integer, print an English phrase that describes the
# integer (e.g., "One Thousand, Two Hundred Thirty Four").

##############################################################################

# I emulate the formatting of the example return string. (No "and", comma use,
# capitalization, no-hyphens.) I also follow this formatting in the rare cases
# where it reads a bit unnaturally, possibly due to our quick reading of year 
# names ("Two Thousand, Nineteen"). While I could identify these instances and 
# omit a comma, I chose not to here for consistency.

# First, it is worth asking about the max expected value of the integer. If it
# is a 4-byte signed integer then it has a max absolute value between 2 and 3 
# billion, but we can handle larger integers into the trillions, quadrillions,
# etc. by storing these strings. We could in addition have an approach that
# prints out scientific notation for larger values than that.

# The lists below hold strings for number names. Some buffer values are used 
# for easier indexing (for example, such that "Twenty" is at decades[2]).

digits  = ["","One","Two","Three","Four","Five","Six","Seven","Eight","Nine"]
teens   = ["Ten","Eleven","Twelve","Thirteen","Fourteen","Fifteen","Sixteen",\
           "Seventeen","Eighteen","Nineteen"]
decades = ["","","Twenty","Thirty","Forty","Fifty","Sixty","Seventy",\
           "Eighty","Ninety"]
groups  = ["","Thousand","Million","Billion","Trillion","Quadrillion",\
           "Quintillion","Sextillion","Septillion","Octillion"]
    
def f1(n):
    """Prints an English phrase that describes an input integer.
    
    Args:
        n: Any int with absolute value less than one nonillion (10^30).
        
    Raises:
        ValueError: n has absolute value greater than 10^30.
    """   
    if n == 0:
        print("Zero")
        return

    neg = True if n < 0 else False
    n = abs(n)
    
    output_stack = Stack()
    three_stack = Stack()
    group = -1
    
    # Divide n into "groups" of three digits: the pre-thouands, then 
    # thousands, then millions, billions, and so on. For each group, 
    # generate a string such as "Two Hundred Twelve" and push onto a
    # stack s.t. groups with greater significance will be output first.   
    
    while n > 0:
    
        for i in range(3):
            three_stack.push(n % 10)
            n //= 10

        hundreds = three_stack.pop()
        tens     = three_stack.pop()
        ones     = three_stack.pop()
        
        output_stack.push(three_digit_string(hundreds,tens,ones))
        group += 1
   
    print_output(output_stack,neg,group)
    
def three_digit_string(hundreds,tens,ones):
    """Given three integers 0-9 inclusive, prints the string 
    representing the number formed by these numbers interpreted as
    digits when read out loud.
    
    Args:
        hundreds: An int representing the hundreds digit.
        tens: An int representing the tens digit.
        ones: An int representing the ones digit.
        
    Returns:
        A string.
        
    Raises:
        IndexError: A digit greater than 9 has been input.
    """
    output_list = []
    
    # When hundreds digit is zero, go immediately to tens digit.
    
    if hundreds > 0:
        output_list.append(digits[hundreds])
        output_list.append("Hundred")
    
    # If the tens digit is one, then strings like "Twelve" and
    # "Seventeen" are used. If not, strings like "Twenty" and "Seventy"
    # are used, and the ones digit is independently consulted.
    
    if tens == 1:
        output_list.append(teens[ones])
    else:
        if tens > 0:
            output_list.append(decades[tens])
        if ones > 0:
            output_list.append(digits[ones])
    
    return(" ".join(output_list))
    
def print_output(output_stack,neg,group):
    """Prints an English phrase that describes an integer.
    
    Args:
        output_stack: A Stack inistance loaded with strings of 3-digit 
          groups, with the most significant group at the top.
        neg: A Boolean. True if negative, False otherwise.
        group: An int representing the highest "group" (thousands,
          millions, etc. that the integer encompasses.
        
    Raises:
        ValueError: Integer to print has absolute value greater than 10^30.
    """
    output_list = []  # List of strings to be joined at the end.
    
    if neg:
        output_list.append("Negative ")
      
    comma = False  # Do not print comma until first group is appended.
        
    while not output_stack.is_empty():
    
        group_description = output_stack.pop()
        
        # Skip the group and group name altogether if "000". For 
        # example, "1,000,678" should be "One Million, Six Hundred 
        # Seventy Eight", not "One Million, Zero Thousand, Six 
        # Hundred Seventy Eight".
        
        if len(group_description) > 0:
            
            if comma:
                output_list.append(", ")
        
            output_list.append(group_description)
            output_list.append(" ")
        
            # Append a group name only if "Thousand" or above
            
            if group > 0:
                try:
                    output_list.append(groups[group])
                except IndexError:
                    raise ValueError("Input must have abs. value < 10^30.")
                    
        group -= 1
        comma = True
    
    print("".join(output_list))
    
def test():
    """Tests various cases."""
    inputs = chain(range(1,150,7),  \
                   [0,              \
                    1006,           \
                    7917,           \
                    4587,           \
                    10345,          \
                    816789,         \
                    -111222333444,  \
                    1000333000555,
                    1000000008000000000000005])
                    
    for input in inputs:
        print(f"{input}: ",end="")
        f1(input)   