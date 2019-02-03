import sys
sys.path.append('..')
from data_structs import Trie

# c17p17

# Re-Space: Oh, no! You have accidentally removed all spaces, punctuation, and
# capitalization in a lengthy document. A sentence like "I reset the computer. 
# It still didn't boot!" became "iresetthecomputeritstilldidntboot". You'll 
# deal with the punctuation and capitalization later; right now you need to 
# re-insert the spaces. Most of the words are in a dictionary but a few are 
# not. Given a dictionary (a list of strings) and the document (a string),
# design an algorithm to unconcatenate the document in a way that minimizes 
# the number of unrecognized characters.
#
# EXAMPLE:
# Input: jesslookedjustliketimherbrother
# Output: jess looked just like tim her brother (7 unrecognized characters)
#         ‾‾‾‾                  ‾‾‾

##############################################################################

# There are some important clarification questions. First, is there any 
# meaning to an empty string in the input dictionary? A trivial "match" to an
# empty string does not change the number of unrecognized characters and 
# seems like a waste of time. I simply ignore any such strings in the input.

# Another question is of the format of the document string. Are newlines 
# between different lines part of the "punctuation" that was removed, or are
# substrings that represent different lines separated by any boundaries? I 
# assume for my solution that no line boundaries remain, so the document
# contains only lower-case characters.

# Another question is whether there is any preference among multiple optimized 
# spacing schemes. What, if anything, should break a tie when more than one 
# option would lead to the same minimized number of unrecognized characters?

# Compound words can give rise to this type of situation. Say the original 
# sentence was as follows:

# "He opened the door and stepped out, sourcing the enemy with his handheld 
# GPS tracker."

# If the dictionary contains tens of thousands of natural English words and 
# their inflections, then there are TWO cases where unconcatenation would 
# result in the same number of unrecognized characters. In one, creating a 
# compound word would be incorrect ("outsourcing"), while in the other the 
# opposite is true ("hand held").

# I don't have a confident a priori assumption as to which default would 
# lead to more accurate results in written English. I lean towards guessing
# that creating compound words is more likely than not to be correct, but 
# there are plenty of cases where this would be wrong ("hishandheldaredball"). 

# More advanced NLP techniques like word sense disambiguation and POS-tagging 
# could help minimize errors in a real-life application, but my solution makes 
# as few words as possible while minimizing unrecognized characters and thus 
# creates compound words whenever it can.

# Now, to the task: optimizing the number of unrecognized characters to be as
# low as possible. This sounds like a dynamic programming problem.

# I use a memo that keeps track of TWO things, for every index i in doc. I 
# call this memo OPT, and have OPT[i] hold an object with two attributes, 
# "count" and "nextword". Count refers to the optimized (minimal) number of 
# unrecognized characters for the substring from indices i to the end of doc.
# nextword refers to the index of the next character that should be printed
# with a space BEFORE it (or the length of doc if no more spaces are needed) 
# should i be treated as the start of a word.

# We populate this memo from "back" to "front", with the base case 

# Assuming that if we have the values of OPT[j] already stored for all indices
# i < j < len(doc), then OPT[i].count is equal to the MINIMUM of:

#     OPT[i+1].count + 1 (treat the character here as unrecognized)          
#     min OPT[x+1].count, for all x that mark the end of a word starting at i

# One way to test each of the x values is to, given a maxlength M of words in 
# the list, check every substring from doc[i:i+1] to doc[i:i+maxlength+1].
# Assuming that the words in the list are hashed into a Python dictionary, 
# we could do this in O(M^2) time for each index i in doc. 

# But this approach duplicates a lot of work, so I use a trie instead to store
# words in the dictionary. This means that all we must do at each i is to 
# traverse at most maxlength steps through the trie, checking for OPT count 
# values any time that the trie signals an end of word. Total runtime is from 
# loading the trie with all words in the dictionary, and processing as above,
# and creating the output string. This is O(M*D+M*S), where D is the number of
# entries in the dictionary and S the length of the document.

# Assuming that we are working with natural English text, we might be able to
# argue that M is in O(1) (given that we cannot expect there to be words
# greater than 20 or so characters in a dictionary, unless perhaps we are 
# working in some specialized domain like medicine), but for abstract cases, 
# using a trie is asymptotically more efficient than the first approach.

class OptObject:
    """Storage class for the dynamic programming memo.
    
    Attributes:
        count: An int. The minimal number of unrecognized characters.
        nextword: An int. Index to start of next word. 
    """

    def __init__(self,count=None,nextword=None):
        """Inits an OptObject with specified values, or None."""
        self.count = count
        self.nextword = nextword
     
