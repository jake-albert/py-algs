# c17p23

# Max Black Square: Imagine you have a square matrix, where each cell (pixel)
# is either black or white. Design an algorithm to find the maximum subsquare
# such that all four borders are filled with black pixels. 

##############################################################################

# The wording of this problem is a little ambiguous. Does it mean that the 
# full subsquare, including pixels that are part of the square but not its
# borders, must also be black, or can they be any color? Is the solution on 
# the input below the 10x10 square, or the 3x3 square inside of it?

#                                ██████████
#                                █        █
#                                █        █
#                                █        █
#                                █   ███  █
#                                █   ███  █
#                                █   ███  █
#                                █        █
#                                █        █
#                                ██████████

# I assumed when writing my solution that the meaning is that the subsquare
# must be fully black, including pixels within its borders (so the 3x3 one).

# First, we consider the search space. A unique subsquare of an NxN matrix can
# be defined by an UPPER-LEFT CORNER and DIMENSION. For example, in a 5x5:

#                                  0 1 2 3 4
#                              0 [ 1 0 1 1 1 ]
#                              1 [ 0 1 1 1 1 ]
#                              2 [ 1 0 1 1 1 ]
#                              3 [ 0 1 1 0 1 ]
#                              4 [ 1 0 1 1 1 ]

# There are 5*5 unique subsquares with dimension 1, and 4*4 with dimension 2, 
# because only the points in the top-left 4x4 positions can be an upper-left
# corner for a subsquare of dimension 2. Altogether, there are O(N^2) 
# positions that can be an upper-left corner and O(N) dimensions, meaning that
# there are O(n^3) total subsquares to check.

# One brute-force way would be to simply check all of the O(N^2) pixels inside
# each of these O(N^3) subsquares to find all-black subsquares, keeping track 
# of the largest ones seen so far. It requires O(1) memory and O(N^5) time.

# Another approach is to consider solving subproblems. We know that every NxN
# square is made of 4 overlapping (N-1)X(N-1) subsquares, and that the largest
# all-black subsquare is either A) the FULL NxN square if all constituenet 
# subsquares' max black subsquares are themselves, or B) the largest max black
# subsquare among the four constituent squares otherwise:

#  CASE A:               ____     ____     ____     ____   
#           ████        │███ │   │ ███│   │    │   │    │         
#           ████    ==\ │███ │ , │ ███│ , │███ │ , │ ███│
#           ████    ==/ │███ │ , │ ███│ , │███ │ , │ ███│
#           ████        │____│   │____│   │███_│   │_███│ 

#  CASE B:               ____     ____     ____     ____   
#           ████        │███ │   │ ███│   │    │   │    │         
#           ███     ==\ │███ │ , │ ██ │ , │███ │ , │ ███│
#           ████    ==/ │███ │ , │ ███│ , │███ │ , │ ███│
#           █ ██        │____│   │____│   │█ █_│   │_ ██│ 

# We can then write a solution on matrix M and length N, with a recursive 
# function that is called on subsquares defined by a UL corner and dim:

# main_call(M,N):
#     return best((0,0),N)
#
# best((row,col),D):
#     if D is 1, return ((row,col),1) if pixel is BLACK else None
#     if D is greater then one, 
#         find UL as best((row,col),D-1),
#              BL as best((row+1,col),D-1),
#              BR as best((row+1,col+1),D-1),
#              UR as best((row,col+1),D-1)
#         if all of UL, BL, BR, UR have dim of D-1 meaning they are full, 
#             return ((row,col),D)
#         else
#             return whichever of the four has D of greatest value
             
# To avoid repeating recursive calls, we could keep a 3-dimensional memo that
# stores the results of best() for EVERY subsquare. The above algorithm would 
# then need O(N^3) space and can return in O(N^3) time, since it performs 
# O(1) work for each of the subsquares. We also can reduce space requirements 
# by carefully managing the order that we traverse the squares. Finding the  
# max subsquare with a certain D value requires only information about max 
# subsquares of dim D-1, so it is possible to solve for max subsquares one D 
# at a time, iteratively, and thus store at most O(N^2) values at any time. 

# I wrote a faster approach below that takes O(N^2) preprocessing time and 
# uses O(N^2) space in order to be able to return the max black submatrix in 
# O(N^2) time. First, the preprocessing step is below.

# For this small example, I assume that the input are simply lists of lists of
# integers, with only values 0 for white and 1 for black. I define "BLACK" 
# below rather than develop a class for the input matrices, which would make 
# working with them easier in larger application but is unnecessary here.

BLACK = 1

