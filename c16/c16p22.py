# start

# so given that this problem takes only K as the input, it seems that the initial 
# configuration of the board is supposed to be the same every time. If the board
# is alternating checkerboard white and black squares, which is one plausible reading 
# the of the problem description in the book, then regardless of the square it starts on,
# its movement is repetitive and not too exciting. It just kind of travels diagonally,
# flipping all of the squares it touches and never doubling back.

#  _______________________                        _______________________
# │█ █ █ █ █ █ █ █ █ █ █ █│                      │█ █ █ █ █ █ █ █ █ █ █ █│
# │ █ █ █ █ █ █ █ █ █ █ █ │                      │ █ █ █ █ █ █ █ █ █ █ █ │
# │█ █ █ █ █ █ █ █ █ █ █ █│                      │█ █ █ █ █ █ █ █ █ █ █ █│
# │ █ █ █ █ █ █ █ █ █ █ █ │        ==>           │ █ █ █ █ ███ █ █ █ █ █ │
# │█ █ █ █ █ █ █ █ █ █ █ █│                      │█ █ █ █ █  ██ █ █ █ █ █│
# │ █ █ █ █ █ █ █ █ █ █ █ │                      │ █ █ █ █ █  ██ █ █ █ █ │
# │█ █ █ █ █ █ █ █ █ █ █ █│                      │█ █ █ █ █ █  ██ █ █ █ █│
# │ █ █ █ █ █ █ █ █ █ █ █ │                      │ █ █ █ █ █ █  ██ █ █ █ │
# │█ █ █ █ █ █ █ █ █ █ █ █│                      │█ █ █ █ █ █ █  ██ █ █ █│
#  ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯                        ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯

# so I am assuming that the intension of the problem is to simulate the ant when 
# all of the squares are WHITE at the start, as this seems to be the main conception
# of the problem and makes for far more interesting behavior.

# Since my instructions are to PRINT the grid at the end of the ant's movements, 
# we have a few choices. We can keep a SET of squares that are black and then 
# ADD to this set when a white square becomes black, and REMOVE if it becomes white
# we can also check for set membership in O(1) time to determine if a square is 
# white or black. This means we can update the grid in O(K) time, where k is the 
# number of steps the ant makes.  

# as for drawing the board, we might want to have a little "buffer" space of white
# untouched spaces so that the pattern is easier to see for a given time. we can as 
# we update spaces, keep track of the north, south, east, and west most that a black 
# space exists and then create an m by n matrix of characters to join together and 
# print. Let's say that we want to create a border of at least one white layer around
# the outermost region with a black square. Then, printing this will take O(m*n) time, 
# which is our best conceivable time complexity for this because we know we have to 
# print out all of the white and black squares in our range.

# let's also decide that the printed board will be square, so we pick whichever is 
# the max of m and n and make those the dimensions. And then have a buffer of one 
# around the whole thing just so it looks nicer.

# and for fun we can display where the ant is. 

# memory for this is O(m*n) because of the requirement to create and store the matrix
# before printing it out, but even if there were a way for us to do that, we would 
# still need to store O(b) where b is the number of black squares, which within the 
# domain we are going to print is somewhere in O(m*n) as well, though we are not sure
# without knowing more about the pattern how much this is. 

def f1(k):

    black_tiles = set()
    i_bounds, j_bounds = [0,0], [0,0]
    
    i,j = 0,0         # starting position
    di,dj = 1,0       # starting direction
    
    for _ in range(k):
    
        # white space
        if (i,j) not in black_tiles:
            black_tiles.add((i,j))
            di,dj = rotate_90(di,dj,1)     # rotate right
            i,j = i+di, j+dj               # step forward one space
        
        # black space
        else:
            black_tiles.remove((i,j))
            di,dj = rotate_90(di,dj,-1)    # rotate left
            i,j = i+di, j+dj               # step forward one space
    
        # update bounds for drawing
        for var,bounds in [(i,i_bounds),(j,j_bounds)]:
            if var < bounds[0]:                # min
                bounds[0] = var
            elif var > bounds[1]:              # max
                bounds[1] = var
            
    print_board(black_tiles,i_bounds,j_bounds,(i,j),(di,dj))
        
# roates di and dj right for dir=1, and left for dir=-1        
def rotate_90(di,dj,dir):

    if abs(dj) == 0:
        dj = (dj-di) * dir
        di = 0
    else:
        di = (di-dj) * dir * -1
        dj = 0
        
    return di,dj
        
# given a set of black tiles and the maximum and minimum values for where the ant
# has ever travleed, print the board. 
def print_board(black_tiles,i_bounds,j_bounds,pos,dir):

    # dimension is either the largest absolute bound we found, or 5...whichever is 
    # largest. this ensures that the printed board is a square of tiles centered 
    # around where the ant began at (0,0)
    dim = max(5,1+max(max(max(abs(i_bounds[0]),abs(i_bounds[1])),abs(j_bounds[0])),abs(j_bounds[1])))
    
    # print the top border line
    print(" ",end="")
    for _ in range(2*dim+1):
        print("_",end="")
    print("\n",end="")
        
    # print each row
    for j in range(dim,-1*dim-1,-1):
        print("│",end="")                # start row
        for i in range(-1*dim,dim+1,1):
            
            #print(i,j)
            
            if (i,j) == pos:
                
                if (i,j) in black_tiles: # black tile
                    if dir == (1,0):
                        print("▶",end="")
                    elif dir == (0,-1):
                        print("⯆",end="")
                    elif dir == (-1,0):
                        print("◀",end="")
                    else:
                        print("⯅",end="")
                else:                    # white tile
                    if dir == (1,0):
                        print("R",end="")
                    elif dir == (0,-1):
                        print("D",end="")
                    elif dir == (-1,0):
                        print("L",end="")
                    else:
                        print("U",end="")
                    
            elif (i,j) in black_tiles:
                print("█",end="")
            else:
                print(" ",end="")
        print("│",end="\n")              # end row
    
    # print the bottom border line
    print(" ",end="")
    for _ in range(2*dim+1):
        print("¯",end="")
    print("\n",end="")
    
    
    print("⇦")
    
    
    
    
    
    
    
    
    
    
    
    
    












