# c16p18

# Pattern Matching: You are given two strings, pattern and value. The pattern
# string consists of just the letters "a" and "b", describing a pattern within
# a string. For example, the string "catcatgocatgo" matches the pattern 
# "aabab" (where "cat" is "a" and "go" is "b"). It also matches patterns like 
# "a", "ab", and "b". Write a method to determine if value matches pattern. 

##############################################################################

# A question to clarify is whether "a" and "b" can be the empty string. For 
# example, we know that the string "catcat" matches the pattern "aa" and 
# "bb", but can it also match "aab" or "aabbbbbbbbbbb"? My below function
# assumes that the answer is YES.

# On a trivial case where pattern contains only one letter, the below function
# returns the result in O(P+V) time, and in non-trivial cases in O(N^2) time, 
# where P is the length of pattern, V is the length of value, and N is P+V.

# There are a few minor possible optimizations to revisit here. For example, 
# I iterate through possible lengths for "a", calling the expensive verify()
# function each time that an "a" length allows for a possible "b" length, but
# when there are fewer "a"s than "b"s in the pattern, this results in more 
# calls to verify() than if I were to work the other way, checking lengths for
# "b" and retroactively fitting "a" to match. Determining the maximum of 
# a_count and b_count would result in minimizing calls to verify() which might 
# improve runtime significantly on certain inputs. (Ex. when pattern is 
# "abbbbbbbbbbbbba" and value is very long.) That verify() exits as early as
# possible on False inputs mitigates the damage of not implementing this, but
# I would still be curious to see the effect it has.

def f1(pat,val):
    """Determines if a value matches a pattern.
    
    Args:
        pat: A string of "a"s and "b" in any order.
        val: A string.
        
    Returns:
        A Boolean.
        
    Raises:
        ValueError: pat is empty or improperly formed.
    """
    
    # No value matches an empty pattern, but an empty value matches any 
    # non-empty pattern; "a" and "b" are simply the empty string.
    
    if len(pat) == 0:
        raise ValueError("Pattern must contain at least one a or b.")
    
    if len(val) == 0:
        return True

    a_count, b_count = pattern_count(pat)
    
    # When there are only "a"'s or only "b"'s in pattern, we can 
    # determine how long the match for that one letter must be and 
    # check with one call to verify(). Total runtime in O(P+V).

    if a_count == 0:
        return len(val) % b_count == 0 and \
               verify(pat,val,0,len(val)//b_count)
    
    if b_count == 0: 
        return len(val) % a_count == 0 and \
               verify(pat,val,len(val)//a_count,0)
    
    # But when pattern holds at least one "a" and one "b", we must test 
    # various lengths for the matches. For each candidate length for 
    # the "a" match, determine the number of characters that would be 
    # taken up by all matches to "a" and thus how many characters would
    # remain to hold all matches to "b". Check only if this number of 
    # characters is divided evenly by the number of instances of "b". 
    
    a_len = 0                       
    while True:
    
        a_space = a_len*a_count     
        if a_space > len(val):
            return False
        
        b_space = len(val) - a_space
        if b_space % b_count == 0 and verify(pat,val,a_len,b_space//b_count):
            return True
        a_len += 1
    
def pattern_count(pat):
    """Returns the total counts "a" and "b" in a string.
    
    Args:
        pat: A string.
    
    Returns:
        A tuple of ints.
    
    Raises:
        ValueError: pat contains characters other than "a" or "b".
    """
    a_count, b_count = 0,0
    for i in range(len(pat)):
        if pat[i] == "a":
            a_count += 1
        elif pat[i] == "b":
            b_count += 1
        else:
            raise ValueError("Invalid input: char not a or b in pattern.")
    
    return a_count, b_count
 
class Matcher:
    """A class that facilitates matching one pattern of set length.
    
    Attributes:
        leng: An int. The length of the pattern.
        val: A string possibly containing instances of the pattern.
        start: An int. The index to the start of the first correct
          instance of the pattern in a val.
    """
    
    def __init__(self,leng,val):
        """Inits a Matcher instance that will attempt to match some 
        pattern of length leng in string value."""
        self.leng = leng
        self.val = val
        self.start = None
 
    def match_word(self,i):
        """Returns True if an instance of the pattern begins at index i,
        and False otherwise."""
        
        # If the pattern has not yet been established, treat i as the
        # first correct appearance of the pattern, and store it for
        # reference. Otherwise, check the characters beginning at i 
        # against the correct characters at the start index. 
        
        if self.start is None:
            self.start = i
            return True
    
        for j in range(self.leng):
            if self.val[i+j] != self.val[self.start+j]:
                return False
        return True

def verify(pat,val,a_len,b_len):
    """Returns whether or not the first (a_len*a_count)+(b_len*b_count)
    characters of value match pattern, when a is assumed to be a_len 
    characters long and b b_len.
    
    Args:
        pat: A string of only "a" and "b".
        val: A string.
        a_len, b_len: Positive ints. 
    
    Returns:
        A Boolean.
        
    Raises:
        IndexError: val has less than (a_len*a_count)+(b_len*b_count)
        characters.
    """
    a_matcher, b_matcher = Matcher(a_len,val), Matcher(b_len,val)

    # For each "a" and "b" in pattern, attempt to match a substring of 
    # the appropriate length in value, advancing a read head each time.
    
    val_reader = 0
    for x in pat:
        
        if x == "a":
            matched = a_matcher.match_word(val_reader)
            val_reader += a_len
        else:
            matched = b_matcher.match_word(val_reader)
            val_reader += b_len
            
        if not matched:
            return False
   
    return True    
    
def test():
    """Tests a wide variety of cases. Still, not exhaustive."""
    true_inputs = [("abbbabba",""),             # a:"", b:"".
              
                  ("aaa","catscatscats"),       # a:"cats", b: undefined.
                  ("aaab","catscatscats"),      # a:"cats", b:"".
                  
                  ("bbb","txtxtx"),             # a: undefined, b:"tx".
                  ("abbbaaaaaaaa", "txtxtx"),   # a:"", b"tx"
                  
                  ("abbab","gocatcatgocat"),    # a:"go", b:"cat"
                  ("aabab","catcatgocatgo"),    # a:"cat", b:"go"
                  ("a","catcatgocatgo"),        # a: full string.
                  ("b","catcatgocatgo"),        # b: full string.
                  ("ab","catcatgocatgo")]       # Several matches.
                  
    false_inputs =[("aaa","catscatsRats"),      # Even divide but wrong char.
                   ("aaa","catscatscat"),       # No even divide.
                  
                   ("bbb","txtxtX"),            # Even divide but wrong char.
                   ("bbb","txtxt"),             # No even divide.
                  
                   ("abbab","gocatRatgocat"),   
                   ("abbab","gocatcatgoca"),    
                   ("abbab","gocatcatgocatS")]
                  
    for input in true_inputs:
        assert f1(*input)
    for input in false_inputs:
        assert not f1(*input)