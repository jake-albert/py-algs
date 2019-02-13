# c17p26

# Sparse Similarity: The similarity of two documents (each with distinct 
# words) is defined to be the size of the intersection divided by the size of
# the union. For example, if the documents consist of integers, the 
# similarity of {1,5,3} and {1,7,2,3} is 0.4, because the intersection has
# size 2 and the union has size 5.
#
# We have a long list of documents (with distinct values and each with an
# associated ID) where the similarity is believed to be "sparse:' That is, any
# two arbitrarily selected documents are very likely to have similarity 0. 
# Design an algorithm that returns a list of pairs of document IDs and the 
# associated similarity.
#
# Print only the pairs with similarity greater than 0. Empty documents should
# not be printed at all. For simplicity, you may assume each document is
# represented as an array of distinct integers.
#
# EXAMPLE
# Input:
# 13: {14, 15, 100, 9, 3}
# 16: {32, 1, 9, 3, 5}
# 19: {15, 29, 2, 6, 8, 7}
# 24: {7, 10}
# Output:
# IDl, ID2  : SIMILARITY
#  13,  19  : 0.1
#  13,  16  : 0.25
#  19,  24  : 0.14285714285714285

##############################################################################

# Say that N is the number of documents, and W is the number of unique words 
# in the document (in other words, the maximum number of words that can be in 
# any one document). The simplest way to calculate the similarities is to, for
# all O(N^2) pairs of documents, calculate their similarities from scratch and
# output iff non-zero. Altogether takes O(W*N^2) time.  

# When calculating similarity just between TWO documents, we find the
# intersection by iterating through one document and checking for membership 
# in the other. For example, say we have two sets representing documents: 

# S1  {14,15,100,9,3)
# S2  {32,1,9,3,5}

# We iterate over S1 and check if each value is in S2. For each match, then we
# add ONE to the intersection score. Once we have the intersection, we can
# find the union in constant time. It is just the size of S1 plus the size of
# S2 minus the size of the intersection.

# For example: 14 in S2? NO. 15? NO. 100? NO. 9? YES. 3? YES. So intersection
# is 2, union is 5+5-2 or 8, and thus similarity is 0.25. If the intersection
# had been 0, we can immediately skip the union and division calculations and 
# move on.

# It seems, then, that calculating the intersections is the "bottleneck" of 
# this problem, and that storing extra information can help do it faster.

# My function below creates two extra dictionaries: the first is a "reverse"
# dictionary of the input that maps word ids to a list of documents that 
# contain that word. This takes O(W*N) time to create and requires that much
# space as well. 

# Simultaneously, it creates a dictionary that maps unique pairs of documents
# to first the intersection between those two documents. It adds 1 to the 
# intersection of a pair of docs in this dictionary iff while creating the 
# first dictionary, it finds an instance of a word in some document that has 
# already been seen in at least one other document. Entries in this dictionary
# are not created until an intersection of at least 1 is found.

# (After this preprocessing is done, we can divide an intersection score by 
# the union in O(1) time as before and return.)

# For example, say that when we read word #47 from doc #21 and see in the 
# first dictionary that word #47 has already been found in docs #3 and #18.
# Checking in the second dictionary, we find that no similarity has been 
# found yet for (3,21), so we add it to the second dictionary with "1" as the
# value. We then see that (18,21) is already stored in the dictionary with
# similarity 3, so we increment it by 1 to 4.

# In an input where similarities exist between every document, the total 
# number of pairs of docs that are in this second dictionary is in O(N^2), 
# but we are assuming that similarities are sparse. Say that of these O(N^2) 
# pairs, only a smaller number S have similarity > 0. The size of the second
# dictionary is thus O(S), and total space requirements are O(W*N+S). 

