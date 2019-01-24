# start

# ahhh, the one that started it all. This time you got it much much more quickly. 
# You know that whatever the span is, it has a left-index and a right-index. 

# for example in the array [-8,3,-2,4,-10] the best sum is 5, from index 1 with value 3, 
# to index 3 with value 4. The index 3 also has the special property that it has the 
# max sum out of all of the spans that start at 0 and go until somewhere. And same for 
# reverse. So we calculate those using O(1) space in O(n) time.

# ONE CAVEAT is required before starting, and this becomes clear when you attempt to 
# run the algorithm on an input with all or nearly all negative values:
# for instance, [-8,1,-2,-4,-10]. The max sum is of course 1 here, but just going by 
# the above we never reach a running total greater than -8. What we need to do at 
# the start is "clip" away all negative numbers on the edge, since after all those 
# cannot be part of a sum, unless ALL negative numbers are in it in which case we 
# return the largest number.

def f1(lst):

    # the sum is undefined for an empty list
    if len(lst) == 0:
        return
        
    # first, clip away negative values on the end
    left = 0
    max = float("-inf")
    
    # clip the left value
    while left < len(lst):
        if lst[left] > 0:
            break
        if lst[left] > max:
            max = lst[left]
        left += 1               
        
    # check if we have all non-positive values
    if left == len(lst):
        return max
        
    # running total and maximum running total
    total, best_total = 0, float("-inf")
    
    # traverse list from left to right
    for i in range(left,len(lst)):
    
        # increment the running total and see if it is max
        total += lst[i]
        if total > best_total:
            best_total = total
            best_i = i
    
    # at this point, we have found best_i to be the right-index of the span
    total, best_total = 0, float("-inf")
    
    # traverse list from right to left
    for i in range(best_i,-1,-1):
        
        total += lst[i]
        if total > best_total:
            best_total = total
    
    return best_total
    
# UNFORTUNATELY, THIS IS ALL STILL WRONG. CONSIDER AN EXAMPLE LIKE [-5,-6,1,-10,-8,3,-5,-9,2]
# the maximum sum is 3, but the algorithm won't find it. 

# okay, i think i have a better way to think of it now. VIEW THE ARRAY NOW AS A SERIES 
# of GLOBS of negative values followed by positive values then negative values. We will
# want to have a result in the form POSITIVE GLOB (NEGATIVE GLOB POSITIVE GLOB)*

def f2(lst):

    if len(lst) == 0:
        return
        
    # peel away the leading non-positive values     
    least_neg = float("-inf")
    left = 0
    
    while lst[left] <=0:
    
        # keep track of the least negative value 
        if lst[left] > least_neg:
            least_neg = lst[left]
        left += 1
        
        # if we have scanned the whole list, return least negative value
        if left >= len(lst):
            return least_neg
            
    # peel away trailing non-positive values
    right = len(lst) - 1
    
    while lst[right] <= 0:
    
        right -= 1
    
    # we now have two indices, left and right, that mark the locations of the 
    # left-most and right-most positive values in the array. 
    
    i, curmax = get_glob(left,lst)
    bestmax = curmax
    
    while i <= right:
        i, neg = get_glob(i,lst)
        i, pos = get_glob(i,lst)
        curmax = max(pos,curmax+neg+pos)
        bestmax = max(bestmax,curmax)
    
    return bestmax
    
# helper function that sums the next "glob" of non-negative or negative values
def get_glob(i,lst):
    
    # determine the appropriate comparator for the glob
    if lst[i] >= 0:
        cmp = lambda x: x >=0
    else:
        cmp = lambda x: x < 0
    
    sum = 0
    
    # continually advance i and add the lst value there to sum
    # so long as the comparator still holds (that is, so long 
    # as we are still within the same glob we identified at the start)
    while i < len(lst) and cmp(lst[i]):
        sum += lst[i]
        i += 1
    
    return i, sum
    
# brute force solution for testing
def f3(lst):

    if len(lst) == 0:
        return
 
    def sumrange(a,b):
        output = 0
        for index in range(a,b+1):
            output += lst[index]
        return output
        
    maxsum = float("-inf")
    for i in range(len(lst)):
        for j in range(i,len(lst)):
            maxsum = max(maxsum,sumrange(i,j))
            
    return maxsum

# highly efficient version
def f4(lst):

    if len(lst) == 0:
        return

    best,prev = lst[0],lst[0]
    for i in range(1,len(lst)):
        prev = max(lst[i],prev+lst[i])
        best = max(prev,best)
    
    return best
    
# test against the brute-force solution
    
import random
    
def test(n):

    messups = 0

    for i in range(n):
        
        if i%10 == 0:
            print("on {}th trial".format(i))
    
        lst = [random.randint(-10,10) for _ in range(200)]
        
        if f2(lst) != f3(lst):
            print("f2",lst)
            messups += 1
        if f4(lst) != f3(lst):
            print("f4",lst)
            messups +=1
            
    print(f"{messups} messups.")
    
    
    
    
    
    
    
    
    
    
    
    
    
            