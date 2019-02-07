from random import randint

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
# all-black subsquare is either A) the FULL NxN square if all constituent 
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
#           █ ██        │____│   │____│   │█_█_│   │__██│ 

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

def get_memo(M,N):
    """Returns a memo that stores two values for every position (r,c) 
    in a square matrix M of dimension n:
   
        A) The number of black pixels in the longest uninterrupted 
        sequence starting at (r,c) and extending to the right; and
        B) The same, but for a sequence extending down.
        
    Args:
        M: A list of lists of ints 0 or 1.
        N: The dimension of the matrix. 
        
    Returns:
        A list of lists of ints with values from 0 to n inclusive.
    """

    # Python for loops are relatively slow, so it would be wise to 
    # re-write using NumPy in any situation where speed really matters.
    
    memo = [[[0,0] for _ in range(N)] for _ in range(N)]
    
    for r in range(N-1,-1,-1):
        for c in range(N-1,-1,-1):
            if M[r][c] == BLACK:            
                memo[r][c][0] = memo[r][c+1][0] + 1 if c < N-1 else 1
                memo[r][c][1] = memo[r+1][c][1] + 1 if r < N-1 else 1
                
    return memo

# Once this preprocessing is done, we can traverse pixels in the matrix by its
# 2N+1 diagonals from bottom-right to upper-left, making O(1) computations at 
# each pixel to find the largest black subsquare with upper-left corner at 
# that pixel.

# The basic idea is that when moving within an all-black square from its 
# bottom-right corner to its top-left corner, the minimum of the length of the
# longest sequence of all-black pixels extending from that pixel to the right
# and from that pixel down always increases:

#                                           4
#           ████                     3     4████
#           ████              2     3███    █
#           ████       1     2██     █      █
#           ████      1█      █      █      █  

# This minimum might increase by 1 at each step, as above, by more than 1:

#                                           5
#           █████                    4     5████
#           ████              2     3███    █
#           █████      1     3███    █      █
#          █████      1█      █      █      █  
#           ██                       █      █

# But either way indicates that the largest all-black square with upper-left 
# corner has a dimension ONE larger than that of the largest all-black square 
# with upper-left corner at the previous pixel down and to the right.

# On the other hand, if this minimum ever decreases, the dimension of the 
# largest all-black square with a corner at that pixel decreases to that 
# minimum:

#                                           4
#           ██ █                     3     2██
#           ████              2     3███    █
#           ████       1     2██     █      █
#           ████      1█      █      █      █  
 
# Whereas the recursive solution I wrote above returns only one max black 
# subsquare, my below approach returns all such squares when there are more 
# than one.
 
class Output:
    """Represents an output of all max black subsquares.
    
    Attributes:
        dim: An int. The dimension of the subsquares.
        array: A list of tuples representing the upper-left corners.
    """ 
    
    def __init__(self):
        """Inits an output representing no black subsquares."""
        self.dim = 0
        self.array = [] 
    
    def __eq__(self,other):    
        """Returns True iff two outputs represent same subsquares.""" 
        return self.dim == other.dim and                \
               sorted(self.array) == sorted(other.array)

    def __str__(self):
        """Returns string for pretty-printing output."""
        if self.dim == 0:
            return "No black subsquares."
            
        builder = [f"Max dimension is {self.dim} with UL corners at:"]
        for point in self.array:
            builder.append(str(point))
        return "\n".join(builder)
               
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
    
    N = len(M)
    memo = get_memo(M,N)
    output = Output()
    
    # We explore diagonals from the "center" spine, where the largest 
    # possible black subsquare can be, outward. 
    
    for x in range(N):    
        
        # Get the coordinates of the bottom-right corners of all 
        # diagonals with an "offset" of x from the center. For example, 
        # when x is 3 for some 4x4 matrix, the "diagonals" are single 
        # pixels at the upper-right and bottom-left corner. 

        diags_start = [(N-1,N-1)] if x == 0 else [(N-1,N-1-x),(N-1-x,N-1)]
        for diag_start in diags_start:
            check_diag(memo,diag_start,output)
        
        # If after updating the max subsquares seen in the diagonals,
        # we see that they have a dimension that later diagonals cannot 
        # possibly beat, exit early. For example, a 4X4 black subsquare 
        # found with upper-left corner at (0,1) in a 5X5 matrix cannot 
        # possibly be beat by subsquares with upper-left corners in 
        # more outward diagonals.
        
        if output.dim == N-x:
            return output
        
    return output   
    
