# The class below simulates a valid grid for p02 as it is produced and has 
# methods that make writing the recursive algorithm in p02.py very easy. 

# It could be redesigned to handle square grids of any dimension with some
# effort, so long as the rules for valid rows and columns are clarified. (Ex.
# What values are allowed in each square? What kinds of "straights" are 
# permitted? What kinds of special combinations like "248" are permitted?). 

# But because these rules are not defined, the class is "hard-coded" to handle
# only a dimension of 3, and only 1-9 as permitted values in each square. It 
# thus does NOT define attributes like "DIM", "MINVAL", and "MAXVAL", which is
# generally good practice but here could give the impression that the class is 
# easily modifiable to other cases. 

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
        
        # Valid digits from the special "248" case handled separately.
        
        if ds == [2,4]:
            output.add(8)
        elif ds == [4,8]:   
            output.add(2)
        elif ds == [2,8]:
            output.add(4)
        
        return output