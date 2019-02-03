# c16p20

# T9: On old cell phones, users typed on a numeric keypad and the phone would
# provide a list of words that matched these numbers. Each digit mapped to a 
# set of 0- 4 letters. Implement an algorithm to return a list of matching 
# words, given a sequence of digits. You are provided a list of valid words 
# (provided in whatever data structure you'd like). The mapping is shown in 
# the diagram below:
#
#        1:[     ]   2:[a,b,c]  3:[d,e,f]
#        4:[g,h,i]   5:[j,k,l]  6:[m,n,o]
#        7:[p,q,r,s] 8:[t,u,v]  9:[w,x,y,z]
#                    0:[     ]
#
# EXAMPLE
# Input: 8733
# Output: tree, used

##############################################################################

# One question is how to handle sequences with the digits "1" or "0". For 
# simplicity, I chose to reject any such inputs and raise an exception.

# The first approach uses a specially-designed Trie that stores words 
# according to their T9 encoding. Words with the same encoding are stored in
# arbitrary order, as the problem does not specify any preferred output order.
# The trie has a benefit of allowing us to exit early if we have a sequence 
# prefix that cannot possibly lead to a stored word.

# Inserting a new word from a list, and retrieving the list of words for an 
# input sequence, both run in O(N) time, where n is the length of the word or
# pattern being retrieved. If we expect to be working with English words whose 
# length is generally less than 20 characters, or if we are working with some 
# other class of strings with a maximum length, then we could argue that this 
# insertion and retrieval time is in O(1) per word or pattern. 

class T9TrieNode:
    """Node to a trie for a T9 sequence.
    
    Rather than a traditional trie, with a different child node for
    each letter in the alphabet, this trie has a child  node for each 
    group of letters associated with a single key.
    
    Attributes:
        children: A list of 8 T9TrieNode instances, or None objects. 
          The 0th entry maps to the first group of letters, or [abc], 
          the 1st maps to [def], and so on.
        mapping: A dictionary from lower-case letter as strings to the 
          appropriate child index.
        null: A set of words that terminate at the current node.
    """
    
    def __init__(self,word_list=None):
        """With default parameters, inits an empty T9TrieNode object.
        If word_list is a list of strings, attempts to insert each word
        but raises an exception and halts if any string is invalid."""
        self.children = [None] * 8   
        self.mapping = self._create_mapping()
        self.null     = set()      
        if word_list is not None:
            for word in word_list:
                self.insert(word)
        
    def _create_mapping(self):
        """Creates and returns a dictionary from letter to index."""
        group_heads = ["a","d","g","j","m","p","t","w",None]
        mapping = {}
        char, val = "a", 0

        while True:
            if char == group_heads[val+1]:  # New letter group.
                val += 1
            mapping[char] = val
            if char == "z":
                return mapping
            char = chr(1+ord(char))  # Advance letter by one.
            
    def insert(self,word):
        """Inserts a lower-cased version of any non-empty string, with
        itself as root.
        
        Args:
            word: A string made up only of characters in [a-z][A-Z].
        """
        if len(word) > 0:            
            self._insert(word.lower(),0)
            
    def _insert(self,word,i):
        """Recursively traces or creates the path to the ith letter 
        of the word, or stores the word at the end of the path.
        
        Raises:
            ValueError: word has an illegal character.   
        """
        if i == len(word):
            self.null.add(word) 
        else:
            c = word[i]          
            if c in self.mapping:
                self._ensure_child(self.mapping[c])
                self.children[self.mapping[c]]._insert(word,i+1)
                return
            raise ValueError("Illegal character: {}".format(c))
    
    def _ensure_child(self,x):
        """Creates self's x'th child if it does not exist."""
        if self.children[x] is None:
            self.children[x] = T9TrieNode()
   
    def retrieve(self,seq):
        """Retrieves all words that match an integer encoding."""
        seq = str(seq)
        if len(seq) == 0:  # Empty sequence matches to no words.
            return []
        return self._retrieve(seq,0)
        
    def _retrieve(self,seq,i):
        """Recursively traces through to the node representing 
        the ith digit of the sequence, or returns that there is 
        no such path, indicating that no words match.
        
        Raises:
            ValueError: The sequence has an illegal character.
        """
        if i == len(seq):
            return list(self.null) # Copy to list, user cannot modify. 
        dig = seq[i]                         
        if "2" <= dig and dig <= "9":
            index = int(dig) - 2  # 2 is lowest digit so 0th index.
            if self.children[index] is None:
                return []
            return self.children[index]._retrieve(seq,i+1)
        else:
            raise ValueError("Illegal key entered: {}".format(dig))

# Another approach is simply convert words to a T9 code and then store them in 
# a hash value where the key is that code. Expected runtime should be the same 
# but it would be interesting to see which works more quickly. The trie makes 
# a recursive call for every character in the input word or sequence, and we 
# can expect this to take more time than a simple hash table lookup. On very 
# long inputs, though, the trie will terminate the earliest it can on a
# sequence that does not match to any words, which could prove advantageous. 

# With short English words, though, the hashing approach seems better.

class T9HashTable:
    """Special hash table that stores words with the same T9 encoding.
    
    Attributes:
        mapping: A dictionary from lower-case letter to encoding digit.
        table: A dictionary from strings of digits to lists of words.
    """
    
    mapping = {"a": 2, "b": 2, "c": 2,         \
               "d": 3, "e": 3, "f": 3,         \
               "g": 4, "h": 4, "i": 4,         \
               "j": 5, "k": 5, "l": 5,         \
               "m": 6, "n": 6, "o": 6,         \
               "p": 7, "q": 7, "r": 7, "s": 7, \
               "t": 8, "u": 8, "v": 8,         \
               "w": 9, "x": 9, "y": 9, "z": 9}

    def __init__(self,word_list=None):
        """With default parameters, inits an empty T9HashTable object.
        If word_list is a list of strings, attempts to insert each word
        but raises an exception and halts if any string is invalid."""
        self.table = {}
        if word_list is not None:
            for word in word_list:
                self.insert(word)
                        
    def insert(self,word):
        """Encodes word and inserts into hash table."""
        code = "".join(self._generate_code(word.lower()))
        if code in self.table:
            self.table[code].append(word)
        else:
            self.table[code] = [word]
    
    def _generate_code(self,word):
        """Returns a string T9 encoding for a word."""
        code_builder = []
        for i in range(len(word)):            
            c = word[i] 
            if c in self.mapping:
                code_builder.append(str(self.mapping[c]))
            else:
                raise ValueError("Illegal character: {}".format(c))
        return code_builder
        
    def retrieve(self,code):
        """Returns a list of all words that map to integer encoding."""
        code = str(code)       
        if code in self.table:
            return self.table[code]
        else:
            return []
            
def test():
    """Tests some input words."""
    word_list = ["used","tree","banana","cat","dog","bat","act","eli","fog"]
    test_trie = T9TrieNode(word_list)
    test_table = T9HashTable(word_list)
    for seq in [8733,226262,228,354,364]:
        print("TRIE :",seq,test_trie.retrieve(seq))
        print("TABLE:",seq,test_table.retrieve(seq))
        print("")