# Total runtime is from:
#
#     - Reading every unique instance of a word in all documents to create the 
#       first dictionary, which is in O(W*N).
#     - Calculating all intersection scores. We do this by incrementing each 
#       intersection score from 0 to its actual value by 1 each time we see a
#       hit where unique word instances match. This runtime thus is the same
#       complexity as the sum of all intersection scores. Say that the most 
#       frequent word appears in F documents. The contribution to the sum of 
#       intersection scores from that word alone is in O(F^2), so the sum 
#       from all words is in O(W*F^2).
#     - Calculating the similarities for each pair of docs from their 
#       intersections, which is in O(S) time. 

# So total time requirements are O((W*N)+(W*F^2)+(S)). The 1st and 3rd terms
# seem to be the best runtime we can conceivably imagine to read the input and
# print the output. The middle term also improves on the original approach 
# whose complexity is O(W*N^2), since F must be smaller than N in order for 
# any two arbitrarily selected documents to very likely have similarity of 0.  

class Dictionaries:
    """Class maintains three dictionaries used to find the solution.
    
    Attributes:
        doc_to_words: A dictionary that maps int doc ids to int word
          ids of all words appearing in the doc. Problem input.
        word_to_docs: A dictionary that maps int word ids to int doc 
           ids of all docs where those words appear.
        pair_to_sim: A dictionary mapping tuples of doc ids to float 
           similarity scores, only for pairs with non-zero similarity.
    """
    
    def __init__(self,doc_to_words):
        """Inits a new collection of dictionaries."""
        self.doc_to_words = doc_to_words   
        self.word_to_docs = {}      
        self.pair_to_sim = {}       
        
def f1(doc_to_words,verbose=False):
    """Calculates similarities between pairs of documents.
    
    Args:
        doc_to_words: A dictionary mapping doc ids to word ids.
        verbose: A Boolean. 
    
    Returns:
        A list of doc pairs and their similarities for all pairs with
        non-zero similarity. If verbose is True, pretty prints output.
    """
    dicts = Dictionaries(doc_to_words)        
    for doc,words in dicts.doc_to_words.items():
        for word in words:
            process_word(word,doc,dicts)    
    calculate_sims(dicts)
    
    if verbose:
        pretty_print(dicts.pair_to_sim)
    else:
        return list(dicts.pair_to_sim.items())

def process_word(word,doc,dicts):
    """Updates dictionaries over a specific word instance in a doc.
    
    Args:
        word: An int word id.
        doc: An int doc id. The doc in which word appeared.
        dicts: A Dictionaries instance.
    """
    
    # This word instance is either the first instance of the word that 
    # has been found, in which there is no change to any pairs' 
    # similarity, or it is not, in which the intersection score of 
    # every document seen so far with that word increases by one.
    
    if word not in dicts.word_to_docs:
        dicts.word_to_docs[word] = [doc]
    else:
        for other_doc in dicts.word_to_docs[word]:
            pair = (doc,other_doc) if doc < other_doc else (other_doc,doc)
            if pair not in dicts.pair_to_sim:
                dicts.pair_to_sim[pair] = 1
            else:
                dicts.pair_to_sim[pair] += 1
                
def calculate_sims(dicts):
    """Calculates similarities from intersections.
    
    Assuming that the pair_to_sim dictionary contains all non-zero 
    intersections between all pairs of docs, derives the union between 
    each pair and divides.
    
    Args:
        dicts: A Dictionaries instance.
    """
    for (doc1,doc2),inter in dicts.pair_to_sim.items():
        union = len(dicts.doc_to_words[doc1]) + \
                len(dicts.doc_to_words[doc2]) - \
                inter
        dicts.pair_to_sim[(doc1,doc2)] /= union

def pretty_print(pair_to_sim):
    """Sorts pairs of docs and prints for easy reading."""
    if len(pair_to_sim) == 0:
        print("No non-zero similarities.")
    print("ID1  ID2  : SIMILARITY\n----------------------------")
    for (doc1,doc2),sim in sorted(pair_to_sim.items()):
        print(f" {doc1},  {doc2}  : {sim}")
 
def test():
    """Tests the sample input."""
    input =  {13: [14,15,100,9,3,],        \
              16: [32,1,9,3,5],            \
              19: [15,29,2,6,8,7],         \
              24: [7,10]          }
    
    f1(input,True)