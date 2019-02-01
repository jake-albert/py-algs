from random import randint

# c16p23

# Rand7 from Rand5: Implement a method rand7() given rand5().That is, given a
# method that generates a random number between 0 and 4 (inclusive), write a
# method that generates a random number between 0 and 6 (inclusive). 

##############################################################################

# First, we implement rand5().

def rand5():

    return randint(0,4)
 
# The first approach is most straightforward but can be optimized further. 
# Multiply the result of two calls to rand5(), creating 25 distinct outcomes.
# This space of outcomes cannot be divided evenly into 7 equally likely parts,
# but if the result is in the first 21, we can divide the space evenly.
# Otherwise, we discards the value and try again until we reach a value in the
# first 21. 

def f1():
    """Generates a random integer 0 to 6 inclusive.
    
    Returns:
        An integer from 0 to 6, and the number of calls to rand5() 
        to generate the integer.
    """
    calls = 0    
    while True:
        x = 5*rand5() + rand5()
        calls += 2
        if x <= 20:
            return x % 7, calls 

# The expected number of calls to rand5() required is 2 per round times the 
# 25/21 or rounds we can expect to go through before hitting a value that on 
# which we can halt. This equates to ~2.381 calls to rand5() on average, and 
# we verify this empirically over 100,000,000 trials:

# val: 0 (14.286402%)
# val: 1 (14.279416%)
# val: 2 (14.289279%)
# val: 3 (14.286955%)
# val: 4 (14.291736%)
# val: 5 (14.286753%)
# val: 6 (14.279459%)
# 
# 2.38099022 calls to rand5() per output
 
# But we can optimize on this approach. If the value is 21, 22, 23, or 24, 
# then rather than discard it and try again, we treat it as a rand4() call and
# then use it as well to generate a random value. We multiply by 5 and then 
# make one more call to rand5() in order to get random values from 0 to 19, and
# we can use 14 of those to get another random 7. Of those, the 6 values from 
# 14-19 cannot be split evenly, so we recycle those as if they were the result 
# of a rand6() value and keep going. We can do this until we hit a point where
# only a single value that cannot be split, which would be equivalent to a 
# rand1() value: devoid of information. So at this point we try again.

def f2():
    """Generates a random integer 0 to 6 inclusive.
    
    Returns:
        An integer from 0 to 6, and the number of calls to rand5() 
        to generate the integer.
    """
    calls = 0
    while True:
        
        # Attempt first using the 25 unique outcomes generated from the
        # first two calls to rand5(), and return if one of 21 vals 0-20.
        
        x = 5*rand5() + rand5()
        calls += 2
        if x <= 20:
            return x % 7, calls
        else:
        
            # Attempt to "recycle" the unused values using another call
            # to rand5() until there is only one unused value. 
        
            min_recycle = 21  # The smallest of the unused values.
            max_recycle = 24  # The largest.
            
            while max_recycle - min_recycle > 0:                  
                n = max_recycle-min_recycle+1  
                x -= min_recycle  # Now a simulated randn() generator.
                x = 5*x+rand5()  # There are now 5*n distinct outcomes.
                calls += 1
                check_val = n*5//7*7-1  # Maximize vals to split evenly.
                if x <= check_val:
                    return calls, x % 7
                else:
                    min_recycle = check_val+1
                    max_recycle = n*5-1

# Empirically testing this second approach in experiments of n trials each 
# shows that the probabilities of each of the 7 values approaches 1/7 as n 
# increases, hinting that the function correctly outputs the values with a 
# truly uniform distribution.

# The number of calls to rand5() has decreased to below the above function by 
# to 2.212 or so on average over 100,000,000 trials:

# val: 0 (14.289142%)
# val: 1 (14.278718%)
# val: 2 (14.293791%)
# val: 3 (14.288421%)
# val: 4 (14.279982%)
# val: 5 (14.287094%)
# val: 6 (14.282852%)
# 
# 2.2121973 calls to rand5() per output

# Defining one full "cycle" as a continued recycling of values until trying 
# again from scratch, the probability of outputting a value in one cycle is: 

# 21/25 + 4/25*(14/20 + 6/20*(28/30 + 2/30*(7/10 + 3/10*(14/15)))), which can 
# also be written as (5**6 - 1) / 5**6. The expected number of cycles we will
# need to perform before halting, then is the inverse of that probability, or 
# ~1.000064 times. A major increase from 25/21 or ~1.19. 

# But the average number of times that rand5() is called per cycle is greater
# than the 2 calls per cycle in the first approach. This value is:
 
# 2*21/25 + 4/25*(3*14/20 + 6/20*(4*28/30 + 2/30*(5*7/10 + 3/10*(6*14/15))))

# When multiplied by the expected number of cycles, we have an expected ~2.212
# calls to rand5() on average. We confirm this superior value in the empirical 
# test.

def test(n,spec):
    """Conducts trials of the above functions and prints results.
    
    For each result 0 to 6 inclusive, prints the percentage of the n 
    calls to the generator that returned the result, and prints both 
    the average number of times rand5() was called by the generator, 
    and the maximum number of times.
    
    Args:
        n: An integer number of trials to call.
        spec: An integer that specifies which function to attempt. If 
          1, attempts f1, and otherwise attempts f2.
    """
    f = f1 if spec == 1 else f2
    results_dict = {}
    calls_counter = 0.0
    max_calls = float("-inf")
    
    for _ in range(n):
        val, calls = f()
        if val not in results_dict:
            results_dict[val] = 0.0
        results_dict[val] += 1
        calls_counter += calls
        max_calls = max(calls, max_calls)
    
    for pair in sorted(list(results_dict.items()),key=lambda x:x[0]):
        print ("val: {} ({}%)".format(pair[0],100*pair[1]/n))
    
    print("\n{} calls to rand5() per output".format(calls_counter/n))
    print("max number of calls for one output: {}".format(max_calls))