import sys
sys.path.append('..')
from data_structs import Trie

# c17p21

# Longest Word: Given a list of words, write a program to find the longest 
# word made of other words in the list.
#
# EXAMPLE
# Input: cat, banana, dog, nana, walk, walker, dogwalker
# Output: dogwalker 

##############################################################################

# An important question is whether we can count "duplicates" of words in the 
# list. If the list is ["dog", "cat", "dogcat", "catdogdog"], then is the 
# longest word "dogcat", the longest word that uses each word at most once, 
# or "catdogdog" that is the result of concatenating repetitions of the same 
# word? I assume the LATTER option for this problem.

# Also important is to determine how to handle the empty string if it appears 
# in the list. Is the empty string made of other words in the list? I assume 
# NO for this problem, so if the input is ["cat","","dog"], then I will output
# None. Because of this, I choose to ignore empty strings in the input.

# Finally, when there is more than one correct solution, do we return all, or 
# is one acceptable? I assume I can arbitrarily return one such word.

# As with many string/matching problems, a trie seems like a natural data 
# structure to start to think about using. Say we load all words from the list
# into a trie in O(N*L) time, where N is the number of words and L is the 
# length of the longest string in the list.

# I began to think about this problem with an approach that forbids word 
# duplicates. Say we have all words made of the first w words in the list. If 
# the list is ["aa","bb","cc","aacc","aabbcc","aab","aabaabaa"], and w is 2,
# then these words would be ["aa","aabb","bb","bbaa"], and two of these, "aa"
# and "aabb", are prefixes to some word in the input list (as verified in the
# trie.) When looking at the third word, "cc", we then consider three cases to 
# update the list of prefixes: A) concatenating "cc" to the ends of each 
# prefix ("aacc" and "aabbcc", which are both words in the list), and B)  
# concatenating each of the w-1 words to the end of "cc" ("ccaa" and "ccbb", 
# neither of which can be prefixes), and C) the word itself as a prefix (which
# here cannot be a prefix to other words). 

# At first, the number of prefixes to track seems to grow exponentially, and 
# it does if we do not attempt to weed out prefixes as they are built. At 
# some stage where there are X prefixes, we keep them, then from case A) add
# another X prefixes that end with the new word, then from case B) add X that
# begin with the new word, and then finally add the new word, so at the next 
# stage the number of prefixes has increased to 3X+1. We can define the total
# number of prefixes at an index i recursively as:

# P[0] = 1
# P[i] = 3*P[i-1]+1

# Because we can expand P[i] to = 3^(i) + 3^(i-1) + ... + 3^(0), it is clear 
# that for input of length N, the list of prefixes grows in O(N*3^N).

# While eliminating prefixes early with a trie would certainly help decrease 
# the runtime (if only possible prefixes are allowed as prefixes are built, 
# then at most O(L*N) prefixes will ever be allowed in the list, so runtime 
# to traverse the whole list would be in O(L*N^2)), it seems like a lot of 
# work to attempt to "build up" possible words. My better approach below 
# instead checks existing words to determine if they are made of other words. 

# Say that we want to determine whether or not the word "aabaabaa" is made 
# up of other words in ["aa","bb","cc","aacc","aabbcc","aab","aabaabaa"]. If 
# we travel along the characters in "aabaabaa" from left to right, we see that
# the first prefix "a" is not another word, but that "aa" is. 

# We can say that "aabaabaa" is made up of other words, then, if (but not
# necessarily ONLY if) "baabaa" is also made up of other words in the list, so
# we can recursively check that  subword. In doing so we find that "b" is not
# another word, and then that "ba" does not exist at all in the trie, so we
# can rule out "baabaa" as being made of other words and try again from the 
# top level. This brings us to the third prefix, "aab", which also is a word,
# so we recursively check "aabaa" and eventually find that it, and thus the 
# full word at the top level is made of other words.

# By memoizing past results and using a Trie for early termination, we can  
# verify a word in O(L^2) time, so the entire function takes O(N*L^2) time. 
# Assuming that we are working with English words, L should be quite small, 
# and if we can assume that L is constant over our inputs, then we can argue 
# that the approach runs in linear time with a very low constant factor. Space
# requirements are in O(L*N).
 
