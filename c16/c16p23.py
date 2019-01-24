# start

from random import randint

# the most straightforward approach. In each phase, make two calls to rand5()
# and if the number is in the first 21 of 25 values that can be output, it 
# splits that probability space evenly into sevens. Otherwise, it discards the 
# value and tries again. Expected number of calls required is 2 per round times
# (25/21) rounds. This has been verified empirically with 100,000,000 trials:

"""
val: 0 (14.286402%)
val: 1 (14.279416%)
val: 2 (14.289279%)
val: 3 (14.286955%)
val: 4 (14.291736%)
val: 5 (14.286753%)
val: 6 (14.279459%)

2.38099022 calls to rand5() per output
"""

def f1():
    
    calls = 0
    
    while True:
        x = 5*rand5() + rand5()
        calls += 2
        if x <= 20:
            return calls, x % 7  
 
# the bonus approach. In the above if the value is 21, 22, 23, or 24, then we simply
# discard it and try again. but in the below, we treat it as a rand4() call and then 
# use it to get more random values. We multiply by 5 and then add rand5() in order to 
# get random values from 0 to 19, and we can use 14 of those to get another random 7.
# of those, only 14,15,16,17,18,19 which are 6 values cannot be used, so we recycle
# those and keep going. We can do this until we hit a point where we are left with 
# a rand1() value and need to start over again.

# the below empirical test on 100,000,000 trials shows that the values are equally 
# likely. As for number of calls to rand5(), we have decreased them to below the 
# above by a bit of an amount. The average is now 2.212 or so, with a max of 12 for 
# one trial when 100,000,000 were attempted.

# The calculation for the probability of outputting a value in one "cycle" is equal 
# to 21/25 + 4/25*(14/20 + 6/20*(28/30 + 2/30*(7/10 + 3/10*(14/15)))) which is also
# equal to (5**6 - 1) / 5**6. The expected number of cycles we will need to perform,
# then, is the inverse of that. Which is 1.000064...times

# the average number of times per cycle that rand5() is called is equal to 
# 2*21/25 + 4/25*(3*14/20 + 6/20*(4*28/30 + 2/30*(5*7/10 + 3/10*(6*14/15))))
# which, when multiplied by the number of times we need to cycle, amounts to 
# 2.212 calls to the function on average. We get pretty much this value EXACTLY
# in the empirical test.

"""
val: 0 (14.289142%)
val: 1 (14.278718%)
val: 2 (14.293791%)
val: 3 (14.288421%)
val: 4 (14.279982%)
val: 5 (14.287094%)
val: 6 (14.282852%)

2.2121973 calls to rand5() per output
"""

def f2():

    calls = 0
    
    while True:
        
        # attempt first using the 25 values
        x = 5*rand5() + rand5()
        calls += 2
        if x <= 20:
            return calls, x % 7
        else:
            min_recycle = 21
            max_recycle = 24
            
            # keep going until you cannot anymore
            while max_recycle - min_recycle > 0: 
                
                n = max_recycle-min_recycle+1
                x -= min_recycle
                x = 5*x+rand5()
                calls += 1
                check_val = n*5//7*7-1
                if x <= check_val:
                    return calls, x % 7
                else:
                    min_recycle = check_val+1
                    max_recycle = n*5-1
 
def rand5():

    return randint(0,4)
    
def test(n,spec):

    f = f1 if spec == 1 else f2

    mydict = {}
    calls_counter = 0.0
    max_calls = float("-inf")
    
    for _ in range(n):
        calls, val = f()
        if val not in mydict:
            mydict[val] = 0.0
        mydict[val] += 1
        
        calls_counter += calls
        max_calls = max(calls, max_calls)
    
    for pair in sorted(list(mydict.items()),key=lambda x:x[0]):
        print ("val: {} ({}%)".format(pair[0],100*pair[1]/n))
    
    print("\n{} calls to rand5() per output".format(calls_counter/n))
    print("max number of calls for one output: {}".format(max_calls))