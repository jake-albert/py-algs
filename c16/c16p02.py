# c16p2

# Word Frequencies: Design a method to find the frequency of occurrences of 
# any given word in a book. What if we were running this algorithm multiple 
# times? 

##############################################################################

# (Discussion only for this problem.)

# It is important first that there be a consistent definition of word
# boundaries and caps-sensitivity for the book. Assuming that such a 
# definition has been agreed on and that the book has been parsed once 
# according to these rules, we may consider the "book" as a list of numbers,
# where each number corresponds to a unique word. 

# If we were running this only ONCE for a single word, then we need to store 
# only one variable, a count value, and iterate through the words of the book 
# while incrementing. This would require O(1) space and O(N) time in the 
# number of words of the book.

# On the other hand, if we were going to run this multiple times, then it
# would be better to maintain a dictionary of words to count value. If the 
# book is guaranteed not to change, then the first time we call the function
# we build the dictionary and return the desired value in O(N) time. Then for 
# all subsequent times we call it, we simply return a value from the 
# dictionary in O(1) time.