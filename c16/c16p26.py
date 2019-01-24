# start

# so as to avoid parsing the input for longer integers, we accept input in the form 
# of a list of strings--for example, ["2","*","3","+","5","/","6","*","3","+","15"]
# one approach that requires two scans of the array (could also use a linked list)
# would involve going through once and computing mult/divides, replacing empty spots
# with "-1" , and then going through one more time to compute the addition and 
# subtractions. 

# the text does not seem to give any indication of the format of the input, so I could
# also request that the input come in the form of a doubly linked list so that 
# I could do without buffer space for the "-1", discarding sets of 3 nodes at a time

# both ways occur with O(1) extra space requirements beyond the input, and the linked
# list option has the benefit of having possibly fewer nodes to iterate through on 
# the second go. 

# another option that involves using only one pass of the input would be to calculate
# additions/subtractions in the main loop, but to "jump" to a different process to calculate
# the multiplication/divisions and return a result and new index to jump to. 

# we assume that the input is valid in that it is expressed in the reges a(ba)*, where 
# a is some positive integer and b is one of +,-*,/

# this was quite gross. If a value is in the place where an integer should be and is 
# not an integer-able string, then Python will throw an error.

# inputting strings in that form is annoying as shit so I wrote this too.
def to_input(str):

    output = []
    i = 0
    
    while i < len(str):
        
        #print(str[i])
        
        if str[i].isnumeric():
            start = i
            while i < len(str) and str[i].isnumeric():
                i += 1
            output.append(str[start:i])
        
        else:
            output.append(str[i])
            i += 1

    return output
            
def f1(lst):

    if len(lst) == 0:
        raise Exception("Undefined result. Empty expression")
    
    if len(lst) % 2 == 0:
        raise Exception("Improperly formed expression.")
    
    # single number
    if len(lst) == 1:
        return int(lst[0])
    
    # values surrounding the current operator
    running_total = int(lst[0])
    arg = int(lst[2])
    
    # indices of operator and next operator
    op, nop = 1,3
    
    while nop < len(lst):
        
        # if the next operator is a plus or minus, then 
        # regardless of what the current operator is, we can 
        # calculate and move on.
        if lst[nop] == "+" or lst[nop] == "-": 

            running_total = compute(running_total,lst[op],arg)
            op += 2
            arg = int(lst[op+1])
            nop = op + 2
            
        # otherwise, we must prioritize as many of the following 
        # operations as possible that are multiplication or divisions
        else:
        
            while lst[nop] != "+" and lst[nop] != "-":
                
                arg = compute(arg,lst[nop],int(lst[nop+1]))
                nop += 2
                
                # exit condition if last computation is + or /
                if nop >= len(lst):
                    return compute(running_total,lst[op],arg)
            
            running_total = compute(running_total,lst[op],arg)
            op = nop
            nop = op + 2
            arg = int(lst[op+1])
            
    return compute(running_total,lst[op],arg)
 
# helper function 
def compute(v1,op,v2):

    if op == "+":
        return v1 + v2
    elif op == "-":
        return v1 - v2
    elif op == "*":
        return v1 * v2
    elif op == "/":
        return v1 / v2
    else:
        raise Exception("Invalid operator: {}".format(op))
            
def test():

    for str in ["7*89/77-7/6/5+1", \
                "1+1"            , \
                "1*2"            , \
                "2*3+5/6*3+15"   , \
                "2*3+5/6*3/15"   ,
                "1+1+1+2+6"      ,]:
        print(f1(to_input(str)) == eval(str))
       
            
            
            
            
            