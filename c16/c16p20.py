# start

# the first attempt uses a specially-designed Trie that stores words acccording to 
# their T9 encoding (and within any order within that categorization).

# insert and retrieval both are in O(n) time, where n is the legnth of the word being
# inserted or the pattern being retrieved. If we wanted the eligible words sorted in 
# any particular order, we could insert them into some tree or something which would 
# still be faster. For this type of use case in which we are working with generally 
# short strings (as we do not type in more than 15-long words normally)

class T9TrieNode:

    def __init__(self):
        self.children = [None] * 8   # 'abc', 'def', ...
        self.null     = set()        # list of words with T9 encoding signified by path 
        
    def insert(self,word):
        if len(word) > 0:            # do nothing on empty string
            self._insert(word.lower(),0)
            
    def _insert(self,word,i):
        if i == len(word):
            self.null.add(word)   # words are kept in insertion order 
        else:
            c = word[i]              # current char
            for ind,b in enumerate([("a","c"),("d","f"),("g","i"),("j","l"),   \
                                    ("m","o"),("p","s"),("t","v"),("w","z")]):
                if b[0] <= c <= b[1]:
                    self._ensure_child(ind)
                    self.children[ind]._insert(word,i+1)
                    return
            raise Exception("Illegal character: {}".format(c))
    
    def _ensure_child(self,x):
        if self.children[x] is None:
            self.children[x] = T9TrieNode()
   
    def retrieve(self,seq):
        seq = str(seq)
        if len(seq) == 0:             # empty sequence returns empty list
            return []
        return self._retrieve(seq,0)
        
    def _retrieve(self,seq,i):
        if i == len(seq):
            return self.null          # ensure that users know NOT to change this
        dig = seq[i]                  # digit in string form
        
        if "2" <= dig and dig <= "9": # legal keys to press
            index = int(dig) - 2
            if self.children[index] is None:
                return []
            return self.children[index]._retrieve(seq,i+1)
        else:
            raise Exception("Illegal key entered: {}".format(dig))
    
# when we think about the benefit to having it stored in a trie, though, there isn't really
# one unless we are ever going to want to traverse through the words in some order. Another
# approach involves converting each new word to a code in O(n) time, and then hashing it 
# to a list that we can retrieve in O(1) time.

class T9HashTable:

    def __init__(self):
        self.table = {}
        self.mapping = {"a": 2, "b": 2, "c": 2, \
                        "d": 3, "e": 3, "f": 3, \
                        "g": 4, "h": 4, "i": 4, \
                        "j": 5, "k": 5, "l": 5, \
                        "m": 6, "m": 6, "o": 6, \
                        "p": 7, "q": 7, "r": 7, "s": 7, \
                        "t": 8, "u": 8, "v": 8, \
                        "w": 9, "x": 9, "y": 9, "z": 9}
                        
    def insert(self,word):
        code_builder = []
        word = word.lower()
        
        # generate code
        for i in range(len(word)):
            
            c = word[i] 
            if c in self.mapping:
                code_builder.append(str(self.mapping[c]))
            else:
                raise Exception("Illegal character: {}".format(c))
    
        code = "".join(code_builder)
        if code in self.table:
            self.table[code].append(word)
        else:
            self.table[code] = [word]
     
    # no need to check for correct input as this would actually take O(n) time
    def retrieve(self,code):
        code = str(code)
        
        if code in self.table:
            return self.table[code]
        else:
            return []
    
    
    
    
    
    
    
    
    
    
    
            