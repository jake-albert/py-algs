# p01

# Longest Straight: A problem shared by my friend Andrew. 
#
# Return the length of the longest consecutive sequence of integers that could
# be formed by picking values from an unsorted list. For example, if the input
# is [1,5,3,6,45,2,11,-10], the correct output is 3 (1,2,3). If the input is 
# [55,77,-1,12], the output is 1 (any sequence of length 1 is the longest).

##############################################################################

# One question is how to handle an empty input. The most reasonable output is 
# 0, given that the longest sequence of any integers that could be formed from
# elements in an empty list is 0.

# The below solution requires O(N) space as it stores one "key: value" pair in
# a dictionary for each item in the input. It takes O(N) time, performing 
# constant-time operations for each item in the input.

# The algorithm works by dynamically growing "spans" of consecutive integers as 
# it reads each item in the list. A "span" has a low value and high value and 
# contains every integer between the low value and high value. 

# Spans are stored in a dictionary such that at any given time, looking up a 
# span's low value returns the high value of that span, and vice versa. We can 
# call this the "low-high property".

# Each new integer that is read is either:
#     1. A duplicate value. This has no effect.
#     2. The beginning of a new, isolated span of length 1. 
#     3. The extension of an already existing span in one direction. 
#        (ex. [7,8],9)
#     4. The "bridge" between two already existing spans. 
#        (ex. [1,2,3],4,[5,6,7,8])

# We can determine which case a new integer x belongs to by checking first 
# whether x is in the dictionary or not. If it is, then we have already seen 
# this integer and can ignore it. If not, then we check whether x+1 and x-1
# are in the dictionary to determine which of cases 2, 3 and 4 holds.

# We then update the span by adding x to the dictionary and setting the 
# appropriate low and high values to maintain the "low-high property".

def f1(lst,verbose=False):
    """Returns the length of the longest consecutive sequence of
    integers that could be formed by picking values from an unsorted 
    list. 
    
    Args:
        lst: A list of ints.
        verbose: A Boolean. If true, prints the sequence as well.
    
    Returns:
        An int.
    """
    if len(lst) == 0:
        return 0

    table = {}
    best_dif = float("-inf")
    best_lo = None
    
    for num in lst:
        
        if num not in table:  # Duplicates do not change program state.
            
            # "Bridge" case between two spans (ex. [2,3],4,[5,6,7,8,9])
            
            if num-1 in table and num+1 in table:
                lo = table[num-1] 
                hi = table[num+1]
                table[num] = num
                
            # "Extension" case from a lesser span (ex. [2,3,4],5)     
            
            elif num-1 in table:
                lo = table[num-1]
                hi = num
                table[num] = lo
            
            # "Extension" case from a greater span (ex. 8,[9])
            
            elif num+1 in table:
                lo = num
                hi = table[num+1]
                table[num] = hi
                
            # "Isolated" span case (ex. 55)    
            
            else:
                lo, hi = num, num
            
            table[lo], table[hi] = hi, lo
            if hi-lo+1 > best_dif:
                best_dif = hi-lo+1
                best_lo = lo
    
    if verbose:
        print([x for x in range(best_lo,best_lo+best_dif)])
    return best_dif
   
def test():
    """Tests some inputs. Far from exhaustive."""
    pairs = [([1,1,3,3,4,8],2),
              ([1,1,103,4,2,3,7,99,101,102,100,105,77],5),
              ([1,5,2,6,3,45,11,-10],3)]
    
    for p in pairs:
        f1(p[0]) == p[1]