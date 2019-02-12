import sys
sys.path.append('..')
from data_structs import Graph
from other_practice import bfs, bidirectional_search
from nltk.corpus import words

# c17p22

# Word Transformer: Given two words of equal length that are in a dictionary,
# write a method to transform one word into another word by changing only one 
# letter at a time. The new word you get in each step must be in the 
# dictionary.
#
# EXAMPLE
# Input: DAMP, LIKE
# Output DAMP -> LAMP -> LIMP -> LIME -> LIKE 

##############################################################################

# NOTE: Importing this file as a module requires that NLTK be installed
# (https://www.nltk.org/install.html). To install the Unix words corpus, 
# use the nltk.download() command in interactive mode and select "words".

# I assume for this problem that words consist only of the 26 letters in the 
# English alphabet (not caps sensitive). I will call the first word in the 
# input the "start word" and the second word the "goal word".

# It will probably be most efficient to load all of the words from the 
# dictionary into some data structure like a graph that allows for fast 
# searching. But first, to get a clearer idea of how this problem works, I am
# going to think about how to solve using only the dictionary of strings.

# The most straightforward brute force solution involves a "depth first 
# search" of the space of possible words. Say that the start word has k
# characters. For each position i in the word, and for each character c in the
# alphabet that is different from the ith character (here, there are 25), we 
# replace the ith letter with c and check whether or not the resultant word is
# in the dictionary. If it is, we recursively restart the search on the new
# word until we have found the goal word. 

# We should use some kind of memo to keep track of words that we have already
# searched. (Ex. When we create LAMP from DAMP and begin to search from LAMP,
# we should know that DAMP has already been created or else we could end up 
# in an infinite loop.)

# We can improve on the above approach by implementing a bidirectional search 
# over the word space. If we maintain a set of all words that we have reached 
# from the start word, and a separate set of words reached from the goal word,  
# then on each "turn" we find ALL words that are one letter swap away "deeper"
# into the search space from each end and compare to find a collision. 

# At this point, we have a good idea of how words can be loaded into a graph:
# each node will represent a word, and edges will connect two nodes iff the
# words those nodes represent are one "letter swap" distance from each other.
# For example, DAMP is connected to both LAMP and DUMP but not to LUMP. This 
# work allows us to find connected nodes in O(1) time by accessing an
# adjacency list, as opposed to constructing a new string for all 25*L 
# possible "sibling" words that a word can have and checking for membership in
# the dictionary in O(L) time (where L is the length of the word). 

# To review why bidirectional search is superior to BFS from only one end in 
# a graph: We assume that nodes in a graph can have at most E edges (for this 
# problem, at most 25*L edges), and that the shortest path between two
# connected nodes is P. With normal BFS we search a total of O(E^P) nodes,
# since we go outwards one "depth unit" on each step. But when we search 
# simultaneously from both ends, we go outwards only half of that distance P 
# in each direction, so we search only O(E^(P/2)) nodes, which is equivalent 
# to O(sqrt(E^P)) nodes, a function that grows significantly more slowly.

# What is the best way to process the dictionary words and insert them into
# the graph? We know that we must for each word A) create a node for that word
# and B) create an edge between the node and the nodes of all words that can 
# be formed by changing one letter in that word. One way to do this is to
# check every already existing node, which would take O(N*L) time, where N is
# the number of nodes in the list and L the length of the word. (This is 
# because we can read both the new word and each other word character by 
# character to check that only one character is different.) This makes loading 
# the whole graph take in O(L*N^2) time for a dictionary of N words.
 
# Another approach other involves finding every transformation of a new word 
# by one letter, and checking to see if this other word is in the graph. This 
# approach is independent of the number of nodes in the graph, and takes 
# O(L^2) time. (This is because for each of the L positions in the word, we 
# try a constant number of new characters, and reading this to check for 
# membership in some hash set takes O(L) time.) So a full load takes O(N*L^2),
# which is an improvement on the above approach given that L is expected to be
# quite small on English language inputs.

# My class below uses O(N*L^2) more memory in order to store an extra
# "wildcard" dictionary that allows us to avoid finding all one-character 
# transformations of a new word. The dictionary maps a wildcard string, which
# is a string of all valid characters except for one wildcard symbol "_", to 
# all of the words that match it. For example, "B_LL" should map to "BALL",
# "BELL", "BILL", and "BULL" if those words are in the graph.
 
# When we add a new word, then, we can convert it to its L wildcard strings 
# and then look up in the wildcard dictionary all words that are a transform 
# distance of 1 from the word. Worst-case runtime is still in O(L^2) but we 
# should expect constant-factor improvements over trying to replace every 
# character in a word with every other character.

