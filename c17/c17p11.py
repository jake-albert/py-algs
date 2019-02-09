from random import randint

# c17p11

# Word Distance: You have a large text file containing words. Given any two 
# words, find the shortest distance (in terms of number of words) between them
# in the file. If the operation will be repeated many times for the same file 
# (but different pairs of words), can you optimize your solution? 

##############################################################################

# I assume that I have access to an NLP tokenizer like from the NLTK library 
# in Python that handles punctuation, hyphenation etc. consistently when 
# parsing files. So I abstract the text file as a list of ints. 
 
# I assume for this question that the distance between two word instances in
# the file is the absolute value of the difference between the two indices of 
# the words. This means that A) it does not matter if a greater index comes 
# before a lesser index; distance is always POSTIVE, and B) there is no
# "wrapping around" from the end of a file to the start. The first and last 
# words of the file/list are the two words with the greatest distance.

# My first thought on how to solve this problem was that storing info on word
# connectedness in a graph would be helpful. Say we create a new node for 
# each unique word in the document and add edges between words that somewhere 
# in the document are adjacent. Then, couldn't we simply call bidirectional 
# search over this graph to find the shortest path between two words? 

# It turns out that this give a different kind of "shortest distance" between 
# words than what we are interested in, because allowing one node to 
# represent every instance of a word in the text allows us to "jump" between 
# instances of a word without adding any distance cost when we should not.  

# Ex. "MY DOG IS THE BEST DOG IN THE WORLD BETTER THAN THE BLUE DOG."
#
#     Shortest path in the above graph from "MY" to "BLUE" is just 2;
#     from "MY" to "DOG", then a "jump" from that "DOG" to the last 
#     "DOG" that costs nothing, then from that "DOG" to "BLUE". The 
#     correct shortest distance is 12.

# Another idea involves storing indices to words in some way that lets us 
# calculate word distances easily. My solution below begins by reading the 
# text (list) once in O(N) time, where N is the word length of the text, and 
# storing in a dictionary the indices of all occurrences of each word.
     
# The trick is that because we read and store indices in increasing order, 
# the problem reduces to taking two sorted lists of integers and finding the 
# smallest absolute value difference between any two integers from each list, 
# which can be done in O(L1+L2). L1 and L2 being lengths of the lists, which 
# here correspond to the number of instances of each word in the document.

# This approach allows us to find the shortest distance between any two words 
# quite quickly, but for very long documents the most common words might 
# occur so often in a document that it would be helpful to calculate the 
# shortest distance between them and other words overnight so they may be 
# returned in O(1) time. This would require an extra O(M^2) storage, where M 
# is the number of words among which we want to store distances ahead of time,
# or O(M*N) time if we want to for some M words store their distances from 
# every other word for O(1) time lookup. 

# Whether we would want to actually do this, though, depends on specific time 
# and memory costs related to the type of document we are storing and what 
# words we expect to be looked up most often.
 
# I first implement the O(L1+L2) algorithm and test it against an O(L1*L2)
# brute-force algorithm for correctness:

def smallest_difference(lst_a,lst_b):
    """Given two lists of integers sorted in increasing order, returns
    the smallest absolute value difference between any two integers 
    from each list.

    Args:
        lst_a, lst_b: Lists of ints.
    
    Returns:
        An int. 
    """
    
    # I define difference as undefined when at least one list is empty.
    
    if len(lst_a) == 0 or len(lst_b) == 0:
        return None
        
    mindiff = float("inf")
    index_a, index_b = 0, 0
    
    while index_a < len(lst_a) and index_b < len(lst_b):
        
        if lst_a[index_a] == lst_b[index_b]:  # Best possible diff.
            return 0
        
        mindiff = min(mindiff,abs(lst_a[index_a]-lst_b[index_b]))
            
        # Since the lists are sorted, only advancing further into the 
        # list with the smaller element has a chance of resulting in a
        # DECREASED difference between the elements.
        
        if lst_a[index_a] < lst_b[index_b]:
            index_a += 1
        else:
            index_b += 1
    
    # Once one list has been fully traversed, we know that every yet
    # unseen value in the other list is greater than or equal to the
    # greatest value in the finished list. So diff cannot decrease.
    
    return mindiff
 
