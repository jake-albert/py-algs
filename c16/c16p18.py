# start

# this first aproach seems rather much like a brute-force approach.

# in this problem, we assume that a and b CAN be matched to an empty string. 
# if it could not, it would slightly change the problem, but we are not going to do that.

# With n being the lengh of value and m of pattern, you can safely bound this in
# O(m+n**2/m) but there is likely a much tighter bound that we can make given how 
# quickly the algorithm will time out in many cases. There still might be bugs in it.

# it is late and your brain is mush. just do it over

def f1(pattern,value):
    
    # return error if pattern is empty
    if len(pattern) == 0:
        raise Exception("pattern must contain at least one a or b")
    
    # there is a pattern match for an empty value -- simply make all a's and b's empty
    if len(value) == 0:
        return True

    # preprocess pattern to find the number of a's and b's
    a_count, b_count = 0,0
    for i in range(len(pattern)):
        if pattern[i] == "a":
            a_count += 1
        elif pattern[i] == "b":
            b_count += 1
        else:
            raise Exception("pattern must consist of only a and b")
    
    # one of either a or b is non-zero. Call this one p, and the other q
    if a_count == 0:
        p_count, q_count = b_count, a_count
    else:
        p_count, q_count = a_count, b_count
    
    p_len = 0                   # starting length of the match for p
    p_space = p_len*p_count     # starting total number of chars nedded for all p's
    
    # test for all lengths of the match for p
    while p_space <= len(value):
        
        # find the number of characters that are left to hold all b's
        q_space = len(value) - p_space
    
        # if the current length for a allows for a legal length of b
        if q_count > 0 and q_space % q_count == 0:
            q_len = q_space // q_count
            p_start, q_start = get_start(p_len,q_len,pattern)
            
            #print(p_start,q_start)
            #print("HELLO")            
            
            if verify(p_start,q_start,p_len,q_len,value):
                return True
        
        # handle case where there are no q's in the pattern
        elif q_count == 0 and q_space == 0:
            q_len = 0
            p_start, q_start = get_start(p_len,q_len,pattern)

            if verify(p_start,q_start,p_len,q_len,value):
                return True
        
        # failed match, so increment and update 
        p_len += 1
        p_space = p_len*p_count
    
    return False
            
def get_start(a_len,b_len,pattern):

    a_start, b_start = [], []
    
    # the start of the first match, either a or b, is at index 0
    if pattern[0] == "a":
        a_start.append(0)
        next_index = a_len
    else:
        b_start.append(0)
        next_index = b_len
        
    # iterate through the pattern and add appropriate start points
    for i in range(1,len(pattern)):
        
        # if next one is a, it takes up a_len space
        if pattern[i] == "a":
            a_start.append(next_index)
            next_index += a_len
            
        # if next one is b, it takes up b_len space
        else:
            b_start.append(next_index)
            next_index += b_len
    
    return a_start, b_start
            
def verify(a_start,b_start,a_len,b_len,value):

    #print(a_start,b_start)

    def verify_letter(leng,start,value):
    
        # if there is no a or b in the pattern, will be empty
        if len(start) == 0:
            return True
    
        # test each letter in the match
        for i in range(leng):
        
            # letter to check each time
            correct_letter = value[start[0]]
            start[0] += 1
            
            # go to the proper location in each instance of the pattern
            for j in range(1,len(start)):
                if correct_letter != value[start[j]]:
                    return False
                start[j] += 1
        
        return True
        
    if not verify_letter(a_len,a_start,value):
        return False
    return verify_letter(b_len,b_start,value)
            
            
            
            
            
            
            
            
            
            
            
            
    
    
    
    
    
    
    
    
    
    
    
            
            
            