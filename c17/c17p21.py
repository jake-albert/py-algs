from random import randint

# c17p21

# Volume of Histogram: Imagine a histogram (bar graph). Design an algorithm to
# compute the volume of water it could hold if someone poured water across the
# top. You can assume that each histogram bar has width 1.
#
# EXAMPLE 
#
# Input{0, 0, 4, 0, 0, 6, 0, 0, 3, 0, 5, 0, 1, 0, 0, 0} 
#
#         █                                     █          
#         █    █                              __█    █      
#      █  █    █                             █WW█__ _█   
#      █  █  █ █         AFTER FILL ==>      █WW█WW█W█   
#      █  █  █ █                             █WW█WW█W█_ 
#      █  █  █ █ █                           █WW█WW█W█W█
#    ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯                      ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
# Output: 26

##############################################################################

# It is important to clarify first whether or not the "ends" of each histogram
# have some invisible infinite wall on each side that keeps water in. Checking 
# the sample output, it seems that the answer is NO. We should instead treat
# both ends as bottomless chasms that drink up all the water that spills in.

# A straightforward approach to solving this problem would be to simulate 
# "filling up" the histogram layer by layer from the ground. First, for height
# 1, we find all values LESS than 1 for which at least one value greater than 
# or equal to 1 exists somewhere to both the left and right, and add 1 to a
# running volume count for each height. We repeat the same for heights 2 and 
# so on (remembering to add only 1 volume unit per value per "layer") until we
# have reached K, the highest height of any bar in the input. This takes O(KN)
# time and O(1) space. 
 
# But there is an approach whose runtime is not dependent on K and thus is 
# faster for most inputs. This became clear to me when I made a few arbitrary 
# histograms and noticed what I was doing when I instinctively drew the water 
# lines myself. When going from the left side until a max value of the list, 
# or from the right side until a max value, water levels out at whatever value
# is the highest that has been seen so far. When there are multiple values of 
# maximum height, water fills up all the way to that height for all indices 
# in between the left-most and right-most appearances of that max value:

#                          _____________
#                         █WWWWWWWWWWWWW█
#                         █WWWWWWWWWWWWW█
#                         █WWWWWWWWWWWWW█________
#                         █WWW█WWWWWWWWW█WWWWWWWW█
#                         █WWW█WWWWWW█WW█WWWWWWWW█____
#                   ____ _█WWW█WWWWWW█WW█WWWW█WWW█WWWW█
#                  █WWWW█W█WWW█WW█WWW█WW█WWW██WWW██████___
#                  █WWWW█W█WWW█WW█W███WW█WWW██WWW██████WWW█
#                  █W█WW███WWW█WW█W████W█WWW██WWW██████WWW█
#              ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ 

# To find the actual volume of water at any given column, we simply take the
# height that the water line should be there and subtract from it the height 
# of the bar itself that acts as the "floor".

# I initially wrote a function that computes and stores the height of the 
# water at each index before computing the volume by summing (water height -
# bar height) at each index, but realized that there is no need for that O(N)
# storage. The below two algorithm runs in O(N) time and require O(1) space. 

# I assume that the input heights for the histogram are non-negative integers,
# but this approach would also return correct volumes with negative integers 
# in the input representing "divots" in the ground.
    
def f1(bar_heights):
    """Returns the volume of water a histogram could hold after water 
    is poured over it. 
    
    Args:
        bar_heights: A list of non-negative ints representing the 
          heights of bars of width 1 in the histogram.
          
    Returns:
        An int.
    """
    if len(bar_heights) < 3:  # Histogram cannot possibly hold water.
        return 0
    
    vol = 0
    
    # Traverse the bars from left to right, adding to vol the
    # difference between the height of the current bar and the highest
    # bar seen yet. After this is complete, max_from_left will equal 
    # the height of the highest bar in the histogram, and vol will have
    # over-counted units of water past the right-most highest bar.
    
    max_from_left = float("-inf")
    for bar_height in bar_heights:
        max_from_left = max(max_from_left,bar_height)
        vol += max_from_left - bar_height
    
    # Return from right to left only until the right-most instance of 
    # a highest bar, this time subtracting from vol to correct for the
    # over-counting.
    
    i, max_from_right = len(bar_heights)-1, float("-inf")
    while bar_heights[i] != max_from_left:
        max_from_right = max(max_from_right,bar_heights[i])
        vol -= max_from_left - max_from_right
        i -= 1
    
    return vol

