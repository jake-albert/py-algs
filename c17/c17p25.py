import sys
sys.path.append('..')
from data_structs import Trie
from functools import reduce
from operator import mul
from nltk.corpus import words
from time import time 

# c17p25

# Word Rectangle: Given a list of millions of words, design an algorithm to 
# create the largest possible rectangle of letters such that every row forms a
# word (reading left to right) and every column forms a word (reading top to 
# bottom). The words need not be chosen consecutively from the list, but all 
# rows must be the same length and all columns must be the same height. 

##############################################################################

# currently work in progress.

# NOT caps sensitive

test_words = ["aa","ab","bq","pq"]

max_L = 24

# when we do it on words.words(), the number of words smushed onto each other 
# for caps to lowercase changes it from 236736 to 234377

class References:

    def __init__(self,words,tries):
        self.words = words
        self.tries = tries

class RectBuilder:

    def __init__(self,row_len,col_len,refs):
        self.row_len = row_len
        self.col_len = col_len
        self.refs = refs
        self.row_trie = refs.tries[row_len]
        self.col_trie = refs.tries[col_len]
        self.tracers = [self.col_trie.root for _ in range(row_len)]
        self.row_words = []
        
    def print_rect(self):
        print("*"*self.row_len)
        for row_word in self.row_words:
            print(row_word)
        print("*"*self.row_len)
        
    def count_col_options(self):
        return reduce(mul,[len(tracer.children) for tracer in self.tracers])
    
    def count_row_options(self):
        return self.row_trie.size
   
    def row_options(self):
        for row_option in self.refs.words[self.row_len]:
            yield row_option
   
    # ASSUME WORD LENGTH IS CORRECT FOR ALL THREE BELOW
    def can_add_row(self,row_word):
        for i in range(len(row_word)):
            if row_word[i] not in self.tracers[i].children:
                return False
        return True
    
    def add_row(self,row_word):
        self.row_words.append(row_word)
        for i in range(len(row_word)):
            self.tracers[i] = self.tracers[i].children[row_word[i]]
                
    def rem_row(self):
        self.row_words.pop()
        for i in range(len(self.tracers)):
            self.tracers[i] = self.tracers[i].parent
    
def get_refs(lst):

    tries = [Trie() for _ in range(max_L+1)]
    words = [set() for _ in range(max_L+1)]
    
    for i, word in enumerate(lst):
        if len(word) > 0:
            tries[len(word)].insert(word.lower())
            words[len(word)].add(word.lower())
    
    return References(words,tries)

def get_orders(L):

    return sorted([(r,c) for c in range(1,L+1) for r in range(c,L+1)],
                  key = lambda p: p[0]*p[1],
                  reverse = True)
 
def f1(lst):

    print("getting refs")
    refs = get_refs(lst)
    print("refs gotten")
    for row_len, col_len in get_orders(max_L):
        print(f"Attempting to find a {row_len} X {col_len} rectangle.")
        builder = RectBuilder(row_len,col_len,refs)
        build_rect(builder)
    
#    onomatopoetically
#    nonuniformitarian
    
def build_rect(builder):
    
    if len(builder.row_words) == builder.col_len:
        builder.print_rect()
        return        
    
    #print(f"Depth: {len(builder.row_words)}")
    #builder.print_rect()
    #options, option_builder, tracer = [], [], builder.row_trie.root
    #get_col_options(builder,options,option_builder,tracer)
    #print(builder.count_row_options(), builder.count_col_options(), len(options))
    
    
    if builder.count_row_options() <= builder.count_col_options():
        options = [word for word in builder.refs.words[builder.row_len] if builder.can_add_row(word)]
        #print(len(options))
    else:
        options, option_builder, tracer = [], [], builder.row_trie.root
        get_col_options(builder,options,option_builder,tracer)
    
    
    for row_option in options:  
        builder.add_row(row_option)
        build_rect(builder)
        builder.rem_row()
        
            
def get_col_options(builder,options,option_builder,tracer):

    if len(option_builder) == len(builder.tracers):
        options.append("".join(option_builder))
        return
    
    for char in builder.tracers[len(option_builder)].children.keys():
        if char in tracer.children:
            option_builder.append(char)
            tracer = tracer.children[char]
            get_col_options(builder,options,option_builder,tracer)
            option_builder.pop()
            tracer = tracer.parent
    
    
            
# we assume that the criterion for "largest" is "has the largest area", or largest "r*c"

# one important question to ask here is......can "duplicate" words exist in the rectangle?
# it seems that the most plausible reading of the problem indicates that they can. For ex.
# if the list of words is ["aaaaa"] -- just one word -- then the word rectangle:

