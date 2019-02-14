from operator import add

# c17p01

# Add Without Plus: Write a function that adds two numbers. You should not 
# use + or any arithmetic operators. 

##############################################################################

# The word "numbers" is a little unclear here. Can the input be any real 
# numbers? Expressed as ints? Or floats, or both?

# I assume that in this problem the inputs can be integers, negative or 
# non-negative. To put constraints on the problem, I implemented a class below
# that converts Python ints to 2's complement, 32-bit signed integers, and 
# thus will need to handle overflow and underflow errors when I add them.

class MySignedInt:
    """Simulates a 2's complement, 32-bit signed integer.
    
    Attributes:
        bits: An int of bit length 32. Represent the signed integer,
          with the 31st bit from 0 as the sign bit. (0 for positive 
          numbers, 1 for negative numbers.)
        disp: A list of strings "1" and "0" for displaying the integer.
          Created and stored on first call to display() method.
        val: An int equal in value to the signed integer.
        modified: A Boolean. Indicates that val must be updated.
    """
    
    BIT_NUM     = 32
    COMPLEMENT  = 2**(BIT_NUM-1)
    UPPER_LIMIT = COMPLEMENT - 1
    LOWER_LIMIT = -1 * COMPLEMENT
    
    def __init__(self,n):
        """Creates a MySignedInt instance with value n."""
        self.bits = self._convert_to(n)
        self.disp = None
        self.val = None
        self.modified = False
        
    def display(self):
        """Prints a string representation of the 32 bits."""
        if self.disp is None:
            trailing_zs = self.BIT_NUM-(len(bin(self.bits))-2)
            self.disp = ["0" for _ in range(trailing_zs)]
            self.disp.extend((b for b in bin(self.bits)[2:]))    
        print(" ".join(self.disp))
    
    def get_value(self):
        """Returns the value of the signed integer."""
        if self.val is None or self.modified:
            self.val = 0
            
            # Compute the value of the first 31 bits, and convert to
            # its 2's complement iff the signed bit is 1.
            
            for place in range(self.BIT_NUM-1):
                if self.bits & (1<<place) != 0:
                    self.val |= 1 << place
            
            if self.bits & (1<<self.BIT_NUM-1) > 0:
                self.val -= self.COMPLEMENT 
            
            self.modified = False
                
        return self.val
    
    def _convert_to(self,n):
        """Converts an int n to a MySignedInt."""
        if n > self.UPPER_LIMIT or n < self.LOWER_LIMIT:
            raise ValueError(f"Unable to convert {n}. Out of range.")
        
        # A negative number -x in 2's complement has non-signed bits
        # whose value is equivalent to (COMPLEMENT - x).
        
        # For example, in a 4-bit signed integer, the number -5 is 
        # expressed as a 1 sign bit, followed by the bits for 
        # (COMPLEMENT - 5), or (8-5), or 3. "1011"
        
        if n < 0:
            return self._val_to_bits(self.COMPLEMENT+n,True)
        else:
            return self._val_to_bits(n,False)

    def _val_to_bits(self,n,neg):
        """Converts a positive integer to its bit representation, and
        changes the sign bit to 1 iff neg is True."""
        output = 0
        
        for place in range(self.BIT_NUM-1):
            if n & (1<<place) != 0:
                output |= 1 << place
        
        if neg:
            output |= 1 << (self.BIT_NUM-1)
        
        return output
    
    def _sign_bit_is_zero(self):
        """Returns True iff sign bit is 0, False otherwise."""
        self.modified = True
        return self.bits & (1<<(self.BIT_NUM-1)) == 0
    
    def _sign_bit_to_one(self):
        """Sets the sign bit to 1."""
        self.modified = True
        self.bits |= 1 << (self.BIT_NUM-1)

# One way to add the two numbers is to simulate adding them bitwise at the
# logic gate level, using an overflow bit. All the wrapping of the above class
# to simulate a 32-bit signed integer means that executions on it will be many
# orders of magnitude slower than actual bit manipulation, but it is helpful 
# to demonstrate correctness over both positive and negative inputs.

# In order to write this addition with as little duplicated code as possible,
# it was helpful to try examples on 4-bit signed integers. 2's complement 
# makes adding numbers with different signs (i.e. subtracting) quite simple --
# regardless of the sign bits, we always add the non-sign bits the same way:

