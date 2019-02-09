from math import ceil, log2

# c17p05

# Letters and Numbers: Given an array filled with letters and numbers, find 
# the longest subarray with an equal number of letters and numbers. 

##############################################################################

# I assume that each object in the list is either a string ONE alphabetical 
# character long, or a string form of some integer. 

# But this problem is really no different from one where the list is filled 
# with only 0's and 1's, so my examples will have "0" stand in for a number 
# and "1" for a letter.

# One other important thing: when there are multiple longest subarrays with an
# equal number of letters and numbers, should all be output, or is any one of
# them acceptable? I assume that just one is sufficient, and my functions
# below all output the one with the leftmost starting index.

# There are O(N^2) total sublists, and to count numbers of 1's and 0's in
# each one takes O(N) time, so the most mindless brute-force approach would 
# run in O(N^3) time and require O(1) space. A small improvement would be to
# keep track of running totals of 1's and 0's for all sublists starting at 
# the same index, bringing runtime to O(N^2).

# I first attempted to come up with an O(N) dynamic programming solution that 
# uses solutions of sublists to find solutions of larger lists, but there was
# not an obvious way to do this in O(1) time at each step. 

# Thinking about this did allow me to realize what kind of preprocessing would 
# be helpful to getting an O(N) solution, though. This involves calculating a 
# "balance factor" on the list from left to right. Let bal[i] equal the number
# of "1"s minus the number of "0"s in the sublist from 0 to i inclusive.
 
# We also determine for each "balance factor" that has been computed, the
# rightmost index with that balance factor. These are stored in a hash table 
# of size O(N) and is represented with the carets below:
 
# i     0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 
# --------------------------------------------------------------------------
# val   1  1  0  0  0  0  1  1  0  0  1  1  1  1  0  1  0  1  1  0  1  1  1 
# bal   1  2  1  0 -1 -2 -1  0 -1 -2 -1  0  1  2  1  2  1  2  3  2  3  4  5
#     
#                                  ^  ^  ^              ^        ^  ^  ^  ^
#                                 -2 -1  0              1        2  3  4  5
                                                  
# Whatever the largest valid sublist is, it is for some i the largest sublist
# that BEGINS with that index. If we can compute the largest valid sublist 
# that begins at each index in the list in O(1) time at each step, then, we 
# can find the largest valid sublist over the whole list. 

# Starting with index 0 is simple: we look up the rightmost index with bal of
# 0. In the above list, this is 13, so our first sublist contender is from 0
# to 13 (length 14).

# In order to think about sublists starting at index 1, we recognize that we
# no longer include the "1" at index 0, so all of the bals ahead should be 1
# LESS than they are stored. But importantly, these scores do not change 
# relative to each other, so they are still useful. Since the value at index 
# 1 is a "1", we want a bal that is one LESS than the current bal, meaning we
# need to find the rightmost index at which the bal is +1. This is is from 1
# to 18 (length 19) and is better than the best sublist seen so far.

# Moving on to index 2, the value of "0" here means we need a bal one MORE 
# than the current val. This is +2, whose rightmost index is 19, and we see 
# that this sublist from 2 to 19 (length 18) should NOT replace the best yet.

# We can simply continue this process until we are done. Note that for some 
# indices, the required bal to find is not in the hash table, or is one that
# is only BEFORE the current index. This indicates that there is no sublist 
# with equal "1" and "0" counts starting at i and going to the right.

# This algorithm requires O(N) space for the list of bals and hash table, and
# takes O(N) time.

def f1(lst):
    """Finds a longest sublist with same number of letters and numbers.
    
    Args:
        lst: A list of strings. A "letter" is a string consisting of
          one alphabetical character, and a "number" is a string form
          of an integer.
        
    Returns:
        A tuple of indices to the start and end (inclusive) of the 
        leftmost longest valid sublist, or None if none exist.
    
    Raises:
        TypeError: lst contains a non-string object.
    """
    if len(lst) <= 1:  
        return None
    
    bals, right_dict = get_bals(lst)   
    best_len = 0
    best_sublist = None
    
    for i in range(len(lst)):
        
        search_val = bals[i] - 1 if lst[i].isalpha() else bals[i] + 1        
        if search_val in right_dict:
            
            right_ind = right_dict[search_val]
            sublist_len = right_ind - i + 1  # non-positive when r_i < i
            if sublist_len > best_len:
                best_len = sublist_len
                best_sublist = (i,right_ind)
    
    return best_sublist