#      a a a a a
#      a a a a a
#      a a a a a
#      a a a a a
#      a a a a a

# should be acceptable, given that "every row forms a word reading from left to right"
# and "every column forms a word reading from top to bottom"

# the search space for this problem is STAGGERINGLY large. One way we can imagine doing 
# this is the most brute force way would be to start with a word, then recursively attach
# as a row a next word for EVERY word of the same length, and at each step check if every 
# column is a word in the dictionary, updating the max area of the rectangle any time we 
# hit a valid rectangle, and stopping only once we as many rows as there are letters in 
# the longest word. (Let's call this L)

# This means that we try to search for every permutation of O(N choose L) sets of words
# which is a total of O((NchooseL)!) possiblilites, and the runtime is even greater than 
# that asymptotically because checking for validity itself takes O(L^2) time in and of 
# itself in this approach. 

# Okay, so what is a more efficient way to do it....

# OPTION 1: the word stacker! v1
#
# here is what we are going to try. For every word, we find the biggest word rectangle 
# that we can find (or determine that we cannot find any word rectangle with that word
# at the top) and then replace it with a running max if we find one. Here is how it works:
#
# First off, we are looking for each word (of which there are O(n)) for the BIGGEST word
# rectangle that we can make that starts with that word in the top row. Since we are looking
# at ALL of the words, we are going to look only for word rectangles with heights less than
# or equal to the number of letters in the current letter. Ex. If the first word we try is 
# "funkalicious", which has 12 letters, then we are going to attempt to find word rectangles
# of heights 12,11,10,...,3,2,1 and then when we are working with a smaller word like "fetch"
# with 5 letters, then we do not need to check for heights greater than 5, because if there 
# is one with height 12 like one including a word "funkalicious", as the far left column,
# then we will find it when we look for "funkalicious".
#
#        f u n k a l i c i o u s         f e t c h
#        e                               u
#        t                               n
#        c                               k
#        h                               a
#                                        l
#                                        i
#                                        c
#                                        i
#                                        o
#                                        u
#                                        s
#
# So, once we have started with a word, there has to be a NEXT word of the same length that
# we must try. There are a total of O(n) words that are of the same length, so we can simply
# try to add each one. But when we add it, we need to know if we are working our way to 
# building an actual rectangle. And we can do this with a TRIE. You see, if we for example
# have the word "fetch" on top, we can keep some pointers that point to the f,e,t,c,and h 
# nodes in the trie. Then, when attempt to add the next word "brown", we can check imediately
# whether we are adding on an okay word by seeing if there are nodes below for each node 
# indicating that we are building up to new words. We can do this in O(L) time, 
# where L is the number of characters in the word (and for us to describe the asymptotic 
# behavior, the number of characters in the longest word of the whole list of words) 
# 
# Also, don't forget that we need to check still whether the top word itself alone is a
# valid rectangle, because we need to remember that in a dictionary with words ["abbbab",
# "a", "b"], that "abbbab" itself has every row and column spell out a word. So that top 
# layer requires a check in O(L) time as well. 
#
# How long does it take to get the best rectangle that starts with one word? Well, we
# must try O(n) words for the second spot, and each of those checks takes O(L) time to check, 
# and then for each one of those that works, we must try that many (which is still in O(n))
# below, and so on. From the top, we try n words, and then below that we try n words 
# to layer under that first word, (since we ARE counting duplicates) which takes O(nL)
# time, and then under that we need more which takes O(nL) time....all the way till we 
# hit the bottom of a word. This means that for a single top word, there are O((nL)^L)
# checks we have to make! We know that, obvioulsy, with our checks helping us to rule out
# paths early, and with English language words that are not likely to be so easy to pack 
# up together, we will often see much quicker behavior than if we had highly dense 
# possibilities of words, but asymptotically speaking, it is in O(n*(nL)^L) time.
# This is not too terrible, especially given that we expect L to be relatively low for 
# a dictionary of normal English words, so if we are allowed to assume a constant value 
# for L like 20 or something, this is at least a polynomial algorithm as opposed to the 
# exponential one above that involves all possibilites. 
#
# ...but can we do better?
# as an example, say that the top word is "fetch". if the next word that we try is 
# "abele", then it will fit only if there are words that start with "fa", "eb", "te",
# "cl", and "he" for all five of these. BUT of course, we know that each of those words 
# "fa_____", "eb_____" etc. must all have the same length themselves! If there were a way 
# to look at that, then we could rule out possibilites even more quickly. OR, we could 
# even narrow down our searching to find EXACTLY the right contenders to look for. 

