# start

# with some preprocessing, we are able to achieve the correct answer in linear time.
# it involves keeping track of the minimums and maximums of certain spans within 
# the list. For example, if we have the list [1,4,3,5,2], and we knew the minimum 
# values from i to the end for every i, then we know that we don't have to sort the 1
# because it the remainder has min 2. but we DO need to sort the 4 because it is HIGHER
# than the minimum of the remaining span. 

# MUST USE LESS THAN/GREATER THAN OR EQUALS SIGN TO ACCOUNT FOR DUPLICATES!

def f1(lst):

    if len(lst) == 0:
        print("List empty.")
        return

    # preprocessing for "left" coordinate
    minlist = [0 for x in range(len(lst))]
    min = float("inf")
    
    # populate minlist
    for i in range(len(lst)-1,-1,-1):
           
        if lst[i] < min:
            min = lst[i]
        minlist[i] = min
    
    # minlist now contains the minimum values in the span from index i to len(lst)-1
    left = 0
    while left < len(lst) - 1 and lst[left] <= minlist[left+1]:
        left += 1
        
    # if we have made it all the way to the end, then the list is sorted    
    if left == len(lst) - 1:
        print("Already sorted.")
        return
        
    # preprocessing for "right" coordinate
    maxlist = [0 for x in range(len(lst))]
    max = float("-inf")
    
    # populate maxlist
    for i in range(0,len(lst)):
        
        if lst[i] > max:
            max = lst[i]
        maxlist[i] = max
      
    # max now contains the minimum values in the span from index 0 to i
    right = len(lst) - 1
    while lst[right] >= maxlist[right-1]:
        right -= 1
    
    return left,right