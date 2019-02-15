from operator import itemgetter
from random import randint

# c17p08

# Circus Tower: A circus is designing a tower routine consisting of people
# standing atop one another's shoulders. For practical and aesthetic reasons,
# each person must be both shorter and lighter than the person below him or
# her. Given the heights and weights of each person in the circus, write a
# method to compute the largest possible number of people in such a tower.
#
# EXAMPLE
# Input (ht, wt): (65,100) (70,150) (56,90) (75,190) (60,95) (68,110)
# Output: The longest tower is length 6 and includes from top to bottom:
# (56,90) (60,95) (65,100) (68,110) (70,150) (75,190) 

##############################################################################

# I assume that the input heights and weights are positive integers.

# First, we consider the brute-force search space for this problem. If there
# are N people, we and we can arrange them in any order, and we are looking 
# for a tower that has any number of people from 1 to 1-N, then there are a 
# total of N!+(N-1)!+(N-2)!+...+1 towers that can be built, which is in 
# O(N*N!). We could this space by trying every ordering, testing it for 
# validity, and keeping track of the largest number of people we see in a
# valid tower so far. This becomes unfeasibly slow with even small N. 

# A good idea to start is to sort the list of people in increasing order by 
# one of their dimensions, either weight or height, selected arbitrarily. All
# valid towers must have people in the same order as the people in the sorted 
# list, so this narrows the search space significantly. In fact, now the fully
# space of towers to check can be searched by searching the set of all 
# sequences of increasing indices in the array. 

# This is equivalent to the set of all subsets of the list of indices. Why?
# Say there are 10 items in the sorted list, with indices:

#                      0  1  2  3  4  5  6  7  8  9

# Any tower that we can build here corresponds to exactly one subset of those
# indices, there is only ONE ordering of those indices that could create a 
# valid tower. For example, a tower that starts with the person at 2 and also
# has the people at 6, 4, and 9 is the tower (2,4,6,9). All other 4!-1
# permutations of those indices also correspond to the same tower/subset.

# So, in O(NlogN) time we are able to reduce brute force search space from 
# O(N*N!) to O(2^N), which is still quite large but better than before. What 
# more is possible?

# Again, assume that we have taken O(NlogN) time to sort the input by one 
# dimension. We are left with a list of people who are not necessarily sorted
# along the second dimension:

#  i: 0   1   2   3   4   5   6   7   8   9  10  11  12
# D1: 2   5   9  11  14  15  16  17  44  47  58  67  78
# D2: 7   2  14  12  13   1  15  17   4  99  16  17  18

# We attempt to stack people from left to right (which means from top to 
# bottom in the tower, since dimensions are in increasing order) using dynamic
# programming. (Let "PPL[x]" mean "the person at index x".) For each index i, 
# we are going to find OPT[i], which I define to mean "the number of people in
# the OPTimal tower that uses only PPL[i], in addition to any other people 
# from indices 0 to i-1. 

# We know that OPT[0] is 1, given that the OPTimal tower we can make using
# only the person at index 0 is always made of that single person. For higher
# values of i, OPT[i] is equal to the largest among two cases:

#     A) 1 if for all j < i, PPL[j] CANNOT stack on top of PPL[i] -- that is,
#        at least one of PPL[j]'s height or weight is greater than or equal to
#        that of PPL[i]'s; and
#     B) the largest value OPT[j]+1 for all j < i for which PPL[j] CAN stack 
#        on top of PPL[i] -- that is, where PPL[j]'s height and weight are 
#        both strictly less than those of PPL[i].

# Here is what happens when I filled out OPT manually: 

#   i: 0   1   2   3   4   5   6   7   8   9  10  11  12
# ------------------------------------------------------
#  D1: 2   5   9  11  14  15  16  17  44  47  58  67  78
#  D2: 7   2  14  12  13   1  15  17   4  99  16  17  18
# OPT: 1   1   2   2   3   1   4   5   2   6   5   6   7

# To find OPT[1]: We cannot cannot stack PPL[0] onto PPL[1] because 7 > 2, so
# OPT[1] is also equal to 1. (Case A)

# To find OPT[2]: PPL[0] can stack onto PPL[2] because 2 < 9 and 7 < 14. 
# PPL[1] also can stack onto PPL[2] because 5 < 9 and 2 < 14. OPT[0] and 
# OPT[1] are both equal to 1, so either is fine. OPT[2] is 2. (Case B)
 
# A simple O(N^2) solution becomes apparent: maintain a memo OPT, and for each
# i that is not the base case, scan backwards and for each person check in 
# O(1) time whether or not they are stackable onto PPL[i]. Keep one running 
# count of the maximum value stored in OPT so far, and return. (Or, simply 
# iterate over OPT once in O(N) time to find the maximum.) O(N) space is 
# required for the memo.