# OPTION 2: the word stacker! v2
#
# in this option, instead of looking through EVERY word to try to fit onto a new level, 
# we look at what the only options are within the trie and then attemt to see if that 
# option is a valid word. 
#
# say that in our trie we do not have only information at each node about what letters 
# come next, but we also have information on, for each letter, how long the words are 
# that lie downward from the tree. So, for example, If the words "vegan","victor","vapid",
# and "vice" are all in the dictionary, then the "v" node will have numbers {4,5,6} as 
# the descriptions of the lengths it has heading downward. We can also imagine that it 
# has some kind of map from "4" to "i" for "vice", "5" to "e" and "a" for "vegan" and "vapid",
# and "6" to "i" for victor. This increases memory requirements somewhat, but we will 
# discuss memory at the end. Ultimately, just one extra dictionary is needed at top
#
# if the top word is "vapid", then rather than iterate through all of the O(n) words that 
# also have 5 letters to see if we can add it on at the end, we need only look through 
# each of the "downward-length" sets for each of the nodes "v", "a", "p", "i", "d", find 
# how many identical lengths hold across ALL of these, and then for each of those lengths, 
# try all of the different possibilities for their belonging in the dictionary itself. 
#
# example, say that the words are ["fetch","abele","fat","ebb","tex","cls","fart","ebony",
# "ten","tend","clue","herd","hendrix","her","tbxsr","eggs","fend"]. When written out, the trie 
# looks like the following:
#
#                                     root
#  a{5}    c{3,4}          e{3,4,5}          f{3,4,5}         h{3,4,7}     t{3,4,5}
#  b{4}    l{2,3}   a{2} b{2,4} g{3}    a{2,3}    e{3,4}      e{2,3,6}     e{2,3} b{4} 
#  e{3}  s{1}  u{2} r{1} b{1}o{3} g{2}  t{1} r{2} n{2} t{3}   r{1,2) n{5}  n{1,2} x{3}
#  l{2}        e{1}          n{2} s{1}       t{1} d{1} c{2}   d{1}   d{4}  d{1}   s{2}
#  e{1}                      y{1}                      h{1}          r{3}         r{1}
#                                                                    i{2}
#                                                                    x{1}
#
# when we consider a word like "fetch", we put it on top, and notice that of all word
# length mappings, which are for f:{3,4,5}, e:{3,4,5}, t:{3,4,5}, c:{3,4}, and h:{3,4,7},
# that the only word lengths that are held in common are 3 and 4. We determine this by 
# simply finding the set intersection of all of these sets. There are a total number of 
# sets as there are letters in the word, which is in O(L), and each set can have as many 
# as O(L) values in it, so this evalutaion takes O(L^2) time. 
#
# we try the greater of these values first, since if we can find a word rectanle that is 
# 5 by 4 then we do not even need to look for one that is 5 by 3--we have found the biggest
# rectangle that starts with "fetch". looking down for each of the options, there are 2 
# letters down from "f" that can lead to a four letter word--"e" for "fend" and "a" for 
# "fart". Then, there is only one for each of the other options--"e" for "eggs", "e" for 
# "tend", "l" for "clue", and "e" for "herd". So, there are a total of two words we need 
# to test--"eeele" and "aeele". Neither of these count as a word which we determine in 
# O(L) time for each by using the trie, or another lookup. So now we must try for 3-letter 
# words. 
#
# For 3 letter words, we have the following options down: 
# from "f": "a" (for "fat")
# from "e": "a" (for "ear"), "b" (for "ebb")
# from "t": "e" (for "ten")
# from "c": "l" (for "cls")
# from "h": "e" (for "herd")
#
# so again, we have two words to try: "aaele" which is not in it, and "abele" which IS. 
# since we did find "abele", we can add it to the row below "fetch" and recursively call
# to explore down from there. 
#
#        f  e  t  c  h
#        a  b  e  l  e
#
# when we think asymptotically about how this works, though, we realize that we run into 
# some problems. Especially at the high level, the total number of words we have to 
# construct and try can be very large....as large as C^L, where C is the number of characters
# and L is the length of the longest word. For instance, if there is a 5 letter word like 
# fetch and it turns out that there are plenty of words that start with f with 4 letters, 
# such as fa__, fe__, fi__, fj__, fl__, fo__, fr__, fu__, and even more if the dicitionary
# has plenty of crossword clue-type words like acronyms and foreign loan words, and expecially
# for vowels that can be followed by nearly any word, we will end up having to try out 
# 26*26*26*26*26 letters, which is in the hundreds of millions of words, which is likely 
# larger than the total number of words in the list of length 5 that we could try out. 
#
# on the other hand, when this number is quite small, such as when we are pretty far down
# the trie on all of the nodes and see that there are hardly any choices left (for instance,
# if the number of choices per spot is not 26,24,26,20,19 where there are 6,165,120 different
# words that can be made, but instead 2,5,2,1,7 where there are only 140) then this is a 
# FAR supeior way to check for words that can next be suitable for the row below. What would 
# be wise is to, whenever we have the candidates ready to deside between, check the total 
# number of combinations that would be required to count up -- which is just the product 
# of the number of next letters for each slot -- against the number of words in the dictionary
# that we have of the same length, and then we compare which is better, because either way 
# we are going to require an O(L) time check to see if this word is even able to go on the 
# next list........
#
# this is because if we pick the first option, where we know that the words are already  
# valid words column-by-column, we must in O(L) time check that each is in the dictionary to 
# make sure that it is valid in a row. And on the other hand, if we pick the second option,
# where we know that the words are already valid words by row (since they are in the
# dictionary already!) we must in O(L) time make sure that each of the words fits on a column
# and would lead to another word in the trie, all of the same length. 

