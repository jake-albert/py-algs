from random import shuffle


# c17p12

# BiNode: Consider a simple data structure called BiNode, which has pointers 
# to two other nodes.
#
# public class BiNode {
#     public BiNode node1, node2;
#     public int data;
# }
#
# The data structure BiNode could be used to represent both a binary tree 
# (where nodel is the left node and node2 is the right node) or a doubly 
# linked list (where node1 is the previous node and node2 is the next node). 
# Implement a method to convert a binary search tree (implemented with BiNode)
# into a doubly linked list. The values should be kept in order and the 
# operation should be performed in place (that is, on the original data 
# structure). 

##############################################################################

# First, I implement a little simple BiNode class with an insertion function 
# that allows us to create binary search trees.

class BiNode:
    """A BiNode class.
    
    Attributes:
        node1,node2: BiNode instances
        data: Any object that supports comparison operations.
    """
    
    def __init__(self,data,node1=None,node2=None):
        """Inits a BiNode with data."""
        self.node1 = node1
        self.node2 = node2
        self.data  = data

    def insert(self,value):
        """Treats self as root of a BST and inserts value as such."""
        self._insert_at(self,value)
    
    def _insert_at(self,node,value):
        """Inserts a leaf with value as a descendant of node."""
        if value <= node.data:
            if node.node1 is None:
                node.node1 = BiNode(value)
            else:
                self._insert_at(node.node1,value)
        else:
            if node.node2 is None:
                node.node2 = BiNode(value)
            else:
                self._insert_at(node.node2,value)
    
# My solution performs an in-order traversal of the tree, linking appropriate 
# nodes to each other at each position in O(1) time to generate the head and 
# tail nodes of the subtree with root at that position, and returns the head
# and tail. This means the function runs in O(N) time to the number of nodes 
# in the tree, and requires O(D) space in the call stack, where D is the depth
# of the tree. (No guarantee here that the input is balanced, so D may be as
# large as N in the worst case.) 
 
def f1(root):
    """Given a root of a BST implemented with BiNode instances, 
    converts the BST to a doubly-linked list with order of nodes 
    preserved and returns the head and tail of the list.
    
    Args:
        root: A BiNode instance.
    
    Returns:
        Two BiNode instances, or the tuple (None,None)
    """
    
    # The head and tail of an empty list are both defined as None. 
    
    if root is None:
        return None,None
        
    # Otherwise, we perform an in-order traversal. The head of the 
    # list created from the left subtree becomes the head of the full 
    # list, and the tail of the list created from the right subtree 
    # becomes the tail. When a subtree is empty, the root node becomes 
    # the end node.
    
    head_1, tail_1 = f1(root.node1)
    if tail_1 is not None:
        concat(tail_1,root)
    
    head_2, tail_2 = f1(root.node2)
    if head_2 is not None:
        concat(root,head_2)    
    
    return root if head_1 is None else head_1, \
           root if tail_2 is None else tail_2
  
def concat(x,y):
    """Given two BiNode instances representing the tail of a first 
    linked list the head of a second one, concatenates the second to 
    the end of the first."""
    x.node2 = y
    y.node1 = x      
        
# It seems that a large part of the challenge in this problem comes when the 
# programming language does not permit functions to return multiple objects, 
# as Python does with both the head and tail nodes. An interesting workaround 
# to this situation suggested in the book is to temporarily link the head 
# and tail directly, making the linked list circular, so that on every 
# return from a recursive call the tail can be accessed from the head and 
# unlinked in O(1) time.
        
def test(trials,node_num):
    """Tests f1 for correctness.
    
    In each trial, randomly creates a BiNode binary search tree with 
    node_num distinct values and checks that f1 has correctly converted
    it to a doubly-linked list while maintaining the nodes' order.
    
    Different insertion orders lead to different tree structures, but 
    if f1 correctly maintains the order of the nodes, then the output
    linked list must always be in increasing order.
    
    Args:
        trials: A non-negative int. Number of inputs to test.
        node_num: A non-negative int. 
        
    Raises:
        AssertionError: f1 has failed to create the expected list.
    """
    insert_order = list(range(node_num))
    
    for trial in range(trials):
    
        shuffle(insert_order)
        root = BiNode(insert_order[0])
        for item in insert_order[1:]:
            root.insert(item)
        
        head,tail = f1(root)
        
        check_order(head,True,node_num)
        check_order(tail,False,node_num)
    
def check_order(end,forward,node_num):
    """Given a node that represents one end of a linked list, checks
    that the nodes from that end to the other are in order.
    
    Elements in the list are expected to be every integer in the range
    from 0 to node_num - 1 inclusive, in increasing order from head to
    tail.   
    
    Args:
        end: A BiNode instance.
        forward: A Boolean. If True, end is the head and the forward 
          direction must be checked, and False end is the tail.
        node_num: An int. Expected number of nodes in the list.
    """
    correct_order = range(node_num) if forward else reversed(range(node_num))
    
    # Check not only that elements are in order, but that the list ends
    # where we expect it to -- after exactly node_num nodes.
    
    for item in correct_order:
        assert item == end.data
        try:
            end = end.node2 if forward else end.node1
        except AttributeError:
            if forward:
                assert end.node2 is None
            else:
                assert end.node1 is None  