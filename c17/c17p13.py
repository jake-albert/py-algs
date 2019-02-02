# start

# this is quite a cool dynamic-programming problem. 

# the task is to optimize the number of unrecognized characters to be as low as possible,
# but there is still a question to ask the interviewer about whether there is a preference
# to favor words together or separate when the number of unrecognized characters would 
# remain the same. 

# As an example...say that the original sentence was the following:
# "He opened the door and stepped out, sourcing the enemy with his handheld GPS tracker."

# There are TWO cases here where the un-concatenation could have occurred differently. These
# are "out sourcing" and "outsourcing", as well as "handheld" and "hand held". I don't really 
# have a confident a priori assumption as to which would lead to more accurate results in 
# written englih off the top of my head, though if I had to guess I would say it is better
# to err on the side of making compound words as opposed to leaving them split. I say 
# this mostly because I took longer to find a contrived verstion of out sourcing where that 
# actually wasn't preferable, but that is not a realiable reason to be confident here. 

# Additionally, there is an opposite version like "His hand held two marbles" where this 
# assumption would go wrong. Obvioulsy, more advanced NLP techniques like POS-tagging 
# could help minimize erros in a real life situation.

# Still, good to ask an interviewer about this and discuss options.

# HERE is the framework taht I am going to use 

# Also is helpful to ask what form te document comes in. For example, is it a single
# string? Is it a bunch of strings that each represents a line, and we can be confident
# that there are boundaries between the spaces? I am going to assume for this problem
# that the document comes in the form of a single string of lower-case characters.

# In addition, I might ask that the dictionary come in the form of a TRIE rather than 
# a hash table, for reasons that can be explained later. I will implement my own trie
# later on to use, but for now let's assume the words are stored in a trie

# I will use a memo that keeps track, for every index i in the string that represents 
# the document, of TWO things. We will call this memo OPT, and have OPT[i] hold an object
# with two attributes, "count" and "lastspace". Count refers to the optimized (minimal)
# number of unrecognized characters for the string from indices 0 to i. Lastspace refers
# to the index of the character that follows the most recent space symbol, or -1 if 
# there is no previous space (this is for backtracking purposes).

# We know that if we have the values of OPT[j] already stored for all indices 0<=j<i,
# then OPT[i].count is equal to the MINIMUM of:
#     OPT[i-1].count + 1              ......... when we treat this char as unrecognized
# min OPT[x-1].count for all x that mark the start of a valid word that ends at i

# how do we keep track of ALL words that end at a given index i? one way would require 
# knowing a maximum length of all the words in the dictionary and then subsequently 
# checking for membership in the dictionary of all the substrings no longer than max
# length that also end at i. Example for the string "jesshopelessly" we would attempt
# for i = 13 (the "y") "y", "ly", "sly", and so on until we have hit the limit. But 
# to do this would take O(maxlength**2) time in terms of concatenating strings and 
# testing them. We will use a trie instead to store the words. 

# Using a trie, then on every turn for a new index i we must do O(1) checks for 
# every prefix that is currently possible, either extending it or not, and then if it 
# can be extedned to the current index, then identifying whether it is the end of a 
# word or not and updating based on that. The maximum number of prefix candidates we 
# will be looking at for a given index is equal to the number of words that can end 
# at an index, which naively is in O(i) since we have to check all the way back to the 
# start, but using a trie we can cull these down to be bounded by the maxlength, and 
# that is a VERY generous bound as using the trie will help to cull the vast majoirty
# of naive preix guesses. It can be argued that this is a linear time algorithm
# if the max length is considered a constant.  

# for the purposes of memoization, we also use a special object that stores two values
class OptObject:

    def __init__(self,count,lastspace):
        self.count = count
        self.lastspace = lastspace

from queue import DequeQueue
from stack import Stack
    
# determine the optimum spacings, then print
def f1(doc,trie):

    # an empty string is unconcatenated to an empty string
    if len(doc) == 0:
        return ""

    opt = get_opt(doc,trie)
    spaces = Stack()
    
    # use last spaces as backpointers
    j = len(doc) - 1
    while opt[j].lastspace >= 0:
        spaces.push(opt[j].lastspace)
        j = opt[j].lastspace
        
    # print with spaces
    nextspace = spaces.pop()
    for i in range(len(doc)):
        print(doc[i],end="")
        if i == nextspace: 
            print(" ",end="")
            nextspace = spaces.pop()
    print("\n",end="")
    
# the main algorithm is written iteratively    
def get_opt(doc,trie):
        
    # we prepare the memo with default values
    opt = [OptObject(None,None) for _ in range(len(doc))] 
    
    # we also use a queue to keep track of currently valid prefixes
    prefixes = DequeQueue()
    
    # the "base" case for the first character
    if doc[0] in trie.root.children:
        
        prefixes.add(trie.root.children[doc[0]])
        
        if trie.root.children[doc[0]].is_end_of_word():
            opt[0].count = 0
            opt[0].lastspace = -1
            if len(doc) > 1:
                opt[1].lastspace = 0
        else:
            opt[0].count = 1
            opt[0].lastspace = -1
    else:
        opt[0].count = 1
        opt[0].lastspace = -1
        
    # the "recursive" case that uses previous values
    for i in range(1,len(doc)):
        
        # the default value for the optimal count is if we discard the current character
        opt[i].count = opt[i-1].count+1
        
        # the default previous space depends on whether we have prevoiusly finished a word 
        if opt[i].lastspace is None:
            opt[i].lastspace = opt[i-1].lastspace
        else:
            opt[i].lastspace = i-1

        best_word_len = 0
        prefixes.add(trie.root)
        trials = len(prefixes)
        
        # look through every possible prefix and eliminate it if no longer viable
        for _ in range(trials):
            
            prefix_node = prefixes.remove()
            
            # return to end of queue if still viable
            if doc[i] in prefix_node.children:
                prefix_child = prefix_node.children[doc[i]]
                prefixes.add(prefix_child)
                
                # if we are currently at the end of a word
                if prefix_child.is_end_of_word():
                    word_len = prefix_child.depth
                                        
                    # first full word encountered
                    if i-word_len < 0:
                        opt[i].count = 0
                        best_word_len = word_len
                        opt[i].lastspace = -1
                        if i < len(doc)-1:
                            opt[i+1].lastspace = i
                        
                    # second or later full word encountered
                    elif opt[i-word_len].count < opt[i].count or \
                    (opt[i-word_len].count == opt[i].count and word_len > best_word_len):
                        opt[i].count = opt[i-word_len].count
                        best_word_len = word_len
                        opt[i].lastspace = i-word_len
                        if i < len(doc)-1:
                            opt[i+1].lastspace = i

    """                        
    for i in range(len(doc)):
        print(i,doc[i],opt[i].count,opt[i].lastspace)
    """
    
    return opt
        
test_trie = Trie()
for word in ["hope","hopeless","hopelessly","less","hop","shop","sly","look","looked","fox","ox","foxes","sand","a","and","but","she","big","dog"]:
    test_trie.insert(word)