# My bare-bones Graph class uses a Node class, where each Node contains an 
# adjacency set of indices. "Adjacency" is only unidirectional and refers to a 
# directed edge. If Node 4 has "6" in its adjacency set, this implies an edge
# from Node 4 to Node 6 but not necessarily from Node 6 to Node 4.  

class Node:
    """Node class for implementing the Graph class.
    
    Attributes:
        data: None by default, but can also store strings, ints, etc.
        children: A set of int indices to the nodes list in a Graph.
        backpointer: None by default. Used in bidirectional search.
    """

    def __init__(self, children, data=None):
        """Inits a Node with optional data stored."""
        self.data = data
        self.children = children
        self.backpointer = None

# The N Nodes in a Graph are numbered 0 through N-1 as they are created.
        
class Graph:
    """Graph class. 
    
    Attributes:
        nodes: A list of Node instances.
    """

    def __init__(self):
        """Inits an empty Graph instance."""
        self.nodes = []
    
    def is_empty(self):
        """Returns a Boolean."""
        return len(self.nodes) == 0

    def __getitem__(self,index):
        """Returns a Node by standard Python indexing syntax."""
        return self.nodes[index]
    
    def has_node(self,index):
        """Returns True iff a node with index exists in graph."""
        return index > 0 and index < len(self.nodes)
    
    def add_node(self,children=None,data=None):
        """Creates a Node and returns its index.
        
        Args:
            children: Optional set of indices. User is responsible for
              including only indices that correspond to existing Nodes.
            data: Optional value to store at Node.
        
        Returns:
            An int.
        """        
        if children is None:
            children = set()
        self.nodes.append(Node(children,data))
        return len(self.nodes) - 1
     
    def add_unidirectional_edge(self,i1,i2):
        """Adds an edge from Node i1 to i2.
        
        Args:
            i1, i2: Ints.
            
        Raises:
            IndexError: At least one of i1 and i2 is out of range.
            ValueError: At least one of i1 and i2 is negative.
        """
        self._add_edge(i1,i2,False)
     
    def add_bidirectional_edge(self,i1,i2):
        """Adds an edge from Nodes i1 i2, and i2 to i1.
        
        Args:
            i1, i2: Ints.
        
        Raises:
            IndexError: At least one of i1 and i2 is out of range.
            ValueError: At least one of i1 and i2 is negative.
        """
        self._add_edge(i1,i2,True)
        
    def _add_edge(self,i1,i2,bi):
        """Edge-adder helper function."""
        if i1 < 0:
            raise ValueError(f"Index {i1} is negative")
        if i2 < 0:
            raise ValueError(f"Index {i2} is negative")    
        self.nodes[i1].children.add(i2)
        if bi:
            self.nodes[i2].children.add(i1)