# The above approach performs more subtraction operations than would be used
# if we, as below, take an initial "scan" of the input list to determine the 
# right-most bar with the highest height in the histogram. Doing this would 
# require more comparison operations, but I imagine that comparison operations
# are less expensive than subtraction, so this might be faster on inputs with
# many large bar heights. (Also, the above approach will be have some kind of
# integer overflow error earlier as bar heights get larger due to its extra 
# additions. This isn't much of a problem in Python, where the int type has 
# arbitrary precision, but could be relevant if using some numeric type of 
# fixed size.) Might revisit to test for timing.

def f2(bar_heights):
    """Returns the volume of water a histogram could hold after water 
    is poured over it. 
    
    Args:
        bar_heights: A list of non-negative ints representing the 
          heights of bars of width 1 in the histogram.
          
    Returns:
        An int.
    """
    if len(bar_heights) < 3:  # Histogram cannot possibly hold water.
        return 0
    
    right = rightmost_max(bar_heights)     
    return fill(bar_heights,right,True) + fill(bar_heights,right,False)  
    
def rightmost_max(lst):
    """Returns the index to the right-most maximum value in a list."""
    maxval = float("-inf")
    
    for i, item in enumerate(lst):
        if item >= maxval:
            maxval = item
            right = i
    
    return right
    
def fill(bar_heights,right,from_left):
    """Simulates filling water from one end to a stop point. 
    
    Args:
        bar_heights: A list of non-negative ints.
        right: An int index to the right-most highest bar.
        from_left: A Boolean.

    Returns:
        An int representing the volume of water held after pour.
    """
    start_i, change_i = (0,1) if from_left else (len(bar_heights)-1,-1)
    vol, i = 0, start_i 
    
    max_so_far = float("-inf")
    while i != right:
        max_so_far = max(max_so_far,bar_heights[i])
        vol += max_so_far - bar_heights[i]
        i += change_i
        
    return vol
    
# To test correctness, I also wrote a the O(KN) time function.
    
def f3(bar_heights):
    """Returns the volume of water a histogram could hold after water 
    is poured over it. 
    
    Args:
        bar_heights: A list of non-negative ints representing the 
          heights of bars of width 1 in the histogram.
          
    Returns:
        An int.
    """
    if len(bar_heights) < 3:  # Histogram cannot possibly hold water.
        return 0
        
    vol = 0  
    max_height = max(bar_heights)
    
    # Fill the histogram one layer of water at a time.
    
    for height in range(1,max_height+1):
        for i in range(*get_boundaries(bar_heights,height)):
           if bar_heights[i] < height:
                vol += 1
    
    return vol
    
def get_boundaries(bar_heights,height):
    """Returns the left and right-most indices for values >= height."""
    left, right = None, None

    for i in range(len(bar_heights)):
        if bar_heights[i] >= height:
            if left is None:
                left = i
            right = i
    
    return left, right

def test():
    """Tests some sample inputs, including the example at the top."""
    in_out = [([0,0,4,0,0,6,0,0,3,0,5,0,1,0,0,0]                      , 26),
              ([0,0,2,3,1,0,0,4,0,2,5,3,2,1,3,0,7,4,1,1,2,1,3,2,3,0,0], 38),
              ([100,0,9987]                                           ,100),
              ([1,3,14,55]                                            ,  0),
              ([5,4,3,2,1]                                            ,  0),
              ([8,7,5,6,4,3,2,1]                                      ,  1),
              ([0,0,4,0,0,6,0,0,3,0,8,0,2,0,5,2,0,3,0,0]              , 46)]
              
    for input, output in in_out:
        assert f1(input) == f2(input) == f3(input) == output
    
def rand_test(trials,length,max_height):
    """Tests all above functions on randomly generated inputs.
    
    Args:
        trials: A non-negative int. The number of inputs to generate.
        length: A non-negative int. The length of each input.
        max_height: A non-negative int. Highest possible bar height.
    
    Raises:
        AssertionError: Some outputs do not align.
    """
    for trial in range(trials):
        input = [randint(0,max_height) for _ in range(length)] 
        assert f1(input) == f2(input) == f3(input)