def sd_brute(lst_a,lst_b):
    """O(L1*L2) version of above function."""
    if len(lst_a) == 0 or len(lst_b) == 0:
        return None
    
    mindiff = float("inf")
    for index_a in range(len(lst_a)):
        for index_b in range(len(lst_b)):
            mindiff = min(mindiff,abs(lst_a[index_a]-lst_b[index_b]))
    
    return mindiff 
 
def test(trials,L1,L2):
    """Tests smallest_difference against sd_brute on random inputs.

    Args:
        trials: An int. Number of inputs to make and test.
        L1,L2: Ints >= 0. Lengths of input lists to test.
        
    Raises:
        AssertionError: The functions' output is different.
    """
    MAXVAL = max(L1,L2)**4
    
    for trial in range(trials):
    
        lst_a = sorted([randint(0,MAXVAL) for _ in range(L1)])
        lst_b = sorted([randint(0,MAXVAL) for _ in range(L2)])
        
        assert smallest_difference(lst_a,lst_b) == sd_brute(lst_a,lst_b)

# With that work done (arguably, the "real work" part of the problem), I wrote  
# a word dictionary that supports finding shortest distances between words 
# that actually works on text files. I wrote a rudimentary word "parser" that 
# defines "words" as longest possible sequences of consecutive, non-whitespace
# characters. (I guess I could also just install NLTK.)
 
def words_from_text(filepath):
    """Generator that yields words one by one from a file. 
    
    Treats whitespace characters as word boundaries, and greedily
    treats as many non-whitespace characters as possible as one word.
    All words are converted to lower-case before being yielded.
    
    Args:
        filepath: A string.

    Yields:
        Strings of non-whitespace characters.
        
    Raises:
        FileNotFoundError: filepath does not lead to a file.
    """
    
    try:
        with open(filepath,"r") as f:
            
            for line in f:                               
                read = 0
                while read < len(line):
                    
                    while read < len(line) and line[read].isspace():
                        read += 1
                    start_char = read
                
                    while read < len(line) and not line[read].isspace():
                        read += 1
                    
                    if read > start_char:
                        yield line[start_char:read].lower()
    
    except FileNotFoundError as e:
        print(e)
 
class FileDict:
    """Stores documents in a way to support word distance queries.
    
    Attributes:
        lookup: A dictionary from strings to indices of occurrences of 
          those strings in the document.
    """
    
    def __init__(self,filepath):
        """Inits a FileDict in O(N) time (N: word count).
        
        Args:
            filepath: A string path to the document.
        """
        self.lookup = self._load_dict(filepath)
        
    def _load_dict(self,filepath):
        """Loads each word occurrence into lookup."""
        lookup = {}
        index = 0
        
        for word in words_from_text(filepath):
            
            if word not in lookup:
                lookup[word] = [index]
            else:
                lookup[word].append(index)
            
            index += 1
    
        return lookup
        
    def word_distance(self,w1,w2):
        """Returns the shortest distance between any occurrences of two
        words in a document, or None if at least one word does is not 
        in the document.
        
        Args:
            w1,w2: Strings.
        
        Returns: 
            An int, or None.
        """
        if w1 not in self.lookup or w2 not in self.lookup:
            return None
            
        return smallest_difference(self.lookup[w1],self.lookup[w2])
    
def toy_test():
    """Tests a toy example."""
    fd = FileDict("c17p11.txt")
    
    triples =  [("this","is",1),
                ("purposes","bananas",4),
                ("parts","test",56),
                ("test","parts",56),
                ("this","the",2),
                ("missing_word","bananas",None)]
                   
    for w1,w2,d in triples:
        assert fd.word_distance(w1,w2) == d