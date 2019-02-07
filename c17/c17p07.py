import sys
sys.path.append('..')
from data_structs import Graph

# c17p07

# Baby Names: Each year, the government releases a list of the 10000 most 
# common baby names and their frequencies (the number of babies with that 
# name). The only problem with this is that some names have multiple 
# spellings. For example, "John" and "Jon" are essentially the same name but
# would be listed separately in the list. Given two lists, one of 
# names/frequencies and the other of pairs of equivalent names, write an
# algorithm to print a new list of the true frequency of each name. Note that
# if John and Jon are synonyms, and Jon and Johnny are synonyms, then John and
# Johnny are synonyms. (It is both transitive and symmetric.) In the final 
# list, any name can be used as the "real" name.
#
# EXAMPLE
#
# Input:
# Names: John (15), Jon (12), Chris (13), Kris (4), Christopher (19)
# Synonyms: (Jon, John), (John, Johnny), (Chris, Kris), (Chris, Christopher)
# Output: John (27), Kris (36) 

##############################################################################

# Say that N is the length of the list of names and M is the length of the
# list of synonyms.

# The first question to ask is whether the list needs to be output in any
# particular order, such as a sorted order by frequency. The input does not 
# appear to be sorted either by frequency or alphabetically, so I am going to
# assume that the output list can be in any order. 

# I begin by converting the input list of individual names and their
# frequencies into a hash table using O(N) space and O(N) time. I then build a
# graph with one node storing the frequency of each name, and add in O(M) time
# a bidirectional edge for every synonym relationship, such as between the 
# "John" vertex and the "Jon" vertex. 

# Once this is done, the graph will be made up of some set of smaller, 
# unconnected graphs, each representing groups of names that are all mutually
# synonymous. By tracking visited nodes and repeatedly performing depth-first
# search on all unvisited nodes (adding the frequencies of all the connected 
# nodes together for each call), we can determine the "true" frequencies in 
# O(M+N) time using O(M+N) space.

def f1(freqs,syns):
    """Returns a list of "true" frequencies of names.
    
    Args:
        freqs: A list of tuples. The first item in the tuple is a
          string representing a name ("Kris"), and the second item is 
          assumed to be a non-negative integer representing that name's 
          frequency.
        syns: A list of tuples of strings representing names that are 
          synonyms to each other.
          
    Returns:
        A list of tuples of identical format to freqs.
    """
    
    # If there are no frequency pairs, we simply return the empty list.  
    # If there are no synonyms, then the original frequency list is the
    # correct output.
    
    if len(freqs) == 0 or len(syns) == 0:
        return freqs
        
    g = load_graph(freqs,syns) 
    output = []
    visited = set()

    # The name used as the label for final groups is whichever name
    # appeared earliest in the input for that group.
    
    for i, (name,_) in enumerate(freqs):
        if i not in visited:
            output.append((name,total_in_group(g,i,0,visited)))   
    
    return output

def load_graph(freqs,syns):
    """Loads a graph with nodes representing unique names and edges 
    connecting synonymous names, and return the graph.
    
    Args:
        freqs: A list of tuples.
        syns: A list of tuples.
    
    Returns: 
        A Graph instance.
    """
    g = Graph()
    lookup = {}
    
    for name, freq in freqs:
        lookup[name] = g.add_node(children=None,data=freq)
     
    # When adding edges between synonymous names, is is possible for  
    # a name to appear that is not in the frequencies list. Add a new
    # node with a data value of 0 so that the sum will work properly 
    # over the full group of names connected to that name.
     
    for n1,n2 in syns:
    
        if n1 not in lookup:
            lookup[n1] = g.add_node(children=None,data=0)
        if n2 not in lookup:
            lookup[n2] = g.add_node(children=None,data=0)
        g.add_bidirectional_edge(lookup[n1],lookup[n2])
    
    return g
    
def total_in_group(g,i,sum,visited):
    """Performs depth-first search beginning at node i of a graph, 
    summing the frequencies of all connected nodes. 
    
    Args:
        g: A Graph instance.
        i: An int index. Assumed to correspond to an existing node. 
        sum: An int. Running sum of frequencies in nodes from this 
          group of connected nodes that have already been visited.
        visited: A set of int indices.
    """
    sum += g[i].data
    visited.add(i)

    for child in g[i].children:
        if child not in visited:
            sum = total_in_group(g,child,sum,visited)
    
    return sum
    
def test():
    """Tests some examples."""
    
    # Example from problem descripton.
    
    freqs_a = [("John"       , 15),
               ("Jon"        , 12),
               ("Chris"      , 13),
               ("Kris"       ,  4),
               ("Christopher", 19)]
    
    syns_a = [("Jon","John"),
             ("John","Johnny"),
             ("Chris","Kris"),
             ("Chris","Christopher")]
            
    print(f1(freqs_a,syns_a))
    
    # Large number of synonyms for names without frequencies.
    
    freqs_b = [("Richard"    , 10),
               ("Dick"       ,  2)]
    
    syns_b = [("Richard","Ricky"),
              ("Ricky","Ricardo"),
              ("Rich","Richard"),
              ("Rich","Dick"),
              ("Sebastian","Sebi")]
    
    print(f1(freqs_b,syns_b))        