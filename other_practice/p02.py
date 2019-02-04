from p02_grid import Grid
from time import time

# p02

# Funky Sudoku: An exercise in recursion and combinatorics thought up by my
# friend Ben. 
#
# Consider a 3x3 grid. Each cell is filled with a single digit, 1-9 (no 
# zeros), but the digits must obey certain rules. For example:
# 
#    1 2 3
#    5 6 4
#    3 4 5
#
# You are allowed to have duplicates. BUT, each row and column must meet the
# following criteria. The 3 digits must form either:
#
#          a triplet (111,222,333,444,555,666,777,888,999);
#       OR a 1-straight (123,234,345,456,567,678,789); 
#       OR a 2-straight (135,246,357,468,579); 
#       OR a 3-straight (147,258,369);
#       OR the combination 248
#
# Order of the digits within each row and column DOES NOT matter.
#
# Determine the total number of unique grids that fulfill these rules.
# Write a function to print each unique grid as well.

##############################################################################

# My algorithmic approach is pretty simple: Begin with a blank grid and, for 
# each of the 9 squares, determine which digits may still legally be put at 
# that square given the state of the board. For each such digit, put it in 
# and recursively call the function on the next position. Each time that all 9
# squares have been filled, display the result. Before each recursive call
# returns up the call stack, set the square it had filled back to blank.

# Asymptotic notation is not very helpful here to describe performance, as the
# grid being considered is always the same size. No more than 10 recursive
# calls must be kept on the call stack at any one time, so memory requirements 
# do not grow with the (potentially large) number of possible grids that can 
# be created. There are 9^9, or 387,420,489, unique arrangements of digits on 
# a grid, but this approach places only digits that can still legally be put
# on the grid as it goes along, pruning off the vast majority of the options.
# (On my machine it counts all valid grid arrangements in 0.91 seconds.)
        
def f1(prin=False,set_check=False):
    """Explores all valid squares according to argument instructions.
    With default values, counts all unique grids and prints the total 
    number before halting.
    
    Args:
        print: If True, function prints each unique grid that it forms.
        set_check: If True, function hashes each arrangement and reports 
          total number of unique arrangements before halting. Useful to 
          check that no duplicates were counted.
    """    
    grid = Grid()
    total = 0
    grid_set = set() if set_check else None

    total = all_valids(grid,0,total,prin,grid_set)
    
    print(f"{total} total grid arrangements found.")
    if set_check:
        print(f"{len(grid_set)} unique grid arrangements.")
    
def all_valids(grid,i,total,prin,grid_set):
    """Counts all valid grids according to the rules above, in 
    addition to extra instructions from parent function.
    
    Args:
        grid: A Grid instance.
        i: An integer index to the current square to fill.
        total: An integer running total of valid grids.
        prin: A Boolean. Prints each valid grid iff True.
        grid_set: A set of grid arrangements as Tuples of digits.
          If no hashing requested by parent function, is None.
          
    Returns:
        An integer count of valid grids.     
    """
    
    # Base case. Complete grid has been formed.
    
    if i == 9:
        if prin:
            grid.display()
        if grid_set is not None:
            grid_set.add(tuple(grid.sqs))
        return total+1
        
    # Recursive case.
        
    else:
        for val in grid.all_valid_digits(i):
            grid.set_square(i,val)
            total = all_valids(grid,i+1,total,prin,grid_set)
        grid.clear_square(i)  
        return total

def time_test():
    """Measures the time to count all valid squares."""
    start = time()
    f1()              
    end = time()
    return end-start
    
# Calculating the total number of unique, valid grids is almost infeasibly
# messy by hand, but we can at least make a start at it.

# Finding the number of unique, valid top rows is simple. There are a total of
# 9 triplets, which can be arranged in only one order, and 16 straights/"248"
# patterns, which have three unique symbols and thus may be arranged into 6 
# orderings. So the number of unique top rows is 9*1+16*6 = 105. 

# Each row placed in the top placed different constraints on the possible rows
# that can be below it; for instance, because there is no valid row/column
# group containing 1 that also contains a 6, 8, or 9, "111" in the top row 
# narrows the number of valid groups that can fill the middle row from 
# 9*1+16*6 = 105 to 6*1+6*6 = 42. Meanwhile, 5 may appear with any other 
# digit, so all 105 possible rows may appear below "555". This analysis 
# becomes more complex when considering rows made of more than 1 unique digit,
# in which some orderings of groups, but not others, get ruled out. Past this
# point, it is best to use an automated approach to find the exact number. 
# But we at least now have a tighter upper bound of 105^3, or 1,157,625, valid 
# grids when column constraints are ignored.

# The actual number turns out to be, unsurprisingly, much smaller than this at 
# 17,061 unique grids. My friend verified this value with a different approach
# that creates a larger number of grids and rules out invalid ones.