# If we wanted to, we could also store "backpointers" in OPT so that we could
# backtrack and return the exact people to stack, but the problem does not 
# call for any more than the maximum number of people.

def f1(PPL):
    """Returns the largest possible number of people that may be
    stacked in a tower.
    
    The tower consists of people stacked one top of the other, and must
    have the property that each person is both shorter and lighter than
    the person below. 

    Args:
        PPL: A list of tuples of positive ints representing heights and
        weights. (As long as each tuple is consistent, which dimension 
        comes first does not matter.)
    
    Returns:
        An int.
    """
    if len(PPL) == 0:
        return 0

    # We sort people by their FIRST dimension.
    
    SORT_D = 0
    PPL.sort(key=itemgetter(0))
    OPT = [1]
    
    for i in range(1,len(PPL)):
        
        # OPT[i] is never less than 1, because a tower can always be 
        # made of PPL[i] alone.
        
        OPT_i = 1
        for j in range(i-1,-1,-1):
            if can_stack_onto(PPL[j],PPL[i],SORT_D):
                OPT_i = max(OPT_i,OPT[j]+1)
        OPT.append(OPT_i)
    
    return max(OPT)
    
def can_stack_onto(pj,pi,SORT_D):
    """Returns True iff pj can stack on top of pi.
    
    Args:
        pj,pi: Tuples of ints.
        SORT_D: An int. The dimension by which people were sorted.
    
    Returns:
        A Boolean.
    """
    
    # Check the SECOND (unsorted) dimension first, which is more likely
    # to fail and allow an early return of False, then the FIRST.
    
    COMP_D = 1 - SORT_D
    return (pj[COMP_D] < pi[COMP_D]) and (pj[SORT_D] < pi[SORT_D])
    
# This approach vastly improves on the exponential brute-force search, but do
# we really need to scan all the way back to index 0 for each index when 
# constructing OPT? Taking a look again at the sample input and its OPT:

# (For now, I assume that there are no duplicate values in D1, meaning that 
# we need check ONLY D2 values when determining who can stack onto whom.)

#   i: 0   1   2   3   4   5   6   7   8   9  10  11  12
# ------------------------------------------------------
#  D1: 2   5   9  11  14  15  16  17  44  47  58  67  78
#  D2: 7   2  14  12  13   1  15  17   4  99  16  17  18
# OPT: 1   1   2   2   3   1   4   5   2   6   5   6   7

# In order to determine OPT[8], we need to look only back to the most RECENT
# indices with unique OPT values. These would be OPT[7]=5, OPT[6]=4, OPT[5]=1,
# OPT[4]=3, and OPT[3]=2. All previous indices have OPT values that are equal 
# to one of these five values, so the resulting tower using PPL[8] and those 
# previous indices are no higher than what can be constructed using these five 
# later indices.

# What's more, because we are reading from PPL from left to right, the most 
# RECENT indices with a given OPT value are also the indices at which the
# tower with a given number of people has the person with the SMALLEST 
# possible second dimension at its bottom. For example, in the completed OPT
# there are several indices i with OPT[i] equal to 2, but it is the rightmost
# one at i=8, where D2 is equal to 4, that we find the tower made of two 
# people "ending" with the "smallest" person possible.

# Keeping track of only these indices, then, allows us to build the towers
# with the most people, because a smaller person at the bottom of the tower is 
# more likely than a larger person to be able to support someone else stacking
# below them. The heights of the indices when deciding OPT[8] are, in order, 
# [1,12,13,15,17]. We see that D2 of PPL[8], of 4, fits "below" 1 where 12
# currently is, so we know that OPT[8] is equal to 2. We replace 12 with 4 to 
# indicate that now any person with a D2 greater than 4 can fit "below" PPL[8] 
# to form a 3-person tower.  

# Duplicate values in D2 are still handled properly by this approach. For
# instance, PPL[7] with D2 value of 17 forms a 5-person tower, but later 
# PPL[12], who also has D2 value of 17, forms a 6-person tower, because the 
# running list of "smallest people at the bottom of a tower with x people" has
# changed at this point to indicate that 16, not 17, is the smallest D2 at the
# bottom of a 5-person tower.

# Altogether, then, the OPTimal number of people in a tower is the length of 
# this list after it is fully updated. At each index i, rather than update 
# OPT[i] by searching backwards in O(N) time, we can simply check D2 of PPL[i]
# and use binary search to place this D2 in the list. We find the right-most 
# or highest D2 value in the list that is smaller than the new value, and then
# replace the D2 value to the right with the new value (or append the new 
# value if no such value exists to the right).

# Thus, each step takes O(logN) time, making overall runtime O(NlogN). O(N)
# space is needed in the most memory-taxing case, where we append to the list
# at each step.

