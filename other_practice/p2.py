# p2

# An exercise in recursion and combinatorics thought up by my friend Ben. 
#
# Consider a 3x3 grid. Each cell is filled with a single digit, 1-9 (no 
# zeroes), but the digits must obey certain rules. For example:
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
# that square given the state of the board, and for each such digit, put it 
# and recursively call the function on the next position. Each time that all 9
# squares have been filled, display the result. Before each recursive call
# returns up the call stack, set the square back to blank.

# Asymptotic notation is not very helpful here to describe performance, as the
# grid being considered is always the same size. No more than 10 recursive
# calls must be kept on the call stack at any one time, so memory requirements 
# do not grow with the (potentially large) number of possible grids that can 
# be created. There are 9^9, or 387,420,489, unique arrangements of digits on 
# a grid, but this approach places only digits that can still legally be put
# on the grid as it goes along, pruning off the vast majority of the options.
# (On my machine it counts all valid grid arrangements in 0.91 seconds.)

# The class below simulates a grid as it is being produced and is built with 
# methods that make writing the recursive algorithm very easy. It could be 
# redesigned to handle square grids of any dimension with some effort, so long
# as the rules for valid rows and columns are clarified. (What values are
# allowed? What kinds of "straights" are permitted? What kinds of special 
# combinations are permitted?) 

class Grid:
    """Simulates a grid in progress of being filled in with digits 
    according to the rules described above.
    
    Attributes:
        BLANK: An integer representing a blank square. Here, -1.
        sqs: A list of length 9 representing the squares of the grid,
             top left to bottom right.
    """ 
    
    BLANK = -1

    def __init__(self):
        """Inits Grid to be entirely blank."""
        self.sqs = [self.BLANK] * 9
    
    def is_blank(self,i):
        """Returns True if ith square is blank, False otherwise."""
        return self.sqs[i] == self.BLANK
    
    def set_square(self,i,dig):
        """Sets the ith square of the grid to hold a digit."""
        if dig < 1 or dig > 9:
            raise ValueError("Invalid input: Digit must be integer 1 to 9.")
        self.sqs[i] = dig
    
    def clear_square(self,i):
        """Sets the ith square back to a BLANK value."""
        self.sqs[i] = self.BLANK
    
    def display(self):
        """Pretty prints the grid."""
        print(" _____")
        for i in range(len(self.sqs)):
            if i%3 == 0:
                print("|",end="")
            if i%3 == 2:
                print(self.sqs[i],end="")
                print("|",end="\n")
            else:
                print(self.sqs[i],end=" ")
        print(" ¯¯¯¯¯")
    
    def all_valid_digits(self,i):
        """Returns an iterable containing each of the digits 1-9 that 
        may be placed at the ith square without violating any row or 
        column rules. Assumes that the ith square is blank.
        """
        
        # The other digits in the ith square's row and column set
        # constraints on which digits are valid. If no constraints,
        # then all digits are valid. If only one of the row and column
        # constrains to a set of digits, then those digits are returned 
        # immediately. Otherwise, the sets' intersection is returned.
        
        rds, cds = self._row_digits(i), self._column_digits(i)
        
        if rds is None and cds is None:  
            return range(1,10)
        elif rds is None:  
            return self._valid_digits(cds) 
        elif cds is None:  
            return self._valid_digits(rds) 
        else:  
            rvds, cvds = self._valid_digits(rds), self._valid_digits(cds)
            return rvds.intersection(cvds)
     
    def _row_digits(self,i):
        """Returns the digits in the same row as the ith square, or 
        None if no such digits exist. Assumes that the ith square is 
        blank.
        """
        i0 = i//3*3  # ex. "3" for 3,4,5. 
        digs = [self.sqs[j] for j in range(i0,i0+3) if not self.is_blank(j)]
        return self._format_digs(digs)
    
    def _column_digits(self,i):
        """Returns the digits in the same column as the ith square, or 
        None if no such digits exist. Assumes that the ith square is 
        blank.
        """
        i0 = i%3  # ex. "2" for 2,5,8.
        digs = [self.sqs[j] for j in range(i0,i0+7,3) if not self.is_blank(j)]
        return self._format_digs(digs)
        
    def _format_digs(self,digs):
        """Ensures that the digits are returned as a list in increasing 
        order, or the None object if there are no digits. When called by 
        functions like row_digits and column_digits, the input digs list 
        is guaranteed to hold at most 2 digits.
        """
        if len(digs) == 0:
            return None
        elif len(digs) == 1:
            return digs
        else:
            return [min(digs[0],digs[1]), max(digs[0],digs[1])]       
    
    def _valid_digits(self,ds):
        """Given a list of either one or two digits from the same group
        (a row or column), returns a set of valid digits that can join 
        this group.
        """
        if len(ds) == 1:
            return self._valid_digits_one(ds[0])
        else:
            return self._valid_digits_two(ds)
            
    def _valid_digits_one(self,d):
        """Given a single digit, returns the set of valid digits that 
        could be added to a group with that digit.
        
        For example, if d is 1, returns {1,2,3,4,5,7}. 6,8,9 cannot 
        exist in the same group as 1 so they are left out.
        """
        
        # Digits can form a 0-straight, 1-straight, 2-straight, or 
        # 3-straight of values (order not mattering). This means that 
        # if a group contains a single number d, any digit that is 
        # within plus-or-minus 0,1,2,3,4, or 6 may join that group.
        # (So long as it is within range of 1-9 inclusive.)
        
        # The special case of group [2,4,8] is already handled here, as
        # each of the values of this group are within 2,4, or 6 of one 
        # another.
        
        diffs = [x for x in range(-4,5)]
        diffs.append(-6)
        diffs.append(6)
        
        return {d+diff for diff in diffs if 0<d+diff<10}
        
    def _valid_digits_two(self,ds):
        """Given a list of two digit, returns the set of valid digits
        that could be added to complete a group with those digits.
        
        For example, if d is [5,7], returns {3,6,9}. Other digits
        cannot be added.
        
        Assumes that the list ds is sorted in increasing order.
        """
        
        output = set()
        
        # One possibility to complete a group would be to be an
        # "external" addition to a straight that extends the pattern.
        # These include going up ([2,4] and then 6) and going down
        # ([8,9],and then 7.). 0-straights are also handled the same.
        
        diff = ds[1] - ds[0]
        if 0 <= diff <= 3:  
            candidate1 = ds[1] + diff 
            candidate2 = ds[0] - diff
            if candidate1 < 10:
                output.add(candidate1)
            if candidate2 > 0:
                output.add(candidate2)
                
        # Another possibility to complete a group would be to be an 
        # "internal" addition ([2,8] with 5 in the middle). This case 
        # occurs only when the two digits' average is an integer.
                
        sum = (ds[0]+ds[1])
        if sum % 2 == 0:
            output.add(sum//2)
        
        # Valid digits from the special "248" case are hard-coded.
        
        if ds == [2,4]:
            output.add(8)
        elif ds == [4,8]:   
            output.add(2)
        elif ds == [2,8]:
            output.add(4)
        
        return output
        
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
        
from time import time

def time_test():
    """Tests the time to count all valid squares without hashing or 
    printing.
    """
    start = time()
    f1()
    end = time()
    return end-start