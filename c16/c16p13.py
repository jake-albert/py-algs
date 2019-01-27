# c16p13

# Bisect Squares: Given two squares on a two-dimensional plane, find a line 
# that would cut these two squares in half. Assume that the top and the bottom
# sides of the square run parallel to the x-axis.  

##############################################################################

# It might help to ask whether what is wanted here is a line, as in a line 
# that extends without and end in two directions, or a line segment that ends
# where it intersects with the outermost sides of the given squares. I am 
# assuming that the desire is for a LINE, not a LINE SEGMENT.

# In order to define a unique square with top and bottom sides parallel to the
# x-axis, all we need are TWO values: a CENTER point, and also a SIDE LENGTH. 
# Let's say that the input is in the form (p, s), where p is a point on the 2D
# plane and s is a positive number representing the side length. 

# We actually do not even need to know the side legnth. A line that runs 
# through the center of both squares can be demonstrated to cut both squares
# into equal halves. These two halves are either isoceles triangles, or
# trapezoids, and the areas and other dimensions of both can be shown to have
# the same dimensions, area etc.

# We return the line in the form of a Line object. The equation is in the form 
# of ny=mx+b, or the slope-intercept form. If vertical, then n is always 0 and
# m is 1, so as to make the form 0y = 1x + b. The goal here is to keep the 
# form of the line consistent for all methods that work with linear equations. 
# If non-vertical, then n is always 1. This also guarantees that every line 
# has a unique representation as a Line object.

# Because the signature values are floats that result from division, I needed
# to define equivalency between two lines, and two approaches seemed possible. 
# One was that any two lines whose signature values are within some absolute 
# or relative threshold of each other are defined to be equivalent. As an 
# example of an absolute threshold: "If the values are within 0.00001 of each
# other, then they are equivalent." 

# The second approach is to, upon normalizing the values for a line, round
# or truncate immediately to a specific place, and then compare and hash the
# values as normal. The two approaches lead to different interpretations. For
# instance, say m1 is 4.568 and m2 is 4.572. With an absolute threshold of
# 0.005, then m1 and m2 are "wihtin range" of each other and thus would be
# considered equivalent, but if they are truncated to the hundredths place 
# then this would not be the case. (4.56 and 4.57). Of course, rounding 
# results in different results. (4.562 and 4.566, for example.)

# I am not sure which approach is more widely accepted, but it seems that 
# with a sufficiently small threshold or significantly precise place of 
# truncation, we can "capture" all of the floats to a specific precision 
# that we want to be considered equivalent, so I opted for the second option
# which is more straightforward to program, using the round() function. 

class Line:
    """Line class. Represents an equation in slope-intercept form: 
    ny = mx + b.
    
    Attributes:
        p: An integer indicating rounding place during normalization.
        n: A float that is 0.0 if line is vertical and 1.0 otherwise. 
        m: The float slope of the line. 1.0 if line is vertical.
        b: The float y-intercept of the line.
        sig: A tuple (n,m,b) signature a line for comparisons. 
    """
    
    p = 10 
    
    def __init__(self,n,m,b):
        """Inits Line with normalized n,m,b, and signature."""
        n,m,b = self.normalize(n,m,b)
        self.n   = float(n)
        self.m   = float(m)
        self.b   = float(b)
        self.sig = (self.n,self.m,self.b) 
    
    def normalize(self,n,m,b):
        """Ensures that n is either 1.0 or 0.0, and that if n is 0.0
        then m is 1. Unique lines thus have only one representation.
        Rounds values to a specified place for float handling."""
        if n == 0.0: 
            if m == 0.0: 
                raise ValueError("Invalid input: Not a line.")
            else:
                return round(n/m,self.p), 1.0, round(b/m,self.p)
        else:
            return 1.0, round(m/n,self.p), round(b/n,self.p)
    
    def __eq__(self,other):
        """Compares the signatures of two lines."""
        return self.sig == other.sig
    
    def __repr__(self):
        """Returns the unambiguous form of a line: its signature."""
        return str(self.sig)
        
    def __str__(self):
        """Returns a readable string form of a line: an equation."""
        if self.n == 0:
            return "x = " + str(self.b*-1)
        else:
            if self.m == 0:
                return "y = " + str(self.b)
            else:
                return "y = " + str(self.m) + "x + " + str(self.b)
    
def f1(sq1,sq2):
    """Prints the equation to a line that runs through the centers
    of two input squares.
    
    Args:
        sq1: A tuple of floats ((x,y),s), where x and y are the 
             coordinates of the center of a square, and s the side
             length.
        sq2: "                                                   "
    
    Raises:
        ValueError: A square with side length <= 0 has been input.
    """
    c1, s1 = sq1
    c2, s2 = sq2
    
    if s1 <= 0 or s2 <= 0:
        raise ValueError("Invalid square: side length must be positive.")
    
    x1, y1 = c1
    x2, y2 = c2
    
    # The centers of the two squares might be identical. If so, we may 
    # return any line that goes through this point. We choose a 
    # horizontal line. (We also could have chosen a vertical line like
    # below, elminating a step.)
    
    if x1 == x2 and y1 == y2:
        print(Line(1,0,y1))
    
    # We then check if the two points form a vertical line.
    
    elif x1 == x2:
        print(Line(0,1,-1*x1))
        
    # Otherwise, compute the slope and y-intercept as "normal".
    
    else:
        slope = (y2 - y1) / (x2 - x1)
        y_int = y1 - (x1 * slope)
        print(Line(1,slope,y_int))
    
def test(): 
    """Tests some examples."""  
    inputs = [(((0,0),6),((2,3),17)),
              (((-5,0),6),((-5,88),17)),
              (((0,0),6),((9,0),17)),
              (((-1,1),6),((1,-1),17)),
              (((0,0),0),((2,3),17))]  # Should raise an exception.
    
    for input in inputs:
        f1(*input)
    
    
    
        
        
    
    
    
    
    
    
    
    
    
    
    
    
            
            
            
            
            
            
            