# Since in this problem, we cannot expect to write out the entire thing, I am going to 
# write pseudocode below for the above enhanced algorithm with superior early termination 
# to the version in the book!

# the book version first.......

# create a Trie with all of the words stored ... O(nL) time, O(nL) space
# go ahead and divide the words into groups by length, so length 1, length 2, etc.

# max_size, max_rectangle = an area, and then a list of words 
# for word in list 
#     for c1,c2,c3...all the chars in word
#          see if there is a node down from root,
#          if not, return early with None/0 
#          if yes, get_biggest_rectangle_with_bottom_nodes(all_the_nodes_from_word)   
#     if better than max_size, replace them
# return max_size

# get_biggest_rectangle_with_word_on_top(nodes):
#     for every word of the same length:
#         take all of the c1,c2,c3 chars and see if they branch down from nodes n1,n2,n3... 
#         if there is, get_biggest_rectangle_with_bottom_nodes(n1,n2,n3...) and return top
#         otherwise, pass onwards
#     return top

# ^ there is probably a good way to rearrange it so that the c1,c2,c3 line doesn't get 
# duplicarted. 

# create a Trie with all of the words stored ... O(nL) time, O(nL) space
# go ahead and divide the words into groups by length, so length 1, length 2, etc.

# max_size, max_rectangle = an area, and then a list of words 
# for word in list 
#     get_biggest_rectangle_with_word_on_bottom(all_the_nodes_from_word,0)   
#     if better than max_size, replace them
# return max_size

# get_biggest_rectangle_with_word_on_bottom(nodes):
#     for c1,c2,c3...all the chars in word
#         see if there is a node down from root or nodes, 
#         if there isnt, return 0
#         if there is for all, then     
#              check if we have completed a word and keep track of score
#              for every new_word of the same length:
#              get_biggest_rectangle_with_word_on_bottom(nodes,new_word) and return best score
#         otherwise, pass onwards
#     return best score

# and then my version just requires some extra preprocessing to put the wordlengths in 
# little sets, and then of course to compare whether at this level it is better to try 
# all of the constructable words, or rather to try all words as usual, and keep a memory
# of which ones we tried so there is no doubling down on paths already done.
#

# you can store the words by group size in their own linked lists 
# and use a RECTANGLE object in order to store things better and help 
# with that. REMEMBER for problems like these, using OOP can help even when 
# you are just sketching out pseudocode.
#
# ONE improvement that you did not think of was the order exactly on how to 
# go through them. If the max number of letters in a word was 9, you tried 9*9,
# then 9*8, then 9*7, and so on but did go all the way down to 9*1. Rather, you 
# could have startred at 81, then go to 80 and find for all numbers 1thru9 that 
# multiply to 80, then 79, and so on. This would have ensured that you could 
# IMMEDIATELY return the first rectangle you are able to build, and do not have 
# to keep any other storage. (Though there is still an optimization where you 
# can store versions as you go....but think later about whether it is really 
# more efficient)?
#
# so, REMEMBER that when all you have to do is return "the biggest" or "the longest"
# or so, then try to find a search ordering that has all the candidates in a strict
# order so that you can return the BEST one IMMEDIATELY once you find a valid one.
#
# The other shortcut you thought of went far beyond what was discussed in the
# text so good job on that.
#
# To be more efficient, you also can hold off on building the tries until you 
# need them, for each word length. That way you do have to store more, but you 
# can spend more time being clean about the code. And just keep a "length 9 trie"
# and then "length 8 trie" and so on in an array or something.
