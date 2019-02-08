# c17p04

# Count of 2s: Write a method to count the number of 2s that appear in all the
# numbers between 0 and n (inclusive).
#
# EXAMPLE
# Input: 25
# Output: 9 (2,12,20,21,22,23,24,25. Note that 22 counts for two 2s.)

##############################################################################



# assuming we are working with non-negative integers

# first, the brute force approach
def f1(n):

    def get_two_digits(x):

        twos = 0
        
        while x > 0:
            if x%10 == 2:
                twos += 1
            x //= 10
        
        return twos
        
    total = 0
    
    for i in range(n+1):
        total += get_two_digits(i)
        
    return total
    
# the time complexity of this is O(N*log10(N)), where N is the input integer. 
# pedantically, though, we normally express complexity as a function of the input
# LENGTH, which is log2(n), so the actual complexity is around O((2**n)*n) which 
# is very slow and not ideal. Let's see if we can improve it!

# it turns out that there is a constant-time way to determine the number of digits
# that will be in a specific PLACE (like tens, hundreds, thousands, etc) for all 
# the integers up to a given number and including it. 

# Say the number is 1422 and we want to know how many 2's are in tens places in 0,
# 1,2,3,4,...1422. Well, first we know that in every "hundred" grouping, there are 
# TEN 2's in the ten's place, from 20,21,22,23,24,25,26,27,28,29. Same for 120,121,
# ...129 as well as for 220,221,and so on. So first we can divide 1422 by 100 and 
# find that it has 140 groupings all the way through 300,400,...1200,1300 that are 
# COMPLETE layers. But then what about the numbers 1420,1421,1422? well to do those,
# we simply find 1422 mod 100 which is 22 and see that it is 3 greater than 19, meaning
# that there are three more to count. If it were 1444, then it would have the 
# complete set so we have to max and min out the subtraction result at 10 and 0.

# the following algorithm implements that approach in O(log10(N)) time which is 
# significantly faster than the brute force option...oh and of course in terms of 
# the length of the input which is log2(N), it is linear time.

def f2(n):

    # powers-of-ten component currently considered
    comp = 1
    
    # value that holds all digits at a component level or lower 
    # for example, for starting n=324 and comp=10, builder is 24
    # after this, comp will be set to=100 and thus builder to 324
    builder = 0
    
    ans = 0
    
    while n > 0:
        
        # give another digit to builder
        # ex. for n=5234, builder becomes 4
        builder += comp*(n%10)
    
        # and take one away from n
        # ex. for n=5234, n is now 523
        n //= 10
    
        # include for n the "complete" sets of the digit, plus any 
        # stragglers that are leftover in an incomplete upper layer
        # ex. 523*1 for each instance of a 2 between 0 and 5230
        # then we get the min of 1 and 4-1, which is 1, the most 
        # "extra" digits that we can muster
        ans += (n*comp) + max(0,min(comp,(builder - ((2*comp)-1))))
        
        comp *= 10
    
    return ans
        
# we get correct on these        
def test(n):

    messups, messup_inputs = 0, []
 
    for trial in range(n):
    
        if trial % (max(1,n//100)) == 0:
            print(f"trial {trial} ({100*trial/n:.2f}%)")
    
        if f1(trial) != f2(trial):
            messup_inputs.append(trial)
    
    print(f"{messups} messups.")