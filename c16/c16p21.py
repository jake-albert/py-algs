# start

# first approach takes at most two scans of each list, halting earlier if it can, 
# for a runtime of O(m+n), and requires an additional O(m+n) of storage for a set

# discussion would be required to determine how to handle a case when there is no 
# such pair of values to swap. Do they want it to return none, or print some message?
# For clarity for the toy example, I chose a message.

# we DO assume that the input lists have only integer elements, so no other types

# there MIGHT be a small optimzation in time that involves making a set for both 
# A and B while calculating the sum, but this involves more storage and probably 
# doesn't make a big difference.

def f1(A,B):
    
    # also good to handle a case where lists are empty. I decided the 
    # sums would be undefined as opposed to 0 for an empty list so raise exception
    if len(A) == 0 or len(B) == 0:
        raise Exception("Invalid input: input lists must have at least one element each.")
        
    # track the sums of the list elements and identify which is greater
    sumA, sumB = 0, 0
    for a in A:
        sumA += a
    for b in B:
        sumB += b
    
    # identify the lists with the lower and higher sums
    lo_lst, hi_lst = (A,B) if sumA <= sumB else (B,A)
    diff = abs(sumA-sumB)
    
    # if the difference between the sums is odd, there are no integers to swap
    if diff % 2 == 1:
        print("No such pair.")
        return
        
    # otherwise, we can identify all of the values that could work in hi_lst
    # based on what values are present in lo_lst
    look_for = set(lo_lst)
    for item in hi_lst:
        if item - diff//2 in lo_lst:
            return item - diff//2, item
    print("No such pair.")
    return
        
# use the STAR to call these
input1 = ([4,1,2,1,1,2],[3,6,3,3])      # (4, 6), or (1, 3) 
input2 = ([-1,-5,17,3],[-3,21])         # (-5, -3)
input3 = ([-1,-5,17,3],[1,-7,17,3])     # (17, 17)  
input4 = ([1,2,3,4],[5,6,7,8])          # No such pair.
input5 = ([1,2,3,4,0],[5,6,7,8,-6])     # (0,5)
        
        
        
        
        
        