# 4  +  3  | "0100" + "0011" --> "0111"
# 4  + -3  | "0100" + "1101" --> "0001"
        
def f1(a,b):
    """Simulates bitwise addition of integers a and b.
    
    Note: The + operator may be called to change a and b to MySignedInt
    instances, but the actual addition over these simulated signed ints 
    does not use the + operator, which is what is important.
    
    Args: 
        a,b: Ints that can be expressed as 32-bit signed integers.
        
    Returns:
        An int.
        
    Raises:
        ValueError: At least one of a and b is out of range.
        OverflowError: Sum resulted in either over or underflow.
    """
    a, b = MySignedInt(a), MySignedInt(b)
    output = MySignedInt(0)
    overflow = False 
        
    for place in range(a.BIT_NUM-1):
        
        a_bit = a.bits & (1<<place) != 0
        b_bit = b.bits & (1<<place) != 0
        
        # Python 3 allows us to calculate bitwise logic over Booleans. 

        output.bits |= ((a_bit^b_bit)^overflow) << place
        overflow = (a_bit and b_bit) or    \
                   (a_bit and overflow) or \
                   (b_bit and overflow)
        
    # If both a and b are non-negative, an overflow bit of 1 indicates
    # overflow error.
    
    if a._sign_bit_is_zero() and b._sign_bit_is_zero():
    
        if overflow:
            raise OverflowError("OVERFLOW ERROR -- Too Positive")
        else:
            return output.get_value()
    
    # By contrast, if both a and b are negative, then an overflow bit
    # of 0 is what indicates underflow error.
    
    elif (not a._sign_bit_is_zero()) and (not b._sign_bit_is_zero()):
    
        if overflow:
            output._sign_bit_to_one()
            return output.get_value()
        else:
            raise OverflowError("UNDERFLOW ERROR -- Too Negative")
        
    # When a and b are of different signs, then the output is certainly 
    # within bounds, and the overflow bit determines the sign.
    
    else:
        
        if overflow:
            return output.get_value()
        else:
            output._sign_bit_to_one()
            return output.get_value()

# As expected, the lowest positive and highest negative sums that induce 
# overflow and underflow errors are the upper and lower bounds of integers 
# that can be expressed as 32-bit signed integers.
            
def error_tests():
    """Tests that the upper and lower bounds are correct."""
    inputs = [(   2**31-1, 0),  # Highest possible sum.
              (   2**31-1, 1),  # One over.
              (-1*2**31  , 0),  # Lowest possible sum.
              (-1*2**31  ,-1)]  # One under.
    
    for a,b in inputs:
        try:
            print(f"{a} + {b} = {f1(a,b)}")
        except OverflowError as e:
            print(f"{a} + {b} = {e}")
            
# The book's recursive solution was elegant and works on both positive and
# negative integers as well. It uses XOR to find the "sum"  portion of the 
# result, and AND (shifted to the left) to determine the carry portion, and 
# then computes the sum of these. 

# In order to make the operations work on Python ints, I again needed to 
# convert inputs to MySignedInt instances, as well as write little XOR, AND, 
# and shift operations on MySignedInt instances. As a result, the calculations
# are quite slow but as a proof of concept it works fine.

# (I do not handle overflow and underflow errors for this function. f2 simply
# returns an incorrect sum.)
            
def my_xor(a,b):
    """Returns a MySignedInt with value equal to a ^ b."""
    output = MySignedInt(0)
    output.bits = a.bits ^ b.bits
    return output
    
def my_and(a,b):
    """Returns a MySignedInt with value equal to a & b."""
    output = MySignedInt(0)
    output.bits = a.bits & b.bits
    return output
    
def shifted_left(a):
    """Returns a MySignedInt with value equal to a << 1."""
    output = MySignedInt(0)
    output.bits = a.bits << 1
    return output
            
def f2(a,b):
    """See f1 docstring."""
    def recurse(a,b):
        if b.get_value() == 0: return a.get_value()
        sum = my_xor(a,b)
        carry = shifted_left(my_and(a,b))   
        return recurse(sum,carry)
    
    return recurse(MySignedInt(a),MySignedInt(b))
    
def test(n):
    """Tests addition of all pairs of unique integers -n to n."""
    for a in range(-1*n,n):
        for b in range(-1*n,n):
            assert a+b == f1(a,b)
            assert a+b == f2(a,b)