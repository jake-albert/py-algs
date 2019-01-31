from itertools import chain
from operator import lt, gt

# c16p22

# Langton's Ant: An ant is sitting on an infinite grid of white and black 
# squares. It initially faces right. At each step, it does the following:
#
# (1) At a white square, flip the color of the square, turn 90 degrees right 
# (clockwise), and move forward one unit.
# (2) At a black square, flip the color of the square, turn 90 degrees left 
# (counter-clockwise), and move forward one unit.
#
# Write a program to simulate the first K moves that the ant makes and print
# the final board as a grid. Note that you are not provided with the data 
# structure to represent the grid. This is something you must design yourself.
# The only input to your method is K. You should print the final grid and 
# return nothing. The method signature might be something like void 
# printKMoves (int K). 

##############################################################################

# The problem describes the ant as sitting on a "grid of white and black 
# squares", but does not specify an initial color pattern for the grid. Since
# the function I write takes only K as input, I need to determine a reading
# of the problem description so that the initial state of the grid can be the 
# same every time I call the function.

# If the board begins as an alternating checkerboard of white and black
# squares, which is one plausible reading the of the problem description, then
# regardless of the square the ant starts on, its movement is repetitive and
# not too exciting. It immediately begins a simple cycle that travels 
# diagonally, flipping all of the squares it touches and never doubling back.

#  _______________________                       _______________________
# │█ █ █ █ █ █ █ █ █ █ █ █│                     │█ █ █ █ █ █ █ █ █ █ █ █│
# │ █ █ █ █ █ █ █ █ █ █ █ │                     │ █ █ █ █ █ █ █ █ █ █ █ │
# │█ █ █ █ █ █ █ █ █ █ █ █│                     │█ █ █ █ █ █ █ █ █ █ █ █│
# │ █ █ █ █ █ █ █ █ █ █ █ │        ==\          │ █ █ █ █ ███ █ █ █ █ █ │
# │█ █ █ █ █ █ █ █ █ █ █ █│        ==/          │█ █ █ █ █  ██ █ █ █ █ █│
# │ █ █ █ █ █ █ █ █ █ █ █ │                     │ █ █ █ █ █  ██ █ █ █ █ │
# │█ █ █ █ █ █ █ █ █ █ █ █│                     │█ █ █ █ █ █  ██ █ █ █ █│
# │ █ █ █ █ █ █ █ █ █ █ █ │                     │ █ █ █ █ █ █  ██ █ █ █ │
# │█ █ █ █ █ █ █ █ █ █ █ █│                     │█ █ █ █ █ █ █  ██ █ █ █│
#  ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯                       ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯

# On the other hand, if all of the squares are WHITE at the start, the ant
# seems to have far more interesting behavior, so I am assuming that the 
# intention of the problem is to simulate an ant on this type of grid. (As it
# turns out, this makes for simpler simulation of the grid because of the data
# structure I chose to use for the problem.)

# Rather than maintian a matrix, whose boundaries I would need to expand
# whenever the ant steps beyond its initial size, I chose to maintain a SET of
# squares that are black. This means that, with my above assumption about the 
# initial state of the grid, I can initialize the board as an empty set. 

# In O(1) time, we can ADD to this set when a white square becomes black, 
# REMOVE from the set when a black square turns white, and check color of a 
# square by checking for set membership in O(1). This means that with each of 
# the K steps of the ant, we can update its position and the state of the grid 
# in a constant number of operations. So can update the grid in O(K) time, and 
# end with a set of at most K spaces that remain black after all the flips.  

# As for printing the board, I chose to keep track of the farthest up, down, 
# right, and left that the ant has traveled, find the maximum of these values, 
# double it, add one for padding to create a value D, and then draw a square 
# cenetered at (0,0) with side length D. We can then either build and then 
# join a list of characters to form a string to print, or write a function 
# that without storing a full string to represent the output, prints each 
# character in the grid top-left to bottom-right. Either way, this should take
# O(D^2) time.

