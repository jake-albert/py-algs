import threading
from time import time
import matplotlib.pyplot as plt
from io import StringIO
import sys

# c15p07

# FizzBuzz: In the classic problem FizzBuzz, you are told to print the numbers
# from 1 to n. However, when the number is divisible by 3, print "Fizz'. When
# it is divisible by 5, print "Buzz'. When it is divisible by 3 and 5, print
# "FizzBuzz'. In this problem, you are asked to do this in a multithreaded 
# way. Implement a multithreaded version of FizzBuzz with four threads. One 
# thread checks for divisibility of 3 and prints "Fizz". Another thread is 
# responsible for divisibility of 5 and prints "Buzz': A third thread is 
# responsible for divisibility of 3 and 5 and prints "FizzBuzz': A fourth 
# thread does the numbers. 

##############################################################################

# The factors for the FizzBuzz problem do not need to be 3 and 5. If we want 
# to see all four options printed -- Fizz, Buzz, FizzBuzz, and the number --
# then it must be the case that the smaller of the two factors does not divide
# the larger factor evenly. (If this were the case, then only one of "Fizz" or 
# "Buzz" would ever be printed.) 

FIZZ_FACTOR = 3
BUZZ_FACTOR = 5

# First, I implemented the straightforward, singlethreaded code for FizzBuzz:

def single(n):
    """Prints output for the FizzBuzz problem using one thread.
    
    Args:
        n: An int. All numbers from 1 to n inclusive are processed. 
          Assumed to be >= 1.
    """
    for x in range(1,n+1):
        
        fizz = x % FIZZ_FACTOR == 0
        buzz = x % BUZZ_FACTOR == 0
        
        if fizz and buzz:
            outstring = ("FizzBuzz")
        elif fizz:
            outstring = ("Fizz")
        elif buzz:
            outstring = ("Buzz")
        else:
            outstring = (f"{x}")
 
        # For easier reading, I print not only the message "Fizz", 
        # "Buzz", etc. but also the number itself as a prefix.
 
        print("".join([f"{x}: ",outstring]))

# In order to more easily write a multithreaded version of the solution, I 
# created a wrapper class, "Number". I will create a single instance of this
# class that only one thread may have access to at any one time.
        
class Number:
    """Wrapper class for multithreaded FizzBuzz approach.
    
    Attributes:
        val: An int. The current value of the Number instance.
        limit: An int. The maximum permitted value for the Number.
    """
    
    def __init__(self,limit):
        """Inits a Number instance at 1."""
        self.val = 1
        self.limit = limit
    
    def __str__(self):
        """The string form of a Number is of its value."""
        return str(self.val)
    
    def increment(self):
        """Adds one to a Number's value."""
        self.val += 1

    def is_done(self):
        """Returns True iff a Number's value is past its limit."""
        return self.val > self.limit
        
    def is_div_by(self,factor):
        """Returns True iff a Number's value is divisible by factor."""
        return self.val % factor == 0
    
# I have never used multithreaded programming in Python before, so I relied 
# heavily on the tutorial at https://tinyurl.com/jmpvmmq to learn about 
# Python's threading library. The code at the "Synchronizing Threads" section
# made for a great template to get started! 
    
# All four threads required by the problem will have access to the same Number
# instance, and to the same lock object that forces them to run synchronously. 
    
class FBThread(threading.Thread):
    """A FizzBuzz Thread class that controls printing output for one of
    the four categories of numbers in the FizzBuzz game.
    
    Attributes:
        name: A string. The thread's name for debugging purposes.
        number: A Number instance.
        lock: A lock object.
        fizz, buzz: Booleans. Represent the truth values of 
          divisibility by the Fizz and Buzz factors that would trigger
          printing a string by the thread.
        out: A string, or the None object. When a print is triggered, 
          a FBThread instance concatenates either out, or the string 
          representation of the Number instance if out is None, to the
          string representation of the Number instance with a colon. 
          
          Ex: 
          A) If self.out is "Fizz" and number.val is 12:
             "12: Fizz"
          B) If self.out is None and number.val is 13:
             "13: 13"
    """ 
    
    def __init__(self,name,number,lock,fizz,buzz,out=None):
        """Inits a FBThread instance with specified behavior.""" 
        threading.Thread.__init__(self)
        self.name = name
        self.number = number
        self.lock = lock
        self.fizz = fizz
        self.buzz = buzz
        self.out = out
    
    def run(self):
        """Continuously checks whether self.number meets the correct
        criteria to trigger a print. If so, prints the desired string
        and increments the value of self.number by one."""
        while True:
        
            # Each thread ensures that no other threads can view or 
            # modify self.number at any one time. A thread may release
            # its lock on self.number only if A) it is to break from 
            # the loop, or B) it has determined whether or not to print
            # under current conditions, and has acted accordingly.
        
            self.lock.acquire()  
            
            if self.number.is_done():
                self.lock.release()
                return
            
            if (self.number.is_div_by(FIZZ_FACTOR) == self.fizz) and \
               (self.number.is_div_by(BUZZ_FACTOR) == self.buzz):
                
                print(f"{self.number}: ", end="")
                print(f"{self.out if self.out is not None else self.number}")
                self.number.increment()
                
            self.lock.release()
        