def get_bals(lst):
    """Returns a list of balance factor values, and a dictionary to the
    rightmost indices with a given balance factor.
    
    Args:
        lst: A list assumed to be of length > 1 of strings."""
    bals = [1] if lst[0].isalpha() else [-1]
    right_dict = {}
    
    for i in range(1,len(lst)):
    
        bals.append((bals[i-1]+1) if lst[i].isalpha() else (bals[i-1]-1))
        right_dict[bals[i]] = i         
    
    return bals, right_dict
    
# There is another way to implement the O(N) solution that still uses O(N) 
# memory for a hash table, but does not create a list of balance factors. It 
# is based on the idea of storing the LEFTMOST indices with a given bal:
   
# i  -1  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 
# ---------------------------------------------------------------------------
# val X  1  1  0  0  0  0  1  1  0  0  1  1  1  1  0  1  0  1  1  0  1  1  1 
# bal 0  1  2  1  0 -1 -2 -1  0 -1 -2 -1  0  1  2  1  2  1  2  3  2  3  4  5
#     
#     ^  ^  ^        ^  ^                                      ^        ^  ^
#     0  1  2       -1 -2                                      3        4  5
   
# Now, when reading the list from left to right and keeping only one integer 
# as a running bal factor, we find that the leftmost index that starts a 
# valid sublist that ends at i is one to the right of the leftmost index with
# the same bal. For example, at index 10 bal is -1, and the leftmost index 
# with the same bal is 4, so the longest valid sublist ending at index 10 is 
# from 5 to 10 inclusive. (It is NOT from 4 to 10 because bal at each index 
# represents the bal AFTER the value at that index is accounted for.)

# One important caveat is to remember that when the balance factor is 0 at a 
# given index, the longest valid sublist ending there begins at index 0. I 
# preemptively store "-1" as the leftmost "index" with bal 0 so that the math 
# works out, and so that no actual index with bal 0 in the list gets stored.

def f2(lst):
    """See f1 docstring. Alternate O(N) implementation."""
    if len(lst) <= 1:
        return 
    
    best_diff = 0
    best_indices = None 
    
    cur_bal = 0
    left_dict = {0:-1}
    
    for i, obj in enumerate(lst):
        
        cur_bal += 1 if lst[i].isalpha() else -1
        
        if cur_bal in left_dict:
            diff = i - left_dict[cur_bal]
            if diff > best_diff:
                best_indices = (left_dict[cur_bal]+1,i)
                best_diff = diff
        else:
            left_dict[cur_bal] = i
            
    return best_indices

# The below O(N^2) approach is used to verify correctness of f1 and f2.
    
def f3(lst):
    """See f1 docstring. O(N^2) brute-force implementation."""
    if len(lst) <= 1:
        return None
    
    best_len = 0
    best_array = None
    
    # Check all sublists starting at i for i=0,1,2, etc., keeping a 
    # running count of the bal and checking length whenever bal is 0.
    # We could terminate early in some cases where we have already 
    # found a valid sublist whose length cannot be beat by any sublists
    # starting at later indices, but if we are truly interested in 
    # fast runtime we should use f1 or f2.
    
    for i in range(len(lst)):    
        bal = 1 if lst[i].isalpha() else -1
        
        for j in range(i+1,len(lst)):
            if lst[j].isalpha():
                bal += 1
            else:
                bal -= 1
            
            if bal == 0 and (j-i+1) > best_len:
                best_len = (j-i+1)
                best_array = (i,j)
    
    return best_array
 
def test(n):
    """Tests f1, f2, and f3 on n unique inputs.
    
    Converts every non-negative integer less than n to an input list 
    that acts as a representation of that integer in binary, with
    letters where that integer's "1" bits are and numbers where the 
    "0" bits are.
    
    Ex. for the integer 9 ("1001"), input is ["L","8","8","L"]
     
    For n values that are powers of 2, this approach thus tests the 
    functions over every possible input of length log2(n).
     
    Raises:
        AssertionError: There is a discrepancy between the outputs of
           of f1, f2 and f3.
    """
    L = "L"  # Letter object
    N = "8"  # Number object
    
    desired_len = ceil(log2(n))
    
    for x in range(n):
    
        if x % (max(1,n//100)) == 0:
            print(f"Trial {x} ({100*x/n:.2f}%)")
    
        # Clever list comprehension from https://tinyurl.com/yxhtn8qq:
        
        input = [L if digit=="1" else N for digit in bin(x)[2:]]
        
        # I add extra "zero bits" in the form of number objects as  
        # padding so that all inputs are of the same length.
        
        input.reverse()
        while len(input) < desired_len:
            input.append(N)
        input.reverse()
        
        r1, r2, r3 = f1(input), f2(input), f3(input)
        
        try:
            assert r1 == r2 == r3
        except:
            st = f"Output {r1} or {r2} differs from {r3} on {input}."
            raise AssertionError(st)