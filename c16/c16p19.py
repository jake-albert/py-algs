import sys
sys.path.append('..')
from data_structs import DequeQueue

# c16p19

# Pond Sizes: You have an integer matrix representing a plot of land, where
# the value at that location represents the height above sea level. A value of
# zero indicates water. A pond is a region of water connected vertically, 
# horizontally, or diagonally. The size of the pond is the total number of
# connected water cells. Write a method to compute the sizes of all ponds in 
# the matrix.
#
# EXAMPLE
# Input:
#    0 2 1 0
#    0 1 0 1
#    1 1 0 1
#    0 1 0 1
# Output: 2, 4, 1 (in any order) 

##############################################################################

# Where R is the number of rows and C the number of columns, this approach 
# operates in O(R*C) time, not touching any one space any more than a constant
# number of times (This constant number is not perfectly minimized because
# in the BFS implementation below, a neighbor space may be added to the queue, 
# then added again by a different neighbor, and then visited once to be
# processed, and then visited once more to be ignored. Still, it can be added 
# no more than 8 times by its 8 neighbors. DFS would likely have fewer average
# visits per space but depending on implementation could have its own costs 
# with repeated recursive calls taking more time.)

# O(R*C) space is required for memoization if we are not permitted to alter 
# the input matrix. If we were, we could change values at visited spaces to
# some non-integer value such as the None object, or redefine input to permit
# only positive values so that we could set visited spaces to -1.

def f1(M):
    """Calculates the sizes of all ponds.
    
    Args:
        M: A list of lists of integers. Assumes that the matrix is well
        formed; that is, that the rows are all of equal length, and 
        that the columns are all of equal length. Any non-zero value is 
        interpreted as land.
    
    Returns:
        A list of integers.
    """
    if len(M) == 0 or len(M[0]) == 0:  # No ponds or land.
        return [] 
    
    rows, cols = len(M), len(M[0])
    memo = set()  # Set of already-explored coordinate pairs.
    sizes = []
    
    for i in range(rows):
        for j in range(cols):
            if (i,j) not in memo:
                if M[i][j] == 0:
                    sizes.append(get_pond_size(i,j,M,memo,rows,cols))
                else:
                    memo.add((i,j))
    
    return sizes
    
def get_pond_size(i,j,M,memo,rows,cols):
    """Given coordinates for an unvisited space with water, calculates
    the size of the pond with this space in it using BFS.
    
    Args:
        i,j: Integer coordinates for the row and column of the space.
        M: A list of list of integers.
        memo: A set of tuples representing visited spaces.
        rows,cols: Integer numbers of rows and column in matrix used
          for boundary checking.
        
    Returns:
        An integer.
    """
    size = 0
    queue = DequeQueue()
    queue.add((i,j))
    
    while not queue.isEmpty():
        x,y = queue.remove()
        if (x,y) not in memo:
            memo.add((x,y))
            if M[x][y] == 0:  # Part of the pond we are interested in.
                size += 1
                add_surrounding_spaces(queue,x,y,rows,cols,memo)
        
    return size    

def add_surrounding_spaces(queue,x,y,rows,cols,memo):
    """Adds to queue inbound, unexplored spaces surrounding (x,y).""" 
    for a in [x-1,x,x+1]:
        for b in [y-1,y,y+1]:
            if 0<=a and a<rows and 0<=b and b<cols and (a,b) not in memo:
                queue.add((a,b))

# Some test inputs below.
                
# Three ponds: [2,4,1]                
input1 = [[0,2,1,0],
          [0,1,0,1],
          [1,1,0,1],
          [0,1,0,1]]

# Five ponds: [2,6,2,4,1]          
input2 = [[0,2,1,0,0,3,3,0,0,5],
          [0,1,0,1,0,1,1,1,1,1],
          [1,1,0,1,2,2,2,1,0,0],
          [0,1,0,1,1,1,0,0,3,2]]   

# One very large pond: [256000]
input3 = [[abs(i%2 - j%2) for j in range(100)] for i in range(512)]          
        
# [[0,1,0,1,0,1,0,1,0,1,0,1,0,1...],
#  [1,0,1,0,1,0,1,0,1,0,1,0,1,0...],
#  [0,1,0,1,0,1,0,1,0,1,0,1,0,1...],
#  [1,0,1,0,1,0,1,0,1,0,1,0,1,0...],
#  [0,1,0,1,0,1,0,1,0,1,0,1,0,1...],
#  [1,0,1,0,1,0,1,0,1,0,1,0,1,0...], 
#  .  
#  .   
#  .   
#  . 
#  [1,0,1,0,1,0,1,0,1,0,1,0,1,0...]]

def test():
    """Tests the above 3 inputs."""
    for input in [input1,input2,input3]:
        print(f1(input))