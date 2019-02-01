import sys
sys.path.append('..')
from data_structs import Stack, DequeQueue, Graph

# My BFS and DFS test functions arbitrarily set the 0th-indexed node as the
# "root" from which to begin searching. If the graph is not connected, then 
# this search function will not print any nodes unconnected to that node.

# In both search implementations, I maintain a separate set of nodes that have
# been visited. As an alternative, I could have added a "seen" attribute to 
# the Node class, but would need to reset this attribute after every search is 
# performed.

def dfs(graph):
    """Performs depth-first search from the node indexed at 0. At each 
    visited node, prints whatever value is stored there.
    
    Args:
        graph: A Graph instance.
    """
    ROOT_INDEX = 0
    
    if graph.is_empty():
        return
    
    # This implementation hashes the memory ids of Node instances 
    # rather than their indices. Might revisit and test later to 
    # see whether one approach is faster than the other.
    
    def dfs_from_node(node):
        if node not in seen_nodes:
            print(node.data)
            seen_nodes.add(node)
            for child_index in node.children:
                dfs_from_node(graph[child_index])
    
    seen_nodes = set()
    dfs_from_node(graph[ROOT_INDEX])

def bfs(graph):
    """Performs breadth-first search from the node indexed at 0. At 
    each visited node, prints whatever value is stored there.
    
    Args:
        graph: A Graph instance.
    """
    ROOT_INDEX = 0
    
    if graph.is_empty():
        return
    
    seen_nodes = set() 
    
    # This approach uses a queue of node indices.
    
    search_queue = DequeQueue()
    search_queue.add(ROOT_INDEX)
    
    while not search_queue.is_empty():
        cur_node = graph[search_queue.remove()]
        if cur_node not in seen_nodes:
            print(cur_node.data)
            seen_nodes.add(cur_node)
            for child_index in cur_node.children:
                search_queue.add(child_index)
                
# To test the Graph class, as well as to demonstrate how DFS and BFS visit 
# nodes in a different order, I defined the graph from page 107 of CCI6. Below
# is my (very) crude Unicode drawing of the graph.

#            0 ----→ 1 ←---- 2               
#            | \     | \     ↑     
#            |   \   |   \   |      
#            ↓     ↘ ↓     ↘ |     
#            5       4 ←---- 3

graph_a = Graph()
graph_a.add_node(set([1,4,5]),"0")  # node 0
graph_a.add_node(set([3,4]),"1")    # node 1
graph_a.add_node(set([1]),"2")      # node 2
graph_a.add_node(set([2,4]),"3")    # node 3
graph_a.add_node(set(),"4")         # node 4
graph_a.add_node(set(),"5")         # node 5
              
def test_a():
    
    print("Performing depth-first search from node 0.")
    dfs(graph_a)
    
    print("Performing breadth-first search from node 0.")
    bfs(graph_a)
              
# Finding the shortest path between two nodes in an undirected graph involves
# bidirectional search: BFS performed from each node. To ensure we return the 
# shortest path possible, I created a "searcher" class that simulates a BFS 
# process beginning at one node, and enforce that the two searcher instances
# searching from each node take turns searching one "step" through the graph.

# In one "step", a searcher takes a group of nodes (on the first step, this 
# group of nodes consists only of the origin node for that searcher) and 
# identifies, for all nodes that are adjacent to the nodes in the group, any
# nodes that it has not yet visited. If any of these nodes have been visited 
# by the OTHER searcher, then a path has been found. Otherwise, these nodes, 
# as well as backpointer indices that indicate where the searcher came to 
# visit them from, are added to a queue as the next group. 

# I developed some helper classes to simplify the approach.

class QueueItem:
    """Objects added and removed from the BFS search queues. Each 
    QueueItem is either substantive, containing indices to nodes that
    are part of the search, or empty, in which it serves as a divider
    between groups of nodes that are to be searched in one step.
    
    Attributes:
        ind: An int index to a node to search, or None.
        bp: An int backpointer index indicating the node where a 
          searcher was when it added node "ind" to the queue, or None.
    """
    
    def __init__(self,index,bp):
        """Inits a QueueItem."""
        self.ind = index
        self.bp = bp

    def is_blank(self):
        """Returns a Boolean."""
        return self.ind is None and self.bp is None
        
class BlankItem(QueueItem):
    """Divider QueueItem between groups of nodes."""
    
    def __init__(self):
        """Inits a BlankItem."""
        super(BlankItem,self).__init__(None,None)
        
class Searcher:
    """Simulates a BFS process originating from a specific node.
    
    Attributes:
        origin: An int index to the node where BFS started.
        seen_indices: A set of int indices of nodes the searcher has 
          already visited.
        backtracer:
        search_queue: A DequeQueue instance.
    """
    
    def __init__(self,i):
        """Inits a Searcher instance whose next "step" begins at the 
        origin node of index i."""
        self.origin = i
        self.seen_indices = set()
        self.backtracer = None
    
        self.search_queue = DequeQueue()
        self.add_node(i,None)  # Origin has no backpointer.
        self.add_divider()
        
    def is_exhausted(self):
        """Returns True if there are no more nodes to search."""
        return self.search_queue.is_empty()
        
    def add_node(self,ind,bp):
        """Adds a new node's index and backpointer to queue."""
        self.search_queue.add(QueueItem(ind,bp))
        
    def add_divider(self):
        """Adds a divider item to queue, marking end of one step."""
        self.search_queue.add(BlankItem())
    
