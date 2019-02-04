from random import randint

# c17p24

# Max Submatrix: Given an NxN matrix of positive and negative integers, write
# code to find the submatrix with the largest possible sum. 

##############################################################################

# If a matrix has multiple submatrices with the largest possible sum, should 
# we return all of them, or is just one sufficient? I assume below that only 
# one such submatrix is needed.

# We can define a unique submatrix by its UPPER-LEFT and BOTTOM-RIGHT corner. 
# For each of the O(N^2) cells that can be defined to be an upper-left corner,
# O(N^2) cells to the right or below that cell can be a bottom-right corner, 
# so the search space of submatrices is in O(N^4).

# The most brute-force of brute-force approaches would be to, for each of 
# these unique submatrices, calculate the sum from scratch in O(N^2) time and
# compare against a a running maximum. This takes O(N^6) time and O(1) space. 

# We can improve this method with preprocessing that allows us to calculate 
# the sum of any submatrix in O(1) time, bringing the runtime down to O(N^4). 
# We take O(N^2) time to store in some memo S the sums of all submatrices with
# top-left corner at some cell X and bottom-right corner at the bottom-right 
# of the full matrix, and thus can compute the sum of any submatrix by adding
# and subtracting at most four values. (Below, S[A] - S[B] - S[C] + S[D]).

#   0   1   2   3   4   5   6   7   8   9   0   1  
#
#   0   1   2   3   4   5   6   7   8   9   0   1
#
#   0   1   2   3   4   5   6   7   8   9   0   1
#                   _________________   
#   0   1   2   3  │A   5   6   7   8│ *B*  0   1
#                  │                 │  
#   0   1   2   3  │4   5   6   7   8│  9   0   1
#                  │                 │
#   0   1   2   3  │4   5   6   7   8│  9   0   1
#                  │                 │
#   0   1   2   3  │4   5   6   7   8│  9   0   1
#                  │                 │
#   0   1   2   3  │4   5   6   7   8│  9   0   1
#                  │                 │
#   0   1   2   3  │4   5   6   7   8│  9   0   1
#                   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ 
#   0   1   2   3  *C*  5   6   7   8  *D*  0   1
#
#   0   1   2   3   4   5   6   7   8   9   0   1
#
#   0   1   2   3   4   5   6   7   8   9   0   1

# My best solution exploits the fact that given a single-dimension array, we 
# can find the subarray with maximum sum in O(N) time and O(1) space.

# This involves picking one ROW, such as the top/0th, and creating a memo in 
# O(N^2) time of all of the cumulative sums down from that top row the column: 

#    [  -10    7   -8    9    ]  is memoized as  [  -10    7   -8    9   ]  
#    [    5   -1   -8   -4    ]                  [   -5    6  -16    5   ] 
#    [   -9    4   -4   -4    ]                  [  -14   10  -20    1   ] 
#    [    5    7    9    7    ]                  [   -9   17  -11    8   ]

# (From here on, I describe a submatrix as having upper-left corner UL=(r1,c1)
# and bottom-right corner BR=(r2,c2).)

# Say that we want to find the sum of the submatrix with UL=(0,0), BR=(2,2). 
# We can do this by summing the values in the third row from the top in the 
# memo, M[2][0] + M[2][1] + M[2][2] = -14 + 10 + -20 = 24, because each of 
# these values represents the cumulative sums of all values in the columns 
# above them. Leaving M[2][0] out of the sum would represent the sum of the 
# submatrix with UL=(0,1), BR=(2,2), and then including M[2][3] in the sum 
# would represent the sum of UL=(0,1), BR=(2,3); in other words, the sums of
# the subarrays of the third row of that memo represent the subs of all 
# submatrices with UL in the top row and BR in the third row, and we can find
# the maximum of such subarrays in O(N) time and O(1) extra space.

# What about repeating this process for submatrices with UL in a different row
# row than the top? Say that we are interested in submatrices with UL in the
# third row and BR in the fourth? Because these submatrices include rows 2 
# and 3 but exclude rows 0 and 1, we can take the values in row M[3] and 
# subtract values in row M[1] to create values that we compare when finding a 
# maximum subarray. 

# Altogether then, using O(N^2) extra space for the memo, we are able to for 
# all O(N^2) pairs of rows "top" and "bottom" find the maximum subarray with 
# "UL" in top and BR in "bottom", giving a total runtime of O(N^3). 

# My approach below makes one more improvement. Given that each iteration 
# over pairs of "top" and "bottom" uses no more than O(N) space, I used a 
# better scheme to calculate cumulative column sums that brings down space 
# requirements to only O(N).