def check_diag(memo,diag_start,output):
    """Finds the largest black subsquare with upper-left corner in a 
    given diagonal, and update global max subsquare if it is larger.
    
    Args:
        memo: A list of lists of ints.
        diag_start: A tuple of ints representing the bottom-right 
          corner of the diagonal.
        output: An Output instance.
    """        
    i,j = diag_start
    cur_dim = 0
    
    while i >= 0 and j >= 0:
        
        to_right, to_down = memo[i][j]      
        if to_right > cur_dim and to_down > cur_dim:
            cur_dim += 1
        else:
            cur_dim = min(to_right,to_down)
        
        # If a subsquare is larger than the previous subsquares stored,
        # we replace them. (Notice that the name "output.array" is 
        # simply reassigned to a new object here. I had originally 
        # continued appending to the same array and kept another value,
        # "start", that marked where the new max subsquares began in 
        # that array, but got rid of that for simplicity's sake. Now, 
        # the Python garbage collector works to deallocate all of the 
        # tuple objects in array when we reassign the name. Altogether,
        # though, no more than O(N) work is done per call to the whole 
        # check_diag() function, as no more than O(N) values can be in 
        # the array at any one time.)
        
        if cur_dim > output.dim:            
            output.dim = cur_dim
            output.array = [(i,j)]
            
        # Ignore any black squares of dim 0 (white pixels).
        
        elif cur_dim > 0 and cur_dim == output.dim:
            output.array.append((i,j))
    
        i-=1
        j-=1
  
def test():
    """Tests some sample inputs."""
    test_matrices = [[[1,1,0],
                      [1,1,1],
                      [1,1,1]],
                    
                    # ^ ans: (0,0),(1,0),(1,1) with dim 2
                    
                     [[0,0,0],
                      [0,0,0],
                      [0,0,0]],
                      
                    # ^ ans: no black subsquares
                    
                     [[1,0,1,1,1,1],
                      [0,1,1,0,1,1],
                      [1,1,1,1,0,1],
                      [1,1,1,0,0,1],
                      [1,1,1,0,1,1],
                      [0,1,1,1,1,1]],     
                    
                    # ^ ans: (2,0) with dim 3              
           
                     [[1,0,0,1,1],
                      [1,0,1,1,1],
                      [1,1,1,1,1],
                      [1,1,1,1,1],
                      [1,1,1,1,1]],       
                    
                    # ^ ans: (2,0),(2,1),(2,2),(1,2) with dim 3   
                     
                     [[1,0,0,0,0],
                      [0,1,1,1,0],
                      [1,1,1,1,0],
                      [1,1,1,1,0],
                      [1,1,0,0,1]],    
                    
                    # ^ ans: (1,1) with dim 3
                    
                     [[0,1,1,1,1,1,1,0],
                      [1,0,1,0,1,1,0,1],
                      [1,1,0,1,1,0,1,1],
                      [1,1,1,0,0,0,1,1],
                      [1,1,0,0,0,1,1,1],                 
                      [1,1,0,1,1,0,1,1],
                      [1,0,1,1,1,0,0,1],
                      [0,1,1,1,1,1,1,0]],
                    
                    # ^ ans: (0,4),(2,0),(2,6),(3,0),(3,6),(4,0),(4,6),
                    #      (5,3),(6,3),(6,2) with dim 2
    
                     [[1 for _ in range(1000)] for _ in range(1000)]]   
                    
                    # ^ ans: (0,0) with dim 1000
                    
    for M in test_matrices:    
        print(f1(M))

# To test more rigorously for correctness, I wrote up a slightly optimized 
# version of the brute-force O(N^6) solution.
        
def f2(M):
    """Brute-force version of f1 above."""
    
    # We simply reject incorrectly sized input.
    
    if len(M) == 0:
        raise ValueError("M is empty.")
    elif [len(M[i]) for i in range(len(M))] != [len(M)]*len(M):
        raise ValueError("M is not a square matrix.")
    
    output = Output()
    early_term = False
    
    # Test from larger dimensions to smaller in order to exit early.
    
    for D in range(len(M),0,-1):
        
        if early_term: break
        
        for r in range(len(M)-D+1):
            for c in range(len(M)-D+1):
        
                if all_black(M,r,c,D):
                    if output.dim == 0:
                        output.dim = D
                        early_term = True
                    output.array.append((r,c))
    
    return output
    
def all_black(M,r,c,D):
    """Returns whether or not subsquare with upper-left corner at 
    (r,c) and dimension D consists entirely of black pixels."""    
    for i in range(r,r+D):
        for j in range(c,c+D):
            if M[i][j] != BLACK:
                return False
    return True
     
def rand_test(trials,dim):
    """Tests f1 against brute-force f2 on randomly generated input.
    
    Args:
        trials: Number of inputs to create and test.
        dim: Dimension of test matrices.
        
    Raises:
        AssertionError: f1 and f2 disagree.
    """
    for trial in range(trials):
        M = [[randint(0,1) for _ in range(dim)] for _ in range(dim)]
        o_01, o_02  = f1(M), f2(M) 
        
        try:
            assert o_01 == o_02 
        except:
            print(M)
            print(o_01)
            print(o_02)