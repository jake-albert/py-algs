# start

# there is an O(n**2) solution that involves trying every pair of values. 
# there is also an O(nlogn) solution that involves SORTING the list first, and 
# then simultaneously traversing from the back towards the front and then the 
# front to the back. This last part runs in linear time so the bulk of time is sorting

# ex for the sum of 3, and a list that sorts to [-6,-5,-1,7,8,9,15], we start 
# with -6 and 15 then move to -6 and 9 which checks out and then to -5 and 8 
# which works and then -1 7 which does not. This would be in O(nlogn) time and O(1) space
# and if the array is PROVIDED sorted, then it can be solved in O(n) time

# best conceivable runtime is O(n) since presumably you need to look at each value
# at least once! Can we actually make it work though? yes. 

# there is also a linear time solution that involves hashing values or using a set
# which I will demonstrate below. It requires also O(n) space

# first, there would need to be a discussion with the interviewer about the handling 
# of duplicates, as the wording is somewhat ambiguous.

# Say that the specified value is 3 and the array is [5,-2,0,3,0,3]. There are two 
# UNIQUE pairs of integers that add to 3, namely [5 and -2] and [3 and 0], but in 
# terms of pairs of values in the list, there is (0a,3a),(0,3b),(0b,3a),and(0b,3b) 
# on top of the (-2,5). In some cases it may be necessary to know this, and in others
# it may be uncecessary to know. 

# for the purposes of this problem, I am just going to have the algorithm output 
# only UNIQUE unordered pairs of integers, but will assume that duplicates can be 
# present in the input list.  

def f1(lst,val):

    # no pairs possible if list has 0 or 1 elements 
    if len(lst) < 2:
        return set()               

    sorted, inc = is_sorted(lst)    
        
    if sorted:
        return find_pairs_sorted(lst,val,inc)
    else:
        return find_pairs_unsorted(lst,val)
        
# O(n) time algorithm to find whether a list is sorted in any order
# ASSUMES length of at least 2 for the lst.       
def is_sorted(lst):
    
    # determine whether to test for increasing or decreasing
    for i in range(0,len(lst)-1):
        
        # continue until we reach a point where lst[i] differs from lst[i+1]
        if lst[i] == lst[i+1]:
            continue
        
        if lst[i] < lst[i+1]:
            cmp = lambda x,y: x <= y
            inc = True
        else:
            cmp = lambda x,y: x >= y
            inc = False
        break
    
    # for the remainder of the indeces, check using the comparator
    for j in range(i+1,len(lst)-1):
        if not cmp(lst[j],lst[j+1]):
            return False, inc
    return True, inc
 
# O(n) time algorithm that requires O(1) space for an already-sorted array
def find_pairs_sorted(lst,val,inc):
    
    output = set()
    left, right = 0, len(lst)-1
    
    # "pinch" in from left and right ends until we have tried all possible pairs
    while left < right:
        
        sum = lst[left] + lst[right]
        if sum < val:
            if inc: left += 1 
            else: right -= 1
        elif sum > val:
            if inc: right -= 1 
            else: left += 1
        else:
            output.add((min(lst[left],lst[right]),max(lst[left],lst[right])))
            left += 1
            right -= 1
    
    return output
    
# O(n) time algorithm that requires O(n) space for an unsorted array
def find_pairs_unsorted(lst,val):

    output_set, search_set = set(),set()
    
    for elem in lst:
    
        # the value that would sum to val with elem
        comp = val - elem
        
        # elem has been designated as a partner to find
        if elem in search_set:
        
            # create a standard ordering and store in results
            lo, hi = min(elem,comp), max(elem,comp)  
            output_set.add((lo,hi))
        
        # elem has not been designated, so insert its comp to search for down the road
        else:
        
            search_set.add(comp)
            
    # depending on how we want to use the output, can output as is in set form, or 
    # alternatively as a list which would take O(n) time to generate
    return output_set
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        