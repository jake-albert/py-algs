# This trie implementation supports only word insertion and lookup. None of 
# the algorithmic problems in which I used a trie required a deletion 
# function, but there is no reason I cannot add to this in the future.

# The below trie also supports any Unicode characters, as opposed to a smaller
# set of characters such as lower-case letters, using a dictionary at each 
# node that maps from a character to a node that represents this character in 
# the subsequent position in a word. Another approach with a smaller set of 
# permitted characters, such as the 26 lower-case letters in English, would be
# to initialize every node with an array of length of 26.

# Unlike my binary tree implementation, the trie has a wrapper class with a  
# root and size attribute. This really is not necessary, as I could have gone 
# with only a node class that supports insert and lookup, but I chose to keep
# only a top-level size attribute so that the trie would not store sizes for 
# subtrees. (That could be useful in other situations.) 

class TrieNode:
    """The individual node class for the Trie.
    
    Attributes:
        children: A dictionary that maps strings of length 1, or 
          characters to TrieNode instances.
        depth: An integer. A Trie's root has depth 0. Corresponds to 
          the index of a character in a string stored in the Trie.
        parent: A TrieNode instance, or None if root of trie.
        EOW: A Boolean. True iff the path from the Trie's root to 
          the current TrieNode represents a valid word.
    """

    def __init__(self,depth,parent=None):
        """Inits TrieNode with no children at given depth."""
        self.children = {}
        self.depth = depth
        self.parent = parent
        self.EOW = False
        
    def is_end_of_word(self):
        """Returns a Boolean."""
        return self.EOW
        
    def mark_as_end_of_word(self):
        """Marks TrieNode as end of valid path to word."""
        self.EOW = True

class Trie:
    """A trie class that supports word insertion and lookup. Treats 
    as distinct all Unicode characters and thus is caps sensitive.
    
    Attributes:
        root: A TrieNode instance.
        size: An int. The number of words stored in the trie.
    """        
    
    def __init__(self):
        """Inits an empty Trie instance."""
        self.root = TrieNode(0)
        self.size = 0

    def __len__(self):
        return self.size
        
    def insert(self,word):
        """Treats a non-empty string as a single word and adds it."""
        self._insert_chars(self.root,word,0)
        
    def _insert_chars(self,node,word,i):
        """Recursive helper. Inserts the ith character of a word."""
        if i == len(word):
            if node.is_end_of_word():
                return 
            else:
                self.size += 1
                node.mark_as_end_of_word()
        else:
            if word[i] not in node.children:
                node.children[word[i]] = TrieNode(node.depth+1,node)
            self._insert_chars(node.children[word[i]],word,i+1)

    def in_trie(self,word):
        """Return True iff a word is in the trie. If the word is not in
        the trie, returns False as early as possible."""
        if len(word) < 1:
            return False
        return self._in_trie(self.root,word.lower())
        
    def _in_trie(self,node,word):
        """Recursive helper. Checks that the current, and if necessary
        the child node, align with the progression of the word."""
        if node.depth == len(word):
            return node.is_end_of_word()
        else:
            if word[node.depth]in node.children:
                return self._in_trie(node.children[word[node.depth]],word)
            else:
                return False