# Total memory constraints depend partly on whether we want to build up (and 
# thus store) the O(D^2) characters for the grid, or print each character 
# immediately. In the second option, we are either writing to the terminal in 
# interactive mode, or perhaps writing to an external file or redirecting
# output elsewhere, so there is no O(D^2) storage overhead on the process 
# running the function. I chose this second option, but there are drawbacks;
# for example, if the program terminates unexpectedly before finishing the 
# drawing task, then the output, whether on the terminal or in some file, will
# be an incomplete drawing rather than a lack of any drawing at all, so it 
# would be important to check that the process running this program exited 
# correctly before "trusting" the drawing. 

# Regardless, this function still requires O(B) space, where B is the number 
# of black squares stored in the set, and we also know that B cannot be
# greater than K so this is O(K) space.  

# For fun, I also found some Unicode characters to display the ant's position 
# and direction on each color tile. 
        
class Ant:
    """A representation of an ant's current position and direction.
    
    Atrributes:
        x: An int. The ant's x-axis position.
        y: An int. The ant's y-axis position.
        dx: An int. 1 when ant faces right, -1 when left, 0 otherwise.
        dy: An int. 1 when ant faces up, -1 when down, 0 otherwise.
    """
    
    def __init__(self):
        """Inits Ant instance facing right on origin point."""
        self.x = 0
        self.y = 0
        self.dx = 1
        self.dy = 0
    
    def facing_right(self):
        return self.dx == 1 and self.dy == 0
    
    def facing_down(self):
        return self.dx == 0 and self.dy == -1
    
    def facing_left(self):
        return self.dx == -1 and self.dy == 0
    
    def facing_up(self):
        return self.dx == 0 and self.dy == 1
    
    def facing_horizontal(self):
        return self.dx != 0 and self.dy == 0
    
    def facing_vertical(self):
        return self.dx == 0 and self.dy != 0
    
    def get_position(self):
        """Returns a hashable tuple of the ant's position."""
        return (self.x,self.y)    
    
    def rotate_right(self):
        self._rotate_90(True)
    
    def rotate_left(self):
        self._rotate_90(False)
        
    def _rotate_90(self,right):
        """Changes dx,dy such that ant has turned 90 degrees.
        
        Args:
            right: A Boolean. If False, interpreted as left turn.
        """
        dir = 1 if right else -1
        if abs(self.dy) == 0:  # True when ant is facing right or left.
            self.dy = (self.dy-self.dx) * dir
            self.dx = 0
        else:                  # True when ant is facing up or down.
            self.dx = (self.dx-self.dy) * dir * -1
            self.dy = 0
        
    def step_forward_one(self):
        """Changes x,y according to dx,dy to simulate ant's step."""
        self.x += self.dx
        self.y += self.dy