# I sort words by their length in decreasing order so that we can return
# immediately the first word that is made up of other words. Assuming that the 
# input words have some maximum possible length L, I implemented a simple 
# bucket sort that organizes words by their length (with words of equal length 
# ordered arbitrarily) and generates lists of indices to the original list. 
# The sort dynamically grows the list of buckets and runs in O(L+N) time, so 
# is not a bottleneck to the above approach (unlike if we used an O(NlogN) 
# comparison sort).

def long_to_short(lst):
    """Given a list of words, generates indices to words in decreasing
    order by length. Equally long words are yielded in arbitrary order.
    
    Args:
        lst: A list of strings.
    
    Yields:
        Lists of int indices to lst.
    """
    buckets = [[]]  # buckets[x] to hold indices to words of length x.
    
    for i,word in enumerate(lst):
        while len(word) >= len(buckets):
            buckets.append([])
        buckets[len(word)].append(i)
    
    for b in range(len(buckets)-1,0,-1):  # Ignore empty strings.
        for word_index in buckets[b]:
            yield word_index

def f1(lst):
    """Returns the longest word made of other words in a list.
    
    Args:
        lst: A list of strings.
        
    Returns:
        A string, or None if no word in list is made of other words.
    """
    if len(lst) < 2:
        return None
        
    trie = trie_from_list(lst)
    for word_index in long_to_short(lst):
        if word_made_of_others(lst[word_index],trie):
            return lst[word_index]
    return None
    
def trie_from_list(lst):
    """Inserts words from a list into a trie and returns the trie."""
    trie = Trie()
    for word in lst:
        if len(word) > 0:
            trie.insert(word)
    return trie
 
def word_made_of_others(word,trie):
    """Given a word that is assumed to be inserted already into a trie,
    returns True if the word is made of other words in the trie, and 
    False otherwise."""
    return subword_made_of_others(word,0,set(),trie.root)

def subword_made_of_others(word,start_i,fail_set,root):
    """Given a word and index start_i to a character within that word, 
    returns True if the subword from start_i to the end of the word is 
    made of other words in a trie, and False otherwise. Because it 
    assumes that the characters in word[0:start_i] are made of other 
    words in the trie, a return of True for any start_i > 0 implies 
    that the full word is also made of other words in the trie.
    
    Args:
        word: A string.
        start_i: An int index to a character in word.
        fail_set: A set of start_i values that have already been 
          determined to result in a return value of False.
        root: A TrieNode instance treated as root of the trie.
    
    Returns:
        A Boolean.
    """
    
    # In order to determine whether or not the subword from start_i to
    # the end of word is made up of other words in the trie, we trace  
    # this subword down the trie from the root.
    
    subword_tracer, next_i = root, start_i        
    while True:
    
        # If the next prefix of the subword does not exist in the trie, 
        # then the subword cannot be made of up words in trie.
        
        char = word[next_i]  
        if char not in subword_tracer.children:
            fail_set.add(start_i)
            return False        
        subword_tracer = subword_tracer.children[char]
        next_i += 1  
        
        if subword_tracer.is_end_of_word():          
                        
            # When start_i == 0 and next_i == len(word), then we have 
            # identified only the full word (NOT made of other words).
            
            if next_i == len(word):
                return True if start_i > 0 else False
            
            if next_i not in fail_set:   
                if subword_made_of_others(word,next_i,fail_set,root):
                    return True 

# The final input below is useful to show the benefits of memoizing previous
# failed values for start_i when calling subword_made_of_others(). When an 
# extra line is added that prints information about every time the function is 
# called, we can comment out the line that adds values to fail_set and see the
# number of calls increase sharply. With the line, there is no more than one 
# call per character, each call in O(L) time; thus O(L^2) time per word. 
                    
def test():
    """Tests on some sample inputs."""
    inputs = (["cat","banana","dog","nana","walk","walker","dogwalker"],
              ["bob","bobbob"],
              ["dog","cat","catdog","dogdogcat"],
              ["aa","bb","cc","aacc","aabbcc","aab","aabaabaa"],
              ["aa","bb","cc"],
              ["a","bb","ccc","dddd","abbcccddddacccddddcccbbabb"],
              ["a","b","c","d","abbcccddddacccddddcccbbabbX"],
              ["do","dogwalker","gwalk","walk","ogwalk","alk","e","r","d"],
              ["dogwalker","dog","d","og","waler","walk"],
              ["abcde","abc","ab","a","bc","bcd","cd","b","c","d"])
              
    for input in inputs:
        print(f1(input))