class WordTransformer:
    """Stores words from a dictionary such that word transformations 
    can be computed efficiently.

    Assumes that words are made only of the 26 English letters. All 
    characters are converted to upper-case before storing. 
    
    Attributes:
        g: A Graph instance. Each node represents a unique word, and 
          each edge connects two words that are different by one letter
          change.
        word_to_node: A dictionary that maps a string representing a
          word to the index at which that word's node is found in g.
        wildcards: A dictionary that maps a string representing a word 
          with one letter missing to int indices of all nodes that
          match that string. For example, the wildcard string "DO_S"
          matches whichever nodes of "DOGS","DOTS" etc. are in g.
    """
    W_CHAR = "_"  # Wildcard char. Cannot be a possible word character.

    def __init__(self,words=None):
        """Inits an empty WordTransformer. If words is an iterator of 
        strings, loads these strings into the WordTransformer."""
        self.word_to_node = {}      
        self.wildcards = {}         
        self.g = Graph()            
        
        if words is None:
            return
         
        for i,word in enumerate(words):

            nth = i+1
            if nth % (max(1,len(words)//100)) == 0:
                    p = 100*nth/len(words)
                    print(f"Adding word #{nth} ({p:.0f}%): '{word}'")
            
            self.add_word(word) 
    
    def add_word(self,word):
        """Converts word to all-caps and adds to WordTransformer."""
        self._add_word(word.upper())
    
    def _add_word(self,word): 
        """Connects a word to the WordTransformer's graph."""
        if word in self.word_to_node:
            return
        
        word_index = self.g.add_node(data=word)
        self.word_to_node[word] = word_index
        for wildcard in self._get_wildcards(word):
            self._process_wildcard(wildcard,word_index)
    
    def _get_wildcards(self,word):
        """Yields every wildcard string derivable from a word.
        
        For instance, if word is "TANK" then yields "_ANK", "T_NK", 
        "TA_K", and "TAN_".
        """
        word_list = list(word)
        for i in range(len(word_list)):
            c, word_list[i] = word_list[i], self.W_CHAR
            yield "".join(word_list)
            word_list[i] = c
    
    def _process_wildcard(self,wildcard,word_index):
        """Connects the node of a new word with all nodes for words 
        that match the same wildcard string, and adds the new node's 
        index to the wildcards map."""
        if wildcard not in self.wildcards:
            self.wildcards[wildcard] = [word_index]
        else:
            for neighbor_index in self.wildcards[wildcard]:
                self.g.add_bidirectional_edge(word_index,neighbor_index)
            self.wildcards[wildcard].append(word_index)

    def transform(self,w1,w2):
        """Prints the transformation path from w1 to w2, or that no 
        such transformation path exists.
        
        Args:
            w1,w2: Strings.
        
        Raises:
            KeyError: At least one word is not in the transformer.
        """
        n1, n2 = self.word_to_node[w1.upper()], self.word_to_node[w2.upper()]
    
        output = []
        for word_index in bidirectional_search(self.g,n1,n2):
            output.extend(list(self.g[word_index].data))
            output.extend(list(" -> "))
        
        if len(output) > 0:
            print("".join(output[:-4]))  # Exclude the last " -> ".
        else:
            print("Transformation is impossible.")
    
    def get_group(self,w1):
        """Returns a list of all possible start words that can be 
        transformed into a word w1."""
        n1 = self.word_to_node[w1.upper()]
        return bfs(self.g,n1) 
    
def toy_test():
    """Tests the example input on a limited dictionary."""
    wt = WordTransformer(["damp","lamp","limp","lime","like","bump"])
    wt.transform("damp","like")
    wt.transform("damp","bump")
    
# I "stress test" the WordTransformer class on the Unix "Word" corpus, 
# accessed through Python's NLTK library. The corpus has 236,736 words, and 
# loading them all into the WordTransformer with proper connections takes 
# between 8 and 9 seconds on my machine.
    
def test():
    """Creates a WordTransformer with the full corpus of spell-check 
    words uses on Unix operating systems loaded. Tests a number of 
    sample inputs, then returns the WordTransformer.
    
    Usage:
        wt = c17p22.test()
        wt.transform("hello","world")
        wt.get_group("extend")
    """
    wt = WordTransformer(words.words())
    
    inputs = [("damp","like"),
              ("luck","fred"),
              ("jazz","ache"),
              ("road","knit"),
              
              ("blimp","phone"),
              ("sauce","bread"),
              ("otter","piano"),
              ("doggy","river"),
                     
              ("monkey","killer"),
              ("screen","glossy"),
              ("reduce","mooing"),
              
              ("blubber","swarthy")]
                     
    print("\nTesting on sample inputs:")
    print("#" * 79)
    for input in inputs:
        print(f"\nFrom '{input[0]}' to '{input[1]}':",end="\n    ")
        wt.transform(*input)
        
    return wt