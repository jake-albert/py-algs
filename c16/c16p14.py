# c16p14

# Best Line: Given a two-dimensional graph with points on it, find a line 
# which passes the most number of points. 

##############################################################################

# This brute-force approach examines every unique pair of points in the input
# list of N points, of which there are O(N^2) pairs, and finds the unique 
# equation to a line that runs through both points. It stores in a memo for  
# each line the number of unique pairs of points in the list that define that  
# line. These values will be either 1,3,6,10, or other values that are 
# "triangle numbers": sums of consecutive integers beginning at 1.

# Ex. for a line that passses through 3 unique points a,b,c, there is the pair
# (a,b), the pair (b,c), and the pair (a,c) that each defines that line.

# I assume for this problem that the input consists of unique points. Some 
# code can be written that works in O(N) time to identify and mark as 
# ignorable any duplicates.

# I also take advantage of the fact that my Line class from c16p13 normalizes
# line equations such that unique lines have only ONE representation, and thus 
# only ONE value for hashing. Furthermore, equivalent lines as defined by the 
# class are hashed to the same value. The discussion about how I keep this 
# consistent is in c16p13.py, where the Line class is defined.

from c16p13 import Line

def f1(points):
    """Prints and returns a Line object representing the line that
    passes through the most points in the input.
    
    Args:
        points: A list of tuples of floats.
    """
    
    # If there are no points, then strictly speaking, ANY line passes
    # the maximum number of points: zero. Arbitrarily return the line 
    # y=0. If only one point, return horizontal line through that point.
    
    if len(points) == 0:  
        print(Line(1,0,0))
        return

    if len(points) == 1:
        print(Line(1,0,points[0][1]))
        return
     
    # Otherwise, check the line defined by each pair of points.
     
    memo = {}
    max_line, max_count = None, 0
    
    for i in range(len(points)):
        for j in range(i+1,len(points)):
            
            line = get_line(points[i],points[j])
            
            if line.sig in memo:
                memo[line.sig] += 1
            else:
                memo[line.sig] = 1
                
            if memo[line.sig] > max_count:
                max_line, max_count = line, memo[line.sig]
            
    print(max_line)
    return
    
# assume that p1 and p2 are different. Return the line that connects them    
def get_line(p1,p2):
    """Return the Line instance representing the line that passes 
    through two different points.
    
    Args:
        p1: A tuple of floats.
        p2: "                "

    Returns:
        A Line object.
    """
    
    x1, y1 = p1
    x2, y2 = p2
    
    if x1 == x2:  # horizontal line
        return Line(0,1,-1*x1)
        
    slope = (y2 - y1) / (x2 - x1)
    y_int = y1 - (x1 * slope)
    return Line(1,slope,y_int)
    
# There is a SMALL possible optimization we can make that involves also 
# keeping track of which points belong to a certain line. This would mean not
# needing to call get_line() for a pair that has already been shown to belong
# to a group. For example, if we check ab, ac, ad, ae, and find that they all
# define the same line, then we should NOT need to check bc, bd, be, cd, etc.

# In a "worst-case" scenario in which no more than two points are EVER 
# colinear for all pairs, this "optimzation" saves no time because we must 
# look at every single pair. Taking into account the added time cost of 
# tracking colinear points, this would be slower performance than before.

# In a "best-case" scenario where all input points lie along the same line, 
# this optimization would be able to finish in O(N) time, but information
# about how often this scenario or similar scenarios with many colinear points
# are likely to happen can help inform whether implementing these checks would 
# improve expected runtime over a typical input.