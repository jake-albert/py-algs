import sys
sys.path.append('..')
from data_structs import Graph

# start

# say that n is the length of the list and m is the length of the synonym list

# FIRST big question is....does the list need to be output in sorted order, as in 
# maintaining the ranking? The input is unranked, so does it matter how the output 
# is? I am going to assume they don't need the output to be sorted. 

# Can we accept the input in any form? Or either way, we can convert the input list
# of individual names and their frequencies into a hash table for instant lookup in 
# O(n) time. 

# NEXT, we can construct a graph with one vertex for all of the names we saw above, 
# and begin it UNCONNECTED. Then, in O(m) time for every synonym relationship we 
# see in that next list, we ADD an edge between those two vertices. 

# Then, when this is done, we keep track of "seen" and "unseen" nodes and continue 
# dfs'ing as many nodes as we can, adding the frequencies to each other. This will 
# take altogether O(n+m) time, and should work out nicely. 


def f1(freqs,syns):

    # if there are no frequency pairs, we simply return back this 
    # empty list. If there are no synonyms, then the original frequency
    # list is the correct output
    if len(freqs) == 0 or len(syns) == 0:
        return freqs
        
    # we load a graph with all vertices in freqs, and edges in syns
    # the ith vertex in the graph represents the ith name/freq pair in 
    # the input list.
    g = load_graph(freqs,syns)
    
    # output list will be the same form as input. Name/freq pairs
    output = []
    
    # we perform dfs search on every vertex that we have not yet seen
    # and determine the total sum.
    seen_verts = set()
    for i in range(len(freqs)):
        if i not in seen_verts:
            total = dfs_from_vert(0,i,g,seen_verts,freqs)
            output.append((freqs[i][0],total))
    
    return output

# load a graph with points representing unique names, and return the graph
def load_graph(freqs,syns):

    g = Graph()
    lookup = {}
    
    # add vertices to graph
    for i in range(len(freqs)):
        g.add_node()
        lookup[freqs[i][0]] = i      # ensure we can find a vertext from a name
    
    # add edges to graph
    for n1,n2 in syns:
        
        # we can ignore case where synonym given that has no freq
        # NO WE CANNOT............if the synonym is not in it then we 
        # need to add a vertex to maintain the connection!!!
        if n1 not in lookup:
            lookup[n1] = g.add_node()
        if n2 not in lookup:
            lookup[n2] = g.add_node()
        g.add_bidirectional_edge(lookup[n1],lookup[n2])
    
    return g
    
# conduct dfs from the current node, adding to a sum, and return the sum
def dfs_from_vert(sum,i,g,seen_verts,freqs):

    # first, process the current vertex by adding the appropriate freq
    # there is a chance that the vertex we are visiting has no freq, but 
    # is a "ghost" bridge between two others that are. Add the sum only 
    # if not a ghost bridge
    if i < len(freqs):
        sum += freqs[i][1]
    seen_verts.add(i)

    for child in g[i].children:
        if child not in seen_verts:
            sum += dfs_from_vert(0,child,g,seen_verts,freqs)
    
    return sum
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    