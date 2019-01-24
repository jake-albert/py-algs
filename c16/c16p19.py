# start

# this approach operates in O(m*n) time, not touching any one square any more than 
# a constant number of times. (This is most often 1, but in the bfs search implementation
# below the queue sometimes can have duplicates up. DFS would probably be better here).

from queue import DequeQueue

def f1(M):

    # we are allowed to assume the input is a MATRIX; that is, the rows and columns
    # are all of equal length. We need to check that this is not an empty matrix, however
    if len(M) == 0 or len(M[0]) == 0:
        return []  # no ponds, no land either
    
    # in a substantive input, then, we get the numbers of rows and columns
    rows, cols = len(M), len(M[0])
    
    # our memo is a set of coordinate pairs, that will require O(m*n) space
    memo = set()
    
    # we output a list of sizes, in any order, preserving duplicates
    sizes = []
    
    # we check every square at most once
    for i in range(rows):
        for j in range(cols):
            if (i,j) not in memo:
                if M[i][j] == 0:
                    sizes.append(get_size(i,j,M,memo,rows,cols))
                else:
                    memo.add((i,j))
    
    return sizes
    
def get_size(i,j,M,memo,rows,cols):
    
    # initialize for bfs
    size = 0
    queue = DequeQueue()
    queue.add((i,j))
    
    # bfs until queue is empty
    while not queue.isEmpty():
    
        # explore the current point if yet unexplored
        x,y = queue.remove()
        if (x,y) not in memo:
            memo.add((x,y))
            
            # if part of a pond, add to size
            if M[x][y] == 0:
                size += 1
                
                # and also explore all surroundings that are inbounds and unexplored
                for a in [x-1,x,x+1]:
                    for b in [y-1,y,y+1]:
                        if 0<=a and a<rows and 0<=b and b<cols and (a,b) not in memo:
                            queue.add((a,b))
    
    return size
                
input1 = [[0,2,1,0],
          [0,1,0,1],
          [1,1,0,1],
          [0,1,0,1]]

input2 = [[0,2,1,0,0,3,3,0,0,5],
          [0,1,0,1,0,1,1,1,1,1],
          [1,1,0,1,2,2,2,1,0,0],
          [0,1,0,1,1,1,0,0,3,2]]   

input3 = [[abs(i%2 - j%2) for j in range(100)] for i in range(512)]          
    
"""    
[[0,1,0,1,0,1,0,1,0,1,0,1,0,1...],
 [1,0,1,0,1,0,1,0,1,0,1,0,1,0...],
 [0,1,0,1,0,1,0,1,0,1,0,1,0,1...],
 [1,0,1,0,1,0,1,0,1,0,1,0,1,0...],
 [0,1,0,1,0,1,0,1,0,1,0,1,0,1...],
 [1,0,1,0,1,0,1,0,1,0,1,0,1,0...], 
 .  
 .   
 .   
 . 
 [1,0,1,0,1,0,1,0,1,0,1,0,1,0...]]
    
    
    
    
    
    
    
    
    
    
    
    
    
    