import sys
sys.path.append('..')
from data_structs import Trie, DequeQueue

# c17p17

# Multi Search: Given a string b and an array of smaller strings T, design a 
# method to search b for each small string in T. 

##############################################################################

# The instructions do not specify a format for the output. I am going to 
# assume that a list of ordered pairs, each pair holding the start and end 
# indices of each hit, is acceptable. 

#                        0   00         11 1 22    2 22
#                        0   45         56 8 01    6 89
#                       "llamas are a slim type of animal"

# So if the string b is "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^" and the array of 
# strings T is ["llama", "llamas", "type","animal", and "im"], my solution 
# outputs the list [(0,4),(0,5),(15,16),(18,21),(28,29),(26,31)]. This format 
# does not categorize hits by the string in T that they match, though I
# suppose I could include this information if preferred. The order of the 
# tuples is also not specified in the problem, so I assume that any order is 
# fine. My solution returns hits in increasing order by the END index. 

# Like with many string/matching-based problems, I used a trie to store all of
# the strings in T that we must search for. We "look at" each character in b 
# once, and if the character matches the beginning of what could be a word
# (that is, if that character maps to a child to the root of the trie), then
# we keep track of that node and attempt to continue traveling down the trie 
# from that node as we look at subsequent characters in b. We make sure to
# stop tracking that path if we discover that it cannot lead to a string in T.

# The time to insert every string from T into the trie is O(c(T)), where c(T)
# is the total number of characters in all of the strings in T.

# Since we will never have more nodes to track at any one time than there are 
# strings in in T, one (generous) bound for the runtime of the second part of 
# the function is in O(B*N), where B is the number of characters in string b 
# and N is the number of strings in T. 

# When there are many strings in T, so N is very large large, but each of the
# strings in T has fewer than N characters, there is a better bound of O(B*L),
# where L is the length of the longest string in T. This is because all node
# trackers will "time out" within at most L steps through b, and since each 
# new step adds no more than 1 new tracker, no more than L must be checked at
# each any one step through b.

# While this does not improve asymptotic performance, on certain inputs we 
# can see that this approach works efficiently with multiple words in T that 
# begin with the same prefix of characters. This is because we track only ONE 
# node as we verify them. For example, if the words in T are "dog" and 
# "dogstand" then we need only one tracker to verify the characters "d","o",
# and "g" for both words in "the dogsitter bought my dog a dogstand." At each
# "g", we recognize that a word has been found at add that hit to the output, 
# but maintain the tracker as it searches for "dogstand".

# So the total runtime is O(c(T)+L*B). Since L is the length of the longest 
# word, c(T) is in O(L*N), so we can also describe the runtime as O(L(N+B)). 
# This is quite efficient when we expect L to be relatively low, such as with
# natural English text.

# O(c(T)), or O(L*N) space is required for the trie, which is on the same
# order as the size of the input, and O(L) space is needed to keep each 
# tracker, so total space requirements is O(L*N).

# I make no assumptions as to the characters allowed in b or T. The trie is 
# caps-sensitive, so if I want the searcher to be caps-insensitive, I could 
# convert b and each string in T to lower-case before processing.

# An important possibility to handle is when one of the strings in T is the 
# empty string. When this is the case, it could be argued that every "empty" 
# interval in b is a hit. I choose instead to ignore empty strings in T.

def f1(b,T):
    """Finds and returns all instances of strings in T that appear in 
    string b. Not case-sensitive.
    
    Args:
        b: A string.
        T: A list of strings. Empty strings in the list are ignored.
    
    Returns:
        A list of tuples (i1,i2), where i1 is the index of the first 
        character, and i2 the index of the last, for each hit.
    """
    
    # If there are no strings to search for, then there are no hits. 

    if len(T) == 0:
        return []
    
    # Strings in T longer than b cannot possibly be in b, so ignore.
    
    trie = Trie()
    for word in T:
        if len(word) > 0 and len(word) <= len(b):
            trie.insert(word)
    
    # Prefixes to possible hits are kept on a queue is updated on each
    # new character. For example, if T is ["abcd","car"] and b "abcd", 
    # then after checking the character "c" in "abcd", the queue holds 
    # two references to nodes in the trie: the "c" below the "b" below 
    # "a" below the root, and, and then the "c" below the root.
    
    prefixes = DequeQueue()
    output = []
    
    for i in range(len(b)):
    
        prefixes.add(trie.root)
        prefix_num = len(prefixes)  # Q length changes, so store! 
        for _ in range(prefix_num):  
        
            node = prefixes.remove()
            if b[i] in node.children:
                
                # Even if the new node marks the end of a word, 
                # continue tracking it, as this word might also be the
                # prefix for another string in T ("dog" and "doggy").
                
                new_node = node.children[b[i]]
                prefixes.add(new_node)
                
                if new_node.is_end_of_word():
                    output.append((i-node.depth,i))
   
    return output
        
def test():
    """Tests some sample inputs. Could also write a brute-force search
    to check correctness more rigorously."""
    bT_pairs = [("abcde",["a","ab","abc","abcd","abcde"]),
                
                ("abcde",["abcde","bcde","cde","de","e"]),
                
                ("llamas are a slim type of animal",
                ["llama","llamas","type","animal","im"])]
                
    for b,T in bT_pairs:
        print(f1(b,T))