def f1(doc,dictionary):
    """Unconcatenates a document to minimize unrecognized characters.
    
    Args:
        doc: A string of only lower-case letters.
        dictionary: A list of strings to be treated as words. Strings 
          should be stripped of non-letter characters. Case-insensitive. 
    
    Returns:
        A string.
    """
    trie = Trie()
    for word in dictionary:
        if len(word) > 0 and len(word) <= len(doc):
            trie.insert(word.lower())

    # Both an empty string and a string of length one cannot be 
    # unconcatenated, so return a copy of that string.
    
    if len(doc) == 0:
        return ""
    if len(doc) == 1:
        return doc[:]
        
    opt = get_opt(doc,trie.root)       
    return build_string(opt,doc)     
    
def get_opt(doc,root):
    """Determines the optimal spacing for a string.
    
    Args:
        doc: A string of only lower-case characters.
        root: A TrieNode instance representing the root of a trie.
    
    Returns:
        A list of OptObject instances.
    """
    opt = [OptObject() for _ in range(len(doc))] 
    
    # The "base case" is the index one past the end of doc, which has
    # no spaces and no unrecognized characters. One extra object serves
    # as "padding" removing the need for checks to avoid IndexError.
    
    opt.append(OptObject(0,len(doc)))
      
    i = len(doc)
    while i > 0:
        i -= 1
        
        # At each index i, the "default" count value is the result of 
        # treating character at i as unrecognized. The "default" 
        # nextword will already have been set if i+1 was found to mark
        # the start of a word that minimzes unrecognized characters.
        
        opt[i].count = opt[i+1].count+1
        if opt[i].nextword == None:
            opt[i].nextword = opt[i+1].nextword
            
        j = i
        cur_node = root        
        while j < len(doc):
            
            # We terminate as early as possible when the trie does not
            # support a substring beginning at i. Otherwise, we "grab"
            # the longest possible word starting at i that lowers count
            # if any such words exist.
            
            if not doc[j] in cur_node.children:
                break
            
            cur_node = cur_node.children[doc[j]]
            j += 1 
            
            if cur_node.is_end_of_word() and opt[j].count <= opt[i].count:
                opt[i].count = opt[j].count
                opt[i].nextword = j
                if i > 0:
                    opt[i-1].nextword = i
    return opt                

def build_string(opt,doc):
    """Constructs the unconcatenated string.
    
    Args:
        opt: A list of OptObject instances.
        doc: A string of only lower-case characters.
    
    Returns:
        A string of only lower-case characters and spaces.
    """
    builder = []
    next_space = opt[0].nextword

    for i in range(len(doc)):
        if i == next_space:
            builder.append(" ")
            next_space = opt[i].nextword
        builder.append(doc[i])

    return "".join(builder)
    
def test():
    """Tests some sample inputs. Far from exhaustive but covers basic 
    "edge cases" and confirms algorithm behavior is not greedy."""
    dict_a = ["hope","hopeless","hopelessly","less","hop","shop","sly","look",
              "looked","fox","ox","foxes","sand","a","and","but","she","big",
              "dog","at","the","openness","just","like","her","brother"]
    
    docs_a = ["",
    
              "a",
              "x",
    
              "ax",  # word at start
              "xa",  # word at end
              "ox",  # full word
              "xx",  # no word
              
              "atx",
              "xat",
              "dog",
              "xax",
              "xtx",
              
              "dogdog",
              "dogxdog",
              "dogxxdog",
              
              "hopenness",  # h<openness> better than <hope>nness
              "opelessly",  # ope<less>ly better than opeles<sly>
              "hopeless",
              "hopelessly",
              
              "jesshopelesslylookedatthebigsandox",
              "jesslookedhopelesslyliketimherbrother",
              
              "xmpqqqleszzz"]
    
    # More examples of behavior with compound words.
    
    dict_b = ["he","stood","and","stepped","out","sourcing","the","enemy",
              "with","his","handheld","GPS","tracker","hand","held","a",
              "red","ball","outsourcing","doorknob","door","knob","turned"]
              
    docs_b = ["hestoodandsteppedoutsourcingtheenemywithhishandheldgpstracker",
              "hishandheldaredball",
              "heturnedthedoorknob"]
              
    for docs, dictionary in [(docs_a,dict_a),(docs_b,dict_b)]:
        for doc in docs:
            print("In : ",doc)
            print("Out: ",f1(doc,dictionary))
            print("-" * 80)