def bidirectional_search(graph,si,ti,verbose=False):
    """Finds the shortest path between two nodes in an undirected 
    graph, or determines that no such path exists.
    
    Args:
        graph: A Graph instance. Assumed all edges are bidirectional.
        si, ti: Int indices to nodes in graph.
        verbose: A Boolean. If True, prints path information. 
    
    Returns:
        A list of indices on the shortest path from si to ti, or an 
        empty list if no such path exists.
    
    Raises:
        IndexError: At least one of si and ti is out of range.
        ValueError: At least one of si and ti is negative.
    """
    if max(si,ti) > len(graph.nodes):
        raise IndexError("Out of range index or indices.")
    if min(si,ti) < 0:
        raise ValueError("Negative index or indices.")
        
    from_s, from_t = Searcher(si), Searcher(ti)
    
    # Alternate between the searcher from s and the searcher from t.
    
    while True:                   
        res = take_step(graph,from_s,from_t)
        if res is not None:
            break
        res = take_step(graph,from_t,from_s)
        if res is not None:
            break
        
    if res:
        path = get_path(graph,from_s,from_t)
        for index in path:
            graph[index].backpointer = None
            if verbose: print(f"{index} -> ",end="")
        if verbose: print("done") 
        return path
    
    else:
        if verbose: print("No path exists.")
        return []
    
    
def take_step(graph,from_x,from_y):
    """Takes one step with searcher from_x and returns result.
    
    Args:
        graph: A Graph instance.
        from_x: The Searcher instance to take a step.
        from_y: The Searcher instance from_x references. 
        
    Returns:
        None if search should not yet halt. If search should halt, 
        returns a Boolean indicating whether or not a path was found.
    """
    if step_and_found_connection(graph,from_x,from_y):
        return True
    if from_x.is_exhausted():  # True if BFS completed without connect.
        return False
    return None
        
def step_and_found_connection(graph,focus,other):
    """Given a Searcher instance with a group of nodes search next, 
    for each node in that group, search every unseen node a distance 
    of one edge away, halting early if one such node is determined to
    have already been found by the other Searcher instance. 
    
    Args:
        focus: A Searcher instance. The searcher currently searching.
        other: A Searcher instance. The searcher that focus might 
          connect with.
          
    Returns:
        A Boolean. True iff a connection has been made on the step. 
    """
    while True:
    
        # Continue taking QueueItems off of the queue until a blank 
        # divider is found, indicating the end of the step.
    
        cur = focus.search_queue.remove()
        if cur.is_blank():  
            return False
            
        if cur.ind not in focus.seen_indices: 
            
            if cur.ind in other.seen_indices:
                focus.backtracer = cur.bp
                other.backtracer = cur.ind
                return True
                            
            else:
                cur_node = graph[cur.ind]
                cur_node.backpointer = cur.bp
                focus.seen_indices.add(cur.ind)
                
                for child_index in cur_node.children:
                    focus.add_node(child_index,cur.ind)
                focus.add_divider()
    
def get_path(graph,from_s,from_t):
    
    # otherwise, must construct the path
    start_stack = Stack()
    
    # first, add the path back to s to a stack
    while from_s.backtracer is not None:
        start_stack.push(from_s.backtracer)
        from_s.backtracer = graph[from_s.backtracer].backpointer
    
    # create a queue for the final output
    path = []
    
    # and now add items from the stack onto the queue
    # now in forward order
    while not start_stack.is_empty():
        path.append(start_stack.pop())
   
    # finally, add the path onwards to t to the queue
    while from_t.backtracer is not None and from_t.backtracer != from_t.origin:
        path.append(from_t.backtracer)
        from_t.backtracer = graph[from_t.backtracer].backpointer
    path.append(from_t.origin)   
  
    return path
   
# Below I define the undirected graph from page 109 in CCI6, with the node 
# labeled "s" at index 0, and "t" at index 46. There is also a photo of my 
# drawing of the graph in this directory, at "graph_sample.jpg". There are 61 
# total nodes, with the node at 60 (not drawn) unconnected to all the others. 

graph_b = Graph()
for i in range(61):
    graph_b.add_node(set(),str(i))
               
connections = [[0, 1], [1, 9], [9, 22], [9, 23], [22, 39], [23, 40], \
               [1, 10], [10, 24], [24, 41], [24, 42], [0, 2],        \
               [2, 11], [2, 12], [11, 25], [25, 43], [12, 26],       \
               [12, 27], [26, 44], [26, 45], [0, 3], [3, 13],        \
               [13, 28], [28, 46], [0, 4], [4, 14], [4, 15],         \
               [14, 29], [29, 47], [15, 30], [15, 31], [30, 48],     \
               [31, 49], [31, 50], [0, 5], [5, 16], [16, 32],        \
               [32, 51], [0, 6], [6, 17], [6, 18], [17, 33],         \
               [18, 33], [18, 34], [33, 52], [33, 53], [34, 54],     \
               [34, 55], [0, 7], [7, 19], [7, 20], [19, 35],         \
               [20, 36], [35, 56], [36, 57], [0, 8], [8, 21],        \
               [21, 37], [21, 38], [37, 58], [38, 59]]
               
for pair in connections:
    graph_b.add_bidirectional_edge(pair[0],pair[1])
    
def test_b():

    inputs = [(32,32),  # 32
              ( 0,16),  # 0 -> 5 -> 16
              (14, 4),  # 14 -> 4
              ( 0,46),  # 0 -> 3 -> 13 -> 28 -> 46
              (45,27),  # 45 -> 26 -> 12 -> 27
              (55,52),  # 55 -> 34 -> 18 -> 33 -> 52
              (59,49),  # 59 -> 38 -> 21 -> 8 -> 0 -> 4 -> 15 -> 31 -> 49
              (17,60)]  # No path exists.
              
    for start, end in inputs:
        print(f"Shortest path from {start} to {end}:", end="\n    ")  
        bidirectional_search(graph_b,start,end,True)