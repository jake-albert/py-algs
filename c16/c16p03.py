# c16p03

# Intersection: Given two straight line segments (represented as a start
# point and an end point), compute the point of intersection, if any. 

# ##############################################################################

# I assume that line segments are input in the form [(x1,y1),(x2,y2)], which
# is a list of tuples representing the points. I assume the inputs are floats,
# though the function also handles int inputs. If there is no intersection 
# point that lies on the line segments, then I chose to return None. 

# I also assume for this problem that the input is well-formed. An alternative
# could be to implement a series of classes such as a LineSeg class with Point 
# attributes p1, p2 that enforces that the input be well-formed, and a Line or 
# Equation class to represent the slope and y-intercepts for each line. I take
# this approach in later problems related to points, lines, and shapes, but it 
# was still instructive developing a non-object-oriented solution.

# The function examines a large number of cases but operates in O(1) time and 
# with O(1) space requirements.

def f1(ls_a,ls_b):
    """Returns a point of intersection between two line segments.
     
    If no such point exists, returns the None object. If the two
    line segments have multiple points of intersection, then returns
    just one point that lies on both segments.
    
    Args:
        ls_a: The first line segment. A list of two tuples of floats.
        ls_b: The second line segment.  A list of two tuples of floats.
    
    Returns:
        A tuple of floats representing (x,y) coordinates,
        OR the None object.
        
    Raises:
        ValueError: The two end points of at least one line segment are
        the same, indicating that the line segment is a point.
    """
    
    # Find the point of intersection of the two LINEs containing each
    # line segment. Return None early here if lines do not intersect. 
    
    int_point = find_intersection(ls_a,ls_b)
    if int_point is None:
        return None
        
    # Check that the point of intersection on both LINEs also is on 
    # both LINE SEGMENTs and return None if not. Ex. the lines 
    # containing the line segment from (0,0) to (1,1) and the line 
    # segment from (0,6) to (6,0) intersect at (3,3), but this point
    # does not lie on both line segments. 
    
    if on_segment(int_point,ls_a) and on_segment(int_point,ls_b):
        return int_point
    return None
    
def find_intersection(ls_a,ls_b):
    """Determines an intersection point of the lines determined by two
    line segments. Returns None if the lines do not intersect.
    
    Args:
        ls_a: The first line segment. A list of two tuples.
        ls_b: The second line segment.  A list of two tuples.
    """
    
    # Derive the equation for each line, expressed in slope-intercept 
    # form. Identify which lines, if any, are vertical.
    
    m1,b1 = get_equation(ls_a)
    m2,b2 = get_equation(ls_b)
    vert_a, vert_b = m1 is None, m2 is None 
    
    # If exactly ONE line is vertical, then there is one intersection.
    # Calculate it using basic algebra.
    
    if vert_a and not vert_b:
        x = b1
        y = m2*x + b2
    elif not vert_a and vert_b:
        x = b2
        y = m1*x + b1
        
    # If BOTH lines are vertical, then either they are the same line, or 
    # they do not intersect. Determine which is true.
    
    elif vert_a and vert_b:
        if b1 == b2:
            x,y = point_on_colinear_segments(ls_a,ls_b)
            if x is None or y is None:
                return None
        else:
            return None
    
    # If NEITHER line segment is vertical, then either they are on 
    # different lines, indicating that they have one intersection point
    # or that they are on the same line.    
    
    else:
        if m1 == m2 and b1 == b2:
            x,y = point_on_colinear_segments(ls_a,ls_b)
            if x is None or y is None:
                return None
        else:
            x = (b2-b1) / (m1 - m2)
            y = (m1 * x) + b1
    
    return x,y
    
def get_equation(ls):
    """Returns values to be interpreted as a linear equation defining
    the line that contains an input line segment.
    
    Returns the slope and y-intercept for the line the two points on 
    the line segment define. If the two points represent a vertical 
    line, return None for m indicating that the slope is undefined,
    and the x-value as b, the intercept. 
    
    Args:
        ls: The first line segment. A list of two tuples.
        
    Returns:
        A tuple of floats: slope then y-intercept.
        
    Raises:
        ValueError: the input is a point.
    """   
    x1,y1 = ls[0]
    x2,y2 = ls[1]
   
    if x1 == x2 and y1 == y2:
        raise ValueError(f"Invalid input: single point at ({x1},{y1})")
   
    if x1 == x2:  # Vertical line
        return None, x1
        
    m = (y2-y1) / (x2-x1) # Slope

    b = y1 - (m*x1) # Intercept
    
    return m,b
    
def on_segment(p,ls):
    """Given a line segment that defines a line, and a point that is on
    that line, return whether or not the point lies on the line segment.
    
    Args:
        p: A tuple of floats. 
        ls: A list of two tuples of floats.
    
    Returns:
        A Boolean.
    """
    
    # The point is on the segment IFF each coordinate is within the bounds
    # (inclusive) defined by the two points in the line segment.
    
    x1, y1 = ls[0]
    x2, y2 = ls[1]
    
    x_lo, x_hi = min(x1,x2), max(x1,x2)
    y_lo, y_hi = min(y1,y2), max(y1,y2)
        
    if x_lo <= p[0] and p[0] <= x_hi and y_lo <= p[1] and p[1] <= y_hi:
        return True
    return False
    
def point_on_colinear_segments(ls_a,ls_b):
    """Given two line segments that have been shown to be co-linear, 
    returns the coordinates of a point that lies on both line segments,
    and a tuple with None if there is no such point.
    
    Args:
        ls_a: The first line segment. A list of two tuples.
        ls_b: The second line segment.  A list of two tuples.
        
    Returns:
        A tuple of floats or None objects.
    """
    
    # We can consider each dimension separately, finding first an
    # appropriate x-coordinate, and then y.
    
    xa1,ya1 = ls_a[0]
    xa2,ya2 = ls_a[1]
    xb1,yb1 = ls_b[0]
    xb2,yb2 = ls_b[1]
    
    x = get_common_val(xa1,xa2,xb1,xb2)
    y = get_common_val(ya1,ya2,yb1,yb2)
    
    return x,y
    
def get_common_val(a1,a2,b1,b2):
    """Given two one-dimensional intervals, returns a value on both
    intervals, or None if no such interval exists.
    
    Args:
        a1: One end of the first interval.
        a2: The other end of the first interval.
        b1: One end of the second interval.
        b2: The other end of the second interval.
        
    Returns:
        A number.
    """  
    a_start, a_stop = min(a1,a2), max(a1,a2)
    b_start, b_stop = min(b1,b2), max(b1,b2)
    
    # Ensure that a is the line segment with the lowest coordinate.
    
    if a_start > b_start:
        a_start, b_start = b_start, a_start
        a_stop, b_stop = b_stop, a_stop
    
    # Intervals might not overlap. But if they do, the start of the
    # second interval is guaranteed to be on both intervals.
    
    if a_stop < b_start:
        return None
    return b_start
    
def test():
    """Tests some sample inputs. Far from exhaustive."""   
    assert f1([(1.0,1.0),(2.0,2.0)],[(-1.0,-1.0),(1.0,1.0)]) == (1.0,1.0)
    assert f1([(1.0,1.0),(0.0,0.0)],[(0.0,6.0),(6.0,0.0)]) == None
    assert f1([(0.0,0.0),(1.0,1.0)],[(1.0,0.0),(0.0,1.0)]) == (0.5,0.5)