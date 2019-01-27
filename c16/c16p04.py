import enum
from itertools import chain

# c16p4

# Tic Tac Win: Design an algorithm to figure out if someone has won a game of
# tic-tac-toe. 

##############################################################################

# I take as input an NxN matrix, and assume that the matrix is well-formed. 
# In other words, the input is an N-length list of N-length lists, and that 
# the only objects held are the strings "X", "O", and "_" for blank.

# It is possible to use enums as defined below, or to design a class for a 
# tic-tac-toe board with methods for checking individual rows and columns, 
# but for this problem I chose to handle the input simply as a list of list 
# of one-character strings.

class Square(enum.Enum):

    x = 1
    o = 2
    b = 3

# One note: It is possible to input a tic-tac-toe board that has multiple 
# winning streaks, either by X or by O or by both. This instance of a board
# would not be possible in a real game, since the game ends once there is one
# winning streak, but it is perfectly possible as an arbitrary input. We can
# either raise an exception and reject such a board upon identifying it, or 
# return True upon finding any winning streak. I chose the SECOND option.

# The following brute-force approach checks every way that the board can be
# won. For extremely large boards, algorithms such as f2 might be faster, 
# but if this function were to be used only on boards of dimensions 3 or 4
# or so, there is little to worry about as it is still in O(N^2) time, which 
# is the best conceivable runtime for the problem. O(1) space requirements.

# We assume that n is greater than 1 in this solution.
    
def f1(board):
    """Returns True if a board for tic-tac-toe has been won, and False
    otherwise.
    
    Args:
        board: an n-length list of n-length lists of "X","O",or "_".
    """          
    n = len(board) # 3 in standard board
    
    # Check each row and column one by one, and then both diagonals,
    # for a winning streak. Return True immediately upon finding one.
   
    for i in range(n):
        if check_row(board,i,n) or check_column(board,i,n):
            return True     
            
    if check_diagonals(board,n):
        return True
        
    return False

def is_blank(sym):
    """Return True if input represents a blank, and False otherwise.
    
    Args:
        sym: A string.
    """      
    return sym == "_"

def check_row(board,i,n):
    """Returns True if the ith row has been won, or False otherwise.
    
    Args:
        board: A list of lists of "X", "O", or "_".
        i: An int representing the row to check.
        n: An int representing the dimension of the board.
    """   
    sym = board[i][0]   
    if is_blank(sym): return False
    
    for j in range(1,n):
        if board[i][j] != sym or is_blank(board[i][j]):
            return False
    
    return True
    
def check_column(board,j,n):
    """Returns True if the jth column has been won, or False otherwise.
    
    Args:
        board: A list of lists of "X", "O", or "_".
        j: An int representing the column to check.
        n: An int representing the dimension of the board.
    """
    sym = board[0][j]  
    if is_blank(sym): return False
    
    for i in range(1,n):
        if board[i][j] != sym or is_blank(board[i][j]):
            return False
    
    return True
    
def check_diagonals(board,n):
    """Returns True if the either of the diagonals of a board has been
    won, or False otherwise.
    
    Args:
        board: A list of lists of "X", "O", or "_".
        n: An int representing the dimension of the board.
    """

    # If top-left to bottom-right is found to have been won, return 
    # True early. Otherwise, must check top-right to bottom-left.

    tlbr_flag = True  
    sym = board[0][0]
    if is_blank(sym): tlbr_flag = False
    
    for i in range(1,n):
        if board[i][i] != sym or is_blank(board[i][i]):
            tlbr_flag = False
    
    if tlbr_flag: return True
        
    sym = board[0][n-1]
    if is_blank(sym): return False
    
    for i in range(1,n):
        if board[i][n-1-i] != sym or is_blank(board[i][n-1-i]):
            return False
    
    return True

# But the above approach requires more checks of individual squares than is 
# necessary, though. The below approach visits each square only once and then
# increments a counter for the correpsonding rows, columns, and diagonals, 
# returning True immediately upon detecting a full streak.

class Zone:
    """Contains information about a row, column, or diagonal.
    
    Attributes:
        x: An integer count of "X" symbols in the zone.
        o: An integer count of "O" symbols in the zone.
        len: An integer indicating the number of squares in the zone.
    """

    def __init__(self,n):
        """Inits Zone with 0 counts for "X" and "O"."""
        self.x = 0
        self.o = 0
        self.len = n
        
    def update(self,sym):
        """Increments the appropriate symbol counter."""
        if sym == "X":
            self.x += 1
        elif sym == "O":
            self.o += 1
    
    def is_won(self):
        """Returns whether or not zone is filled with one symbol."""
        return self.x == self.len or self.o == self.len

# Given that this approach requires O(N) memory to store counters for each 
# of the rows, columns, and diagonals, there is a bit of a tradeoff. In 
# addition, the "work" done at each square, which involves finding all of 
# the rows, column, and diagonals in which it belongs and updating them, is 
# greater than that done at each square in f1, so it is not immediately 
# obvious that f2 should have constant-factor improvements to runtime.
        
# Perhaps with some added optimzations, such as if the function were to keep
# track (at a greater memory cost) which zones are still "in the running" to 
# be won, and systematically "rule out" ones with blank spaces or with at 
# least one of each an X and an O, then it could improve runtime more.

# But the below function, which builds a complete picture of the board before 
# identifying whether there is a winner or not, serves to build information 
# on the zones incrementally and could serve as the model to for a function
# that identifies a win in O(1) time after each turn is completed in a real
# game as it progresses.
       
def f2(board):
    """Returns True if a board for tic-tac-toe has been won, and False
    otherwise.
    
    Args:
        board: an n-length list of n-length lists of "X","O",or "_".
    """    
    n = len(board)   
    rows = [Zone(n) for i in range(n)]
    cols = [Zone(n) for i in range(n)]
    dags = [Zone(n), Zone(n)]
    
    for i in range(n):
        for j in range(n):
            for zone in get_zones(i,j,n,rows,cols,dags):
                zone.update(board[i][j])
    
    for zone in chain(chain(rows,cols),dags):
        if zone.is_won():
            return True
    return False
    
def get_zones(i,j,n,rows,cols,dags):
    """Returns a list of Zone instances to which the square in the ith 
    row and jth column belongs.

    Args:
        i: An integer representing the row.
        j: An integer representing the column.
        n: An integer representing the dimension of the board.
        rows: A list of all Zone instances for rows.
        cols: A list of all Zone instances for columns.
        dags: A list of all Zone instances for diagonals.
    """    
    output = [rows[i]]
    output.append(cols[j])
    if i==j:
        output.append(dags[0])
    if i+j==n-1:
        output.append(dags[1])
    return output
    
def test():
    """Tests some inputs. If all correct, returns None."""   
    win1 = [["X","O","_"],
            ["X","O","_"],
            ["X","_","_"]]
        
    win2 = [["X","O","_"],
            ["_","X","_"],
            ["_","O","X"]]
        
    win3 = [["X","_","O"],
            ["_","O","_"],
            ["O","X","X"]]    
        
    yet1 = [["_","O","_"],
            ["X","O","_"],
            ["X","_","_"]]   

    yet2 = [["_","O","O"],
            ["X","O","_"],
            ["X","_","X"]] 

    for win in [win1,win2,win3]:
        assert f1(win)
        assert f2(win)
    
    for yet in [yet1,yet2]:
        assert not f1(yet)
        assert not f2(yet)