class Grid:
    """
    Attributes:
        SIDE_BORDER, BOTTOM_BORDER, etc.: Strings of length 1 
          (characters) for drawing borders, tiles, and the ant in 
          all directions. Treated as Class-wide, Class-specific 
          constants and thus are Class attributes.
        black_tiles: A set of tuples representing black tile locations.
        ant: An Ant instance.
        x_bounds, y_bounds: Lists of the most left and right, and of
          the most down and up, that the ant has traveled.       
    """
    SIDE_BORDER = "│"  # NOT the pipe symbol. 
    BOTTOM_BORDER = "¯"
    TOP_BORDER = "_"
    
    BLACK_SPACE = "█"
    WHITE_SPACE = " "
    EMPTY_CHAR = " "
    
    RIGHT_ON_BLACK = "▶"
    DOWN_ON_BLACK = "⯆"
    LEFT_ON_BLACK = "◀"
    UP_ON_BLACK = "⯅"

    RIGHT_ON_WHITE = "R"
    DOWN_ON_WHITE = "D"
    LEFT_ON_WHITE = "L"
    UP_ON_WHITE = "U"
    
    def __init__(self):
        """Inits a Grid instance with no black tiles ."""
        self.black_tiles = set()
        self.ant = Ant()
        self.x_bounds = [0,0]
        self.y_bounds = [0,0]
    
    def one_langton_step(self):
        """Simulates one step of the Langton's Ant's behavior."""
        pos = self.ant.get_position()        
       
        # Ant must flip tile color and step forward in both cases, so 
        # determine tile color and rotate ant first. 
       
        if self._tile_is_black(pos):
            self.ant.rotate_left()            
        else:
            self.ant.rotate_right()
        self._flip_tile(pos)
        self.ant.step_forward_one()
        self._update_bounds()
    
    def _tile_is_black(self,pos):
        """Returns a Boolean."""
        return pos in self.black_tiles
    
    def _flip_tile(self,pos):
        """Adds or remove the tuple pos to indicate change in color."""
        if pos in self.black_tiles:
            self.black_tiles.remove(pos)
        else:
            self.black_tiles.add(pos)
    
    def _update_bounds(self):
        """Determines if the the ant is the farthest has traveled in
        any direction. Asumes that the ant has not rotated since last
        taking a step.
        """
        if self.ant.facing_horizontal():
            self._update_bound(self.ant.dx,self.ant.x,self.x_bounds)
        else:
            self._update_bound(self.ant.dy,self.ant.y,self.y_bounds)
    
    def _update_bound(self,dir,coord,bounds):
        """Checks whether the ant has moved beyond its farthest 
        traveled point along one dimension. Assumes that the ant has 
        not rotated since last taking a step.
        """
        ind, cmp = (0,lt) if dir < 0 else (1,gt)
        if cmp(coord, bounds[ind]):
            bounds[ind] = coord
            
    def display(self):
        """Prints an image of the grid and ant."""

        # Determine dim to be the largest of A) 1+ the largest bound 
        # found, or B) 5, and print all spaces from -dim to dim on both
        # the x an y-axis. This ensures that the printed board is a 
        # padded square centered around the ant's start at (0,0).
        
        dim = max(5,1+max(map(abs,chain(self.x_bounds,self.y_bounds))))
        self._print_top_border(dim)
        for y in range(dim,-1*dim-1,-1):  # Print rows from top to bottom.
            self._print_row(dim,y)        
        self._print_bottom_border(dim)
    
    def _print_top_border(self,dim):
        self._print_border(dim,self.TOP_BORDER)
    
    def _print_bottom_border(self,dim):
        self._print_border(dim,self.BOTTOM_BORDER)
   
    def _print_border(self,dim,c):
        """Prints a line representing a horizontal border."""
        print(self.EMPTY_CHAR,end="")
        for _ in range(2*dim+2):
            print(c,end="")
        print("\n",end="")
    
    def _print_row(self,dim,j):
        """Prints a line for the jth row from the top (+dim)."""
        print(self.SIDE_BORDER,end="")
        for i in range(-1*dim,dim+1,1):
            if (i,j) == self.ant.get_position():
                self._print_ant_space(self._tile_is_black((i,j)))
            elif self._tile_is_black((i,j)):
                print(self.BLACK_SPACE,end="")
            else:
                print(self.WHITE_SPACE,end="")
        print(self.SIDE_BORDER,end="\n")              
        
    def _print_ant_space(self,on_black):
        """Prints a space with the ant on it, showing its direction."""
        if on_black: 
            if self.ant.facing_right():
                print(self.RIGHT_ON_BLACK,end="")
            elif self.ant.facing_down():
                print(self.DOWN_ON_BLACK,end="")
            elif self.ant.facing_left():
                print(self.LEFT_ON_BLACK,end="")
            else:
                print(self.UP_ON_BLACK,end="")
        else:                    
            if self.ant.facing_right():
                print(self.RIGHT_ON_WHITE,end="")
            elif self.ant.facing_down():
                print(self.DOWN_ON_WHITE,end="")
            elif self.ant.facing_left():
                print(self.LEFT_ON_WHITE,end="")
            else:
                print(self.UP_ON_WHITE,end="")                    
    
def f1(k):
    """Given non-negative integer k, simulates a Langton's ant taking k
    steps and then prints the resulting grid.
    
    Raises:
        ValueError: k is negative.
    """
    if k < 0:
        raise ValueError("Invalid input: k must be non-negative.")
    
    grid = Grid()
    for _ in range(k):
        grid.one_langton_step()
    grid.display()