def multi(n):
    """See docstring for single. Runs using four threads. """
    num = Number(n)
    lock = threading.Lock()
    threads = []
    
    # All four ordered sequences of two Booleans must be represented as
    # trigger criteria for the FizzBuzz game. Leaving one out would 
    # lead to never breaking out of the while loop in FBThread.run().
    
    threads.append(FBThread("General",num,lock,False,False))
    threads.append(FBThread("Fizz",num,lock,True,False,"Fizz"))
    threads.append(FBThread("Buzz",num,lock,False,True,"Buzz"))
    threads.append(FBThread("FizzBuzz",num,lock,True,True,"FizzBuzz"))
         
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()

# Both functions print to standard output, so in order to test for correctness
# I borrow from a technique from this link: https://tinyurl.com/y9bpcpwl. This
# allow us to create a context manager that directs printed output to a list 
# of lines that can be compared for equality.

class Capturing(list):

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout
   
def test(n):
    """Tests output of multi(n) against the output of single(n).
    
    Raises:
        AssertionError: There is a discrepancy.
    """
    with Capturing() as s:
        single(n)
    
    with Capturing() as m:
        multi(n)
    
    assert s == m
  
# A note on correctness: the above multithreaded approach works correctly 
# because the locks properly ensure that the threads act synchronously on the 
# Number instance that they share as an attribute. When I comment out the 
# lock.acquire() and lock.release() lines, all kinds of errors can occur:

# Example 1: 

# On one call of multi(20) when the lock mechanism was removed, the output was
# nearly correct but included the number 21, which it should not. (Also, 21 
# should say "Fizz", not the original number!)

#    ...
#    18: Fizz
#    19: 19
#    20: Buzz
#    21: 21
 
# What I think happened here is that the "Buzz" thread handled the number 20
# and incremented it to 21 between the "General" thread's check that the
# number 20 was divisible by 3 (False) and its check that the same number was
# divisible by 5 (should be True, but 20 had been incremented to 21 already, 
# so False) leading it to print 21.

# Example 2: 

# A lot went wrong here in a call of multi(100).

#    ...
#    14: 14
#    15: FizzBuzz
#    15: Buzz
#    16: 16
#    18: Fizz
#    19: 19
#    ...
  
# It seems here that the "General" thread handled and incremented 14 between
# the "Buzz" thread's check of divisibility by 3 (False) and 5 (should be 
# False, but now True on 15), leading "Buzz" to print in addition to the 
# correct "FizzBuzz". And 17 was incremented to 18 before the "General" thread
# had a chance to check it. 
  
# I also took some time to test the runtimes of the single and multithreaded
# approaches against one another. Multithreaded approaches can be used to save
# time by allowing different threads to work asynchronously on tasks that do 
# not interfere with each other, but in the FizzBuzz problem, all threads must
# be forced to run synchronously to avoid issues like above. 

# As a consequence, there is no time-saving benefit that offsets the overhead
# of different threads locking and unlocking access to the Number instance, 
# and the multithreaded approach, while still showing O(N) behavior, has a 
# higher constant value (slope) than the singlethreaded approach does as the
# input n increases. 

# This isn't the end of the analysis -- for instance, does anything change if 
# I change the single and multi to rely not on the IO-based print() function
# but some other type of function, like appending the results to a list? Might
# revisit later.
 
def time_test(trials):
    """Tests single and multi REPEATS number of times on input n values
    that begin at 10 and then double once for each trial, and plots 
    average time per call in relation to n.
   
    Args: 
        trials: An int. Assumed to be positive.
    """
    REPEATS = 10
    inputs, outputs = [], []
    n = 10
    
    for _ in range(trials):
    
        inputs.append(n)
        output = []
            
        for f in [single,multi]:
            
            start_time = time()
            for _ in range(REPEATS): f(n)
            end_time = time()
            
            output.append((end_time-start_time)/REPEATS)  # Average time.
        
        outputs.append(output)
        n *= 2
    
    plot(inputs,outputs)
    
def plot(inputs,outputs):
    """Plots a graph for each single and multi."""
    plt.plot(inputs,[p[0] for p in outputs],label="single")
    plt.plot(inputs,[p[1] for p in outputs],label="multi")
    plt.legend(loc="upper left")
    
    plt.xlabel("\"Play FizzBuzz up to N\"")
    plt.ylabel("Runtime (seconds)")
    
    plt.savefig("c1507.png")
    plt.close()

# The results of one call with 12 trials is below:
    
inputs_12 = [10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5120, 10240, 20480]
outputs_12 = [[0.0007604837417602539, 0.02448873519897461], [0.0015624523162841796, 0.0078122615814208984], [0.003124833106994629, 0.01338191032409668], [0.004941010475158691, 0.015624499320983887], [0.013054108619689942, 0.028156113624572755], [0.023436784744262695, 0.06211464405059815], [0.04818990230560303, 0.12324376106262207], [0.0930314302444458, 0.2182354211807251], [0.18416576385498046, 0.447144603729248], [0.3711287498474121, 0.9103098630905151], [0.7390389919281006, 1.753097128868103], [1.5104444980621339, 3.6489831686019896]]