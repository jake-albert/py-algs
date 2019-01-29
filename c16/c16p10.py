# c16p10

# Living People: Given a list of people with their birth and death years, 
# implement a method to compute the year with the most number of people alive.
# You may assume that all people were born between 1900 and 2000 (inclusive).
# If a person was alive during any portion of that year, they should be 
# included in that year's count. For example, Person (birth = 1908, death = 
# 1909) is included in the counts for both 1908 and 1909. 

##############################################################################

# The naive approach I first thought of was to, for every year 1900 to the 
# current year, determine the number of living people and then after that 
# return the year that had the highest value. O(1) alive_by_yearry required and takes
# O(Y*N) time where Y is the number of years to check. Since in this case 
# there are a constant number of years to check, it can be argued that this 
# is an O(N) time algorithm. 

# Still, 119 full iterations through the list are required. There is likely 
# a more efficient way to do it.

# We know that whatever year(s) have the most number of people alive, one will
# be the birth or death year of SOMEBODY in the list. So rather than check all
# of the 118 full iterations, we need check at most all of the birth years of 
# someone, leading to an algorithm that, while having O(N^2) behavior on a 
# generalized problem in which the possible birth years are not capped, is an 
# improvement to the above idea given the constraints of this problem. 

# Up to one key,value pair is stored for every unique birth year, so in a
# generalized problem this would mean requiring O(N) space, but given there 
# are at most 101 birth years possible, it can be argued that space 
# requirements are in O(1).

def f1(ppl):
    """Returns a year with the most number of people alive.
    
    Args:
        ppl: A list of tuples (birth_year, death_year) for each person.
             These year values are assumed to be ints. If person is still
             Alive, then death_year is None. For each person, it is assumed 
             that birth_year <= death_year
        
    Returns:
        An int when input is nonempty, otherwise None.
    """
    if len(ppl) == 0: return
    
    alive_by_year = {}    
    maxyear = ppl[0][0]
    
    for person in ppl:
    
        year = person[0]  # Birth year.
    
        # Calculate number of people alive for year only if year has 
        # not yet been encountered.
        
        if year not in alive_by_year:
            for person in ppl:
                if alive(person,year):
                    if year not in alive_by_year:
                        alive_by_year[year] = 1
                    else:
                        alive_by_year[year] += 1
        
            if alive_by_year[year] > alive_by_year[maxyear]:
                maxyear = year
    
    return maxyear
    
def alive(person,year):
    """Returns whether or not a person was alive in a given year.
    
    Args:
        person: A tuple of ints
        year: An int.
    
    Returns:
        A Boolean.
    """
    return year >= person[0] and (person[1] is None or year <= person[1]) 
    
# Another approach takes advantage of the fact that how people's birth and
# death years line up does not matter. We simply sort the births and deaths
# in chronological order, and keep a running count of the number of people 
# alive as we iterate forwards in time through these births and deaths, 
# keeping a running maximum of people alive. This approach will return the 
# EARLIEST of all such years with the highest number of people alive.

# If we sort the births and deaths in place, then O(1) memory is required 
# and overall the algorithm takes O(N*logN) time. But given that there are 
# a fixed number of possible values for the birth and death years, we could 
# use perform a sort of bucket sort over the input for an overall runtime 
# of O(N). The below algorithm uses O(N) space, storing counts for births
# and deaths per year for all people in O(N) time, and then traverses the 
# years in O(1) time to calculate people alive at each year.

def f2(ppl):
    """Returns a year with the most number of people alive.
    
    Args:
        lst: A list of tuples (birth_year, death_year) for each person.
             These year values are assumed to be ints. If person is still
             Alive, then death_year is None. For each person, it is assumed 
             that birth_year <= death_year
        
    Returns:
        An int when input is nonempty, otherwise None.
    """  
    if len(ppl) == 0: return None

    # Ignore any deaths after 2000 as those years can have only decreases
    # to the population. Input does not include those born after 200.

    changes_per_year = [[0,0] for _ in range(101)] # 1900 to 2000 inclusive
        
    for birth, death in ppl:
        changes_per_year[birth-1900][0] += 1
        if death is not None and death <= 2000:
            changes_per_year[death-1900][1] += 1
    
    # Importantly, we treat as "alive" during a given year the anyone who  
    # was alive at ANY point in the year. So in each new year, we add births,
    # and use this value as the number alive, and only then subtract deaths.
    # Given this, so long as the list is non-empty, at least one year will 
    # have at least one person alive, even if they died that same year.
    
    current_alive = 0
    most_alive = float("-inf")
    
    for i, (births,deaths) in enumerate(changes_per_year):
        current_alive += births
        if current_alive > most_alive:
            most_alive = current_alive
            best_year = 1900 + i
        current_alive -= deaths
    
    return best_year
    
# Sample inputs are below. Note that 1961 is not the ONLY acceptable answer
# for the first input, ans1961a, but it is a correct one.
    
ans1961a = [(1900,1975),(1936,2002),(1961,None),(1945,1978)]
ans1945a = [(1900,1975),(1936,2002),(2000,None),(1945,1978)]
ans1940a = [(1901,1978),(1920,1988),(1980,1993),(1940,1997),(1911,1989), \
            (1936,1982)]
ans1950a = [(1901,1950),(1950,1970)]
ans1901a = [(1901,1949),(1950,1970)]
ans1950b = [(1901,1953),(1950,1970)]
ans1978a = [(1901,1901),(1978,1978),(1978,1978)]

# f1 and f2 return different values for the input ans1940a, but both are
# correct. f2 returns the earliest correct year while f1 returns the correct
# birth year that appears earliest in the input. 
    
def test():
    """Tests some sample inputs."""
    inputs = [ans1961a,ans1945a,ans1940a,ans1950a,ans1901a,ans1950b,ans1978a]
    
    for input in inputs:
        print(f1(input),f2(input))