def get_memo(M,n):
    """Returns a memo such that stores two values for every position 
    (r,c) in a square matrix M of dimension n:
   
        A) The number of black pixels in the longest uninterrupted 
        sequence starting at (r,c) and extending to the right; and
        B) The same, but for a sequence extending down.
        
    Args:
        M: A list of lists of ints 0 or 1.
        n: The dimension of the matrix. 
        
    Returns:
        A list of lists of ints with values from 0 to n inclusive.
    """

    # Python for loops are relatively slow, so it would be wise to 
    # re-write using NumPy in any situation where speed really matters.
    
    memo = [[[0,0] for _ in range(n)] for _ in range(n)]
    
    for r in range(n-1,-1,-1):
        for c in range(n-1,-1,-1):
            if M[r][c] == BLACK:            
                memo[r][c][0] = memo[r][c+1][0] + 1 if c < n-1 else 1
                memo[r][c][1] = memo[r+1][c][1] + 1 if r < n-1 else 1
                
    return memo

class Output:

    def __init__(self):
        self.array = []
        self.start = 0
        self.best = 0

def f1(M):
    """Returns the largest fully black submatrix of square matrix M.
    
    Args:
        M: A list of list(s) of ints. The function enforces that M is
          square, with equal numbers of rows and columns, and assumes
          that the ints are only of values 0 for white and 1 for black.
    
    Returns:
        An Output instance.
    
    Raises:
        ValueError: M is empty or is not square.
        TypeError: M has non-int elements that do not support addition.
    """
    
    # We simply reject incorrectly sized input.
    
    if len(M) == 0:
        raise ValueError("M is empty.")
    elif [len(M[i]) for i in range(len(M))] != [len(M)]*len(M):
        raise ValueError("M is not a square matrix.")
    
    n = len(M)
    memo = get_memo(M,n)
    output = Output()
    
    for d in range(n):    
        
        # update the output to hold the best full matrices we have found so far
        diags_start = [(n-1,n-1)] if d == 0 else [(n-1,n-1-d),(n-1-d,n-1)]
        for diag_start in diags_start:
            check_diag(memo,n,diag_start,output)
        
        # we can exit early if we have checked a diagonal with the best possible 
        # max square that it can hold, such as a 4X4 from (0,1) in a 5X5 matrix        
        if output.best == n-d:
            return output
        
            
    # otherwise, we simply return the best that we have found so far
    return output   


    
def check_diag(memo,n,diag_start,output):

    i,j = diag_start
    current = 0
    
    # keep moving up and to the left until hit a wall
    while i >= 0 and j >= 0:
        
        # we are part of a full subsquare of dim n as long as these values continue
        # to be greater than or equal to n for every point on the diagonal
        to_right, to_down = memo[i][j]       
        
        if to_right > current and to_down > current:
            current += 1
        else:
            current = 1 if to_right > 0 and to_down > 0 else 0
                 
        if current > 0:
        
            # replace best if found first subsquare of bigger size
            if current > output.best:            
                output.best = current
                #output = [((i,j),best)]
                output.array.append((i,j))
                output.start = len(output.array)-1
                
            # otherwise, just append it to the list of best subsquares    
            elif current == output.best:
                output.array.append((i,j))
        
        i-=1
        j-=1
  
# pretty printing for the output    
def print_output(output):
    print(f"Best subsquare dimension is {output.best}")
    for point in output.array[output.start:]:
        print(point)  

def test():
                
    
    test_matrices = [[[1,0,1,1,1,1],
                      [0,1,1,0,1,1],
                      [1,1,1,1,0,1],
                      [1,1,1,0,0,1],
                      [1,1,1,0,1,1],
                      [0,1,1,1,1,1]],     
                    # ans: (2,0) with dim 3              
           
                     [[1,0,0,1,1],
                      [1,0,1,1,1],
                      [1,1,1,1,1],
                      [1,1,1,1,1],
                      [1,1,1,1,1]],       
                    # ans: (2,0),(2,1),(2,2),(1,2) with dim 3   
                     
                     [[1,0,0,0,0],
                      [0,1,1,1,0],
                      [1,1,1,1,0],
                      [1,1,1,1,0],
                      [1,1,0,0,1]],    
                    # ans: (1,1) with dim 3
                    
                     [[0,1,1,1,1,1,1,0],
                      [1,0,1,0,1,1,0,1],
                      [1,1,0,1,1,0,1,1],
                      [1,1,1,0,0,0,1,1],
                      [1,1,0,0,0,1,1,1],                 
                      [1,1,0,1,1,0,1,1],
                      [1,0,1,1,1,0,0,1],
                      [0,1,1,1,1,1,1,0]],
                    # ans: (0,4),(2,0),(2,6),(3,0),(3,6),(4,0),(4,6),
                    #      (5,3),(6,3),(6,2) with dim 2
    
                     [[1 for _ in range(1000)] for _ in range(1000)]]   
                    # ans: (0,0) with dim 1000
                    
    for M in test_matrices:    
        print_output(f1(M))