class Output:
    """Class facilitates storage and printing of solution info.
    
    Attributes:
        sum: An int. The max sum of all submatrices.
        UL, BR: Tuples of int indices to the upper-left and 
          bottom-right corners of the max submatrix (row,column).
    """
    
    def __init__(self):
        """Inits an Output object with no solution yet."""
        self.maxsum = float("-inf")     
        self.UL  = (None,None)       
        self.BR  = (None,None)       
    
    def __eq__(self,other):
        """Checks equivalence only of sum of two subarray outputs."""
        return self.maxsum == other.maxsum
    
    def __str__(self):
        """Returns a string for pretty printing the output."""
        return f"Max sum            : {self.maxsum}\n"  \
               f"Upper-left corner  : {self.UL}\n"      \
               f"Bottom-right corner: {self.BR}" 

def f1(M):
    """Returns a submatrix with largest possible sum in O(N^3) time.
    
    Args:
        M: A list of list(s) of ints. The function enforces that M is
          a square matrix, with equal numbers of rows columns.
    
    Returns:
        An Output instance.
    
    Raises:
        ValueError: M is empty or is not square.
        TypeError: M has non-int elements that do not support addition.
    """
    
    # This algorithm also works on non-square matrices, but we reject 
    # them to adhere strictly to the problem description.
    
    if len(M) == 0:
        raise ValueError("M is empty.")
    elif [len(M[i]) for i in range(len(M))] != [len(M)]*len(M):
        raise ValueError("M is not a square matrix.")
    
    # col_sums is initialized to have the length of a row in the
    # matrix. Since M is square, this is also the length of a column,
    # so we can use just the top-level length of M.
    
    col_sums = [None for _ in range(len(M))]  
    output = Output()
    
    # For each pair of rows, we modify col_sums to reflect the 
    # cumulative sum within each column from r1 to r2 inclusive. We 
    # perform element-wise addition any time that r2 differs from r1, 
    # which could be drastically sped up using NumPy arrays, but I 
    # stick to using only "pure" Python in this exercise.   
    
    for r1 in range(len(M)):

        col_sums[:] = M[r1][:]
        
        for r2 in range(r1,len(M)):
 
            if r1 != r2:
                col_sums[:] = [a+b for a,b in zip(col_sums,M[r2])] 
            
            sub_sum, start, end = best_subarray(col_sums)
        
            if sub_sum > output.maxsum:
                output.maxsum = sub_sum
                output.UL  = (r1,start)
                output.BR  = (r2,end)           
            
    return output
            
def best_subarray(A):
    """Given a list of integers, returns the sum, start index, and end 
    index of the contiguous sublist with the highest sum."""
    
    # prev is the maximum sum among all sublists ending at the previous 
    # index, and prevstart is the starting index of the sublist with 
    # that sum. Ex. when i is 1, the maximum sublist is from 0 to 0.
    
    prev, prevstart = A[0], 0
    best, start, end = A[0], 0, 0
    
    for i in range(1,len(A)):
        prev, prevstart = (A[i],i) if prev <= 0 else (prev+A[i],prevstart)
        if prev > best:
            best, start, end = prev, prevstart, i 
 
    return best,start,end  
       
    
def f2(M):
    """Maximally brute-force function that returns a submatrix with
    largest possible sum in O(N^6) time. Useful only to check against
    f1 for correctness on relatively small inputs.
    
    Args:
        M: A list of list(s) of integers. Dimensions are assumed to 
          be equal for all lists, including sublists.
    
    Returns:
        An Output instance.
    """
    output = Output()

    for r1 in range(len(M)):
        for r2 in range(r1,len(M)):
            for c1 in range(len(M)):
                for c2 in range(c1,len(M)):
                    subsum = sum_submatrix(M,r1,c1,r2,c2)
                    if subsum > output.maxsum:
                        output.maxsum = subsum
                        output.UL = (r1,c1)
                        output.BR = (r2,c2)
    
    return output
    
def sum_submatrix(M,r1,c1,r2,c2):
    """Given square matrix M and indices r1,c1,r2,c2, returns the sum
    of the submatrix with UL = (r1,c1) and BR = (r2,c2). Assumes that 
    all four input indices are in range of M."""
    return sum([sum(M[row][c1:c2+1])for row in range(r1,r2+1)])
    
def test(trials,d,minv,maxv):
    """Tests f1 for correctness over randomly generated matrices.

    Args:
        trials: A non-negative int. Number of matrices to test.
        d: A positive int. The dimension of the square matrices.
        minv, maxv: Ints. Min and max possible values in each matrix.
    
    Raises:
        AssertionError: f1 returns an incorrect sum.
    """
    ten_percent = trials // 10
    for trial in range(trials):
    
        if trial % ten_percent == 0:
            print(f"On trial {trial} of {trials}.")
    
        M = [[randint(minv,maxv) for _ in range(d)] for _ in range(d)]

        assert f1(M) == f2(M)