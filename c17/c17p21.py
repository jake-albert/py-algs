# c17p21

# Volume of Histogram: Imagine a histogram (bar graph). Design an algorithm to
# compute the volume of water it could hold if someone poured water across the
# top. You can assume that each histogram bar has width 1.
#
# EXAMPLE 
#
# Input{0, 0, 4, 0, 0, 6, 0, 0, 3, 0, 5, 0, 1, 0, 0, 8} 
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
# faster for most inputs. This became clear to me when I drew a few arbitrary 
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




# to find the actual volume of water at any given bar, we simply take the height that 
# the water shouuld be there and subtract it from the height of the bar itself that acts
# as the "floor"

# the below implementation requires O(n) space for keeping track of water heights, and 
# takes O(n) time, in fact no more than 3 passes of the array.

def f1(bar_heights):

    # the narrowest histogram that can possibly hold water is of width 3
    if len(bar_heights) < 3:
        return 0
    
    # determine the highest height that the water can settle to at each index
    water_heights = get_water_heights(bar_heights)
    
    return sum(diff_gen(water_heights,bar_heights))
   
# assumes A and B are of equal length   
def diff_gen(A,B):

    for i in range(len(A)):
        yield A[i]-B[i]
   
# return an array of heights that the water level should be at each index    
def get_water_heights(bar_heights):

    water_heights = []
    
    # calculate maximum values from the left onwards, and record them
    max_from_left = float("-inf")
    for bar_height in bar_heights:
        max_from_left = max(max_from_left,bar_height)
        water_heights.append(max_from_left)
    
    # calculate maximum values from the right onwards, updating them until 
    # you hit max_from_left which currently stores the global maximum value
    max_from_right = float("-inf")
    for i in range(len(bar_heights)-1,-1,-1):
        if bar_heights[i] == max_from_left:
            return water_heights
        max_from_right = max(max_from_right,bar_heights[i])
        water_heights[i] = max_from_right
    
def test(n):
    
    f = f1 if n == 1 else f2

    print(f([0,0,4,0,0,6,0,0,3,0,5,0,1,0,0,0]))                       # 26
    print(f([0,0,2,3,1,0,0,4,0,2,5,3,2,1,3,0,7,4,1,1,2,1,3,2,3,0,0])) # 38
    print(f([100,0,9987]))                                            # 100
    print(f([1,3,14,55]))                                             # 0
    print(f([5,4,3,2,1]))                                             # 0
    print(f([8,7,5,6,4,3,2,1]))                                       # 1
    print(f([0,0,4,0,0,6,0,0,3,0,8,0,2,0,5,2,0,3,0,0]))               # 46
    
# there was ONE improvement that you could have made, by decreasing the total number
# of sweeps from a bit over 2 to exactly 2. you led yourself not to pick up on it 
# by immediatley writing a modular function that stores a memo, but you actually 
# could have been doing slightly more work at the same time 

def f2(bar_heights):

    # the narrowest histogram that can possibly hold water is of width 3
    if len(bar_heights) < 3:
        return 0
    
    # determine the highest height that the water can settle to at each index
    water_heights = []
    
    # calculate maximum values from the left onwards, and record them
    max_from_left = float("-inf")
    for bar_height in bar_heights:
        max_from_left = max(max_from_left,bar_height)
        water_heights.append(max_from_left)
    
    volume = 0
    
    # calculate maximum values from the right onwards, updating them until 
    # you hit max_from_left which currently stores the global maximum value
    max_from_right = float("-inf")
    i = len(bar_heights) - 1
    while True:
        if bar_heights[i] == max_from_left:
            break
        max_from_right = max(max_from_right,bar_heights[i])
        volume += (max_from_right - bar_heights[i])
        i -= 1
        
    while i > 0:
        volume += (water_heights[i]-bar_heights[i])
        i -= 1
    
    return volume