# I assume we are permitted to modify the input (sort it by one dimension). 
# Otherwise, we must copy the input in O(N) time first, but this is not the 
# bottleneck of the problem. 

def f2(PPL):
    """See f1 docstring."""
    if len(PPL) == 0:
        return 0
    
    # We sort people by their FIRST dimension (assume no duplicates).
    
    SORT_D, COMP_D = 0, 1
    PPL.sort(key=itemgetter(SORT_D))
    
    # By the time f2 returns, d_list[i] means: "the SECOND dimension of
    # the smallest person that can be at the bottom of a tower made of
    # i+1 people". Its length is thus max number of people in a tower.    
    
    d_list = []
    for i,size in enumerate(PPL):
        bin_insert(d_list,PPL[i][COMP_D])
    
    return len(d_list)

def bin_insert(lst,x):
    """Inserts x into a sorted lst by binary search.
    
    Given a list and new value x, finds the right-most value in the
    list that is smaller than x, and then replaces the value to the
    right with x (or append x if no value exists to the right). If no
    value in the list is smaller than x, sets or appends x as lst[0].
    
    By above, if x is already in lst, no change to lst.
    
    Ex. lst           x   | lst after update   
        [2,4,15,22]   7   | [2,4,7,22]
        [2,4,15,22]  17   | [2,4,15,17]
        [2,4,15,22]  33   | [2,4,15,22,33] 
        [2,4,15,22]   4   | [2,4,15,22]
        [2,4,15,22]   1   | [1,4,15,22]
    """
    lo, hi = 0, len(lst)-1
    
    while lo <= hi:
    
        mid = (lo+hi)//2
        if lst[mid] > x:
            hi = mid-1
        elif lst[mid] < x:
            lo = mid+1
        else:
            return 
    
    if lo >= len(lst):
        lst.append(x)
    else:
        lst[lo] = x
  
def toy_test():
    """Tests f1 and f2 the two sample inputs discussed above."""
    inputs = [[(65,100),(70,150),(56,90),(75,190),(60,95),(68,110)],
              [(1,7),(2,2),(3,14),(4,12),(5,13),(6,1),(7,15),(8,17),(9,4),
               (10,99),(11,16),(12,17),(13,18)]]

    outputs = [6,
               7]
               
    for input,output in zip(inputs,outputs):
        assert f1(input) == output
        assert f2(input) == output
        
# Until now, when writing f2, I have assumed that there were no duplicates in 
# D1, the dimension by which we first sorted the input. Unfortunately, we need
# to do more when we cannot assume this, as in the possible input below:

#   i: 0   1   2   3   4   5   6   7   8
# ---------------------------------------
#  D1: 1   2   3   4   4   4   5   6   7       
#  D2: 7   5   6   7   3   4   5   6   7
# OPT: 1   1   2   3   1   1   2   3   4

# On this input, f2 would assume that PPL[4] can stack onto PPL[5] because 
# 3 < 4, but this is incorrect because both people have the same D1 value. 
# The d_list would look like [3,4,5,6,7], indicating a 5-person tower, when
# actually no tower with more than 4 people is possible.

# Using only the logic of f2, we have a workaround on some inputs. Because 
# duplicates in D2 do NOT make f2 incorrect, we can detect duplicates in each 
# dimension in O(N) time, and sort on any dimension without them.

# If there are duplicates in BOTH lists, though, we need something better than
# f2 in order to still be able to solve in O(NlogN) time. Consider the below 
# input, which has been sorted on D1, and secondarily on D2 to break ties:

#   i: 0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16
# ----------------------------------------------------------------------
#  D1: 1   2   3   4   5   5   5   5   5   5   5   5   5   5   5   5   5
#  D2: 2   5   8  14   1   2   3   4   5   6   7   8   8   9  10  15  16  
# OPT: 1   2   3   4   ?

# Before hitting the "sea" of people all with D1 of 5, d_list is [2,5,8,14].
# We can use no more than ONE person with D1 of 5 in constructing any tower, 
# so we cannot simply change d_list to [1,2,3,4,5,6,7,8,9,10,15,16] as we 
# could if all sorted D1 values were unique.

# Instead, what we can do is find where each of these people would belong in
# d_list if they were the ONLY person with D1 value of 5. PPL[4], with D2 of
# would change d_list from [2,5,8,14] to [1,5,8,14]. PPL[8], with D2 of 5, 
# would not change d_list at all. All such changes are below:

# PPL[i][D2]   bin_insert([2,5,8,14],PPL[i][D2])
# ----------------------------------------------
#          1            * [1,5,8,14]    
#          2              [2,5,8,14]
#          3            * [2,3,8,14]    
#          4              [2,4,8,14]
#          5              [2,5,8,14]
#          6            * [2,5,6,14]    
#          7              [2,5,7,14]
#          8              [2,5,8,14]
#          8              [2,5,8,14]
#          9            * [2,5,8, 9]    
#         10              [2,5,8,10]
#         15            * [2,5,8,14,15] 
#         16              [2,5,8,14,16]
  
# The starts represent a point at which a specific value in d_list is replaced
# for the FIRST time by a person with D1=5. Since they are sorted by D2, this 
# means the person with the lowest D2 value who can replace a specific value 
# in d_list. These are the values that we want stored in the new d_list after
# we exit the "sea" of people with D1=5: [1,3,6,9,15].

# The way to form this is as follows: take the first person in this "sea" and 
# like usual find where they would belong in d_list. This time, though, STORE
# in O(1) space the value that this person replaced (in the above example, 2.)

# Skip over any D2 values that are <= to this replaced value. Insert again 
# only once a D2 higher than this value is found, and overwrite the "replaced"
# value with the new one (in the above, 5).

# If ever the new value is APPENDED to the list, increasing the tower height, 
# then there is no need to check people with higher D2 values, so we move 
# until we find the next distinct D1 value. 

# PPL[i][D2]   replaced     action       d_list  
# ----------------------------------------------
#          1       -inf     insert    [1,5,8,14]  
#          2          2       skip    [1,5,8,14]
#          3          2     insert    [1,3,8,14]    
#          4          5       skip    [1,3,8,14]
#          5          5       skip    [1,3,8,14]
#          6          5     insert    [1,3,6,14]    
#          7          8       skip    [1,3,6,14]
#          8          8       skip    [1,3,6,14]  
#          8          8       skip    [1,3,6,14]  
#          9          8     insert    [1,3,6, 9]   
#         10         14       skip    [1,3,6, 9]
#         15         14     insert    [1,3,6, 9,15] 
#         16        inf       DONE    [1,3,6, 9,15]

# Very little revision of f2 was required to write the correct f3:

def f3(PPL):
    """See f1 docstring."""
    if len(PPL) == 0:
        return 0
    
    # We sort people by their FIRST dimension, then by their second
    # dimension to break ties.
    
    SORT_D, COMP_D = 0, 1
    PPL.sort(key=itemgetter(SORT_D,COMP_D))
    
    # By the time f3 returns, d_list[i] means: "the SECOND dimension of
    # the smallest person that can be at the bottom of a tower made of
    # i+1 people". Its length is thus max number of people in a tower.    
    
    d_list = []
    replaced = float("-inf")
    
    for i,size in enumerate(PPL):
        
        if i == 0 or PPL[i-1][SORT_D] != PPL[i][SORT_D]:
           replaced = float("-inf") 
        
        if PPL[i][COMP_D] > replaced:
            replaced = bin_insert_f3(d_list,PPL[i][COMP_D])
    
    return len(d_list)

def bin_insert_f3(lst,x):
    """See bin_insert docstring. Returns replaced value."""
    lo, hi = 0, len(lst)-1
    
    while lo <= hi:
    
        mid = (lo+hi)//2
        if lst[mid] > x:
            hi = mid-1
        elif lst[mid] < x:
            lo = mid+1
        else:
            return x
    
    if lo >= len(lst):
        lst.append(x)
        return float("inf")
    else:
        replaced = lst[lo]
        lst[lo] = x
        return replaced

# And we see that this f3 correctly returns 5 on our example input, just like 
# the O(N^2) approach of f1.
        
def toy_test_f3():

    PPL = [(1,2),(2,5),(3,8),(4,14),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),
           (5,8),(5,8),(5,9),(5,10),(5,15),(5,16)]

    fns = [(f1, 5),  # Correct
           (f2,12),  # Incorrect
           (f3, 5)]  # Correct
           
    for f,output in fns:
        assert f(PPL) == output 
 
# The below test does not systematically check all possible inputs of a 
# certain length with certain possible integer values, so does not give 100% 
# confidence that f3 performs identically to f1, but testing over many long,
# randomized inputs shows no discrepancies.
 
def test(trials):
    """Randomly generates PPL and tests f2 and f3 against f1 on them."""
    MINV, MAXV = 1, 30
    N = 100

    f_discreps = [[f2,0],[f3,0]]
    for _ in range(trials):
    
        PPL = [(randint(MINV,MAXV),randint(MINV,MAXV)) for _ in range(N)]
 
        for p in f_discreps:
            try:
                assert f1(PPL) == p[0](PPL)
            except:
                p[1] += 1
    
    print("Discrepancies with f1:")
    for f,discreps in f_discreps:
        print(f"{f.__name__}: {discreps:4}")