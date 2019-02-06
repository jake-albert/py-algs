# c17p16

# The Masseuse: A popular masseuse receives a sequence of back-to-back
# appointment requests and is debating which ones to accept. She needs a 
# 15-minute break between appointments and therefore she cannot accept any 
# adjacent requests. Given a sequence of back-to-back appointment requests 
# (all multiples of 15 minutes, none overlap, and none can be moved), find the
# optimal (highest total booked minutes) set the masseuse can honor. Return 
# the number of minutes.
#
# EXAMPLE
# Input: {30, 15, 60, 75, 45, 15, 15, 45}
# Output: 180 minutes ({30, 60, 45, 45}).  

##############################################################################

# I define the output on an empty list as 0. Zero appointments, zero minutes!

# This approach returns the maximum number of minutes in O(N) time and O(1) 
# space. If the set of appointments were required as well, we could store 
# backpointer information in O(N) space but asymptotic runtime is the same.

# (It would be important to clarify in that case what set(s) the Masseuse
# would prefer among several sets with the same maximum time. Does she have a
# second factor that she would like to "tie-break", such as minimizing total 
# break time between her first and last appointments, or is any one fine?)

# Anyway, to find only the maximum time, we can imagine defining some memo OPT
# containing at each index i the optimal time for a list of appointments up to
# and including i. Finding OPT[0] is simple, as it is always optimal to 
# include the appointment when there is only one. So OPT[0] = apts[0]. We also 
# know that OPT[1] is simply the greater of apts[0] and apts[1]. We cannot 
# take both, so just pick the best one. 

# Now say we have found OPT[i] for all 0 <= i < x, and we want to find OPT[x].
# We have two choices: A) include apt[x] in the schedule, and thus cannot use 
# apt[x-1], so we add OPT[x-2]; or B) exclude apt[x] in order to keep OPT[x-1]
# if this option is better than A. This logic works because all appointments 
# are POSITIVE as is described in the problem. 

# Because at every step we never look back more than 2 spots into OPT, we can
# rid ourselves of that storage and keep only 3 integers.

class TinyMemo:
    """Class stores optimal times of sublists of appts.
    
    Attributes:
        current: The optimal time from appts to some index i.
        minus_one: The optimal time from appts to i-1.
        minus_two: The optimal time from appts to i-2.
    """
    
    def __init__(self):
        """Inits TinyMemo for running on index 0."""
        self.current = 0
        self.minus_one = 0
        self.minus_two = 0

def f1(apts):
    """Returns the maximum number of minutes that a Masseuse can honor.

    Args:
        apts: A list of positive ints that are multiples of 15
          representing the durations of back-to-back appointment 
          requests. The Masseuse cannot accept adjacent requests.

    Returns:
        An int.
    """
    opt = TinyMemo()
    for i in range(len(apts)):
    
        opt.minus_two = opt.minus_one
        opt.minus_one = opt.current
        opt.current = max(opt.minus_one,apts[i]+opt.minus_two)    
    
    return opt.current

def test():
    """Tests some sample inputs, including from problem description."""
    in_out = [([],                                 0),
              ([15],                              15),
              ([15,30],                           30),
              ([30,15],                           30),
              ([15,15,15],                        30),
              ([15,150,15],                      150),
              ([30, 15, 60, 75, 45, 15, 15, 45], 180),
              ([30, 15, 60, 75, 45, 45, 15, 45], 195),
              ([30, 45, 60, 90, 45, 15, 15, 45], 195)]
    
    for input, output in in_out:
        try:
            assert f1(input) == output
        except:
            print(input,f1(input),output)