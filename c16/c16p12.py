# c16p12

# XML Encoding: Since XML is very verbose, you are given a way of encoding it 
# where each tag gets mapped to a pre-defined integer value. The 
# language/grammar is as follows:
#
# Element --> Tag Attributes END Children END
# Attribute --> Tag Value
# END --> e
# Tag --> some predefined mapping to int
# Value --> string value
#
# For example, the following XML might be converted into the compressed string
# below (assuming a mapping of family -> 1, person ->2, firstName -> 3, 
# lastName -> 4, state-> 5).
#
# <family lastName="McDowell" state="CA">
# <person firstName="Gayle">Some Message</person>
# </family>
# Becomes:
# 1 4 McDowell 5 CA e 2 3 Gayle 0 Some Message e e
#
# Write code to print the encoded version of an XML element (passed in Element
# and Attribute objects). 

##############################################################################

# First, given that the input are Element objects, it is helpful to develop 
# classes for these. (I assume for this problem that the input can be only 
# instances of the Element class, not of the Attribute class.)

# The grammar is somewhat unclear so it would be important to clarify: Can 
# CHILDREN be any number of Elements? Or can CHILDREN also contain Values, 
# such as a string "some message"? My implementation puts no restrictions
# on what kinds of objects can be CHILDREN.

# I use the mapping from the example in the problem description:

mapping = {"family":     1,
           "person":     2,
           "first_name": 3,
           "last_name":  4,
           "state":      5}

class Element:
    """An Element as defined in the grammar.
    
    Attributes:
        tag: An integer representing some word.
        attributes: A list of Attribute instances.
        children: A list of Attribute instances and strings.
    """ 
    
    def __init__(self,tag,attributes=None,children=None):
        """Inits Element with tag and optional attributes, children.""" 
        self.tag = mapping[tag]
        if attributes is None:
            self.attributes = []
        else:
            self.attributes = attributes
        if children is None:
            self.children = []
        else:
            self.children = children
    
class Attribute:
    """An Attribute as defined in the grammar.
    
    Attributes:
        tag: An integer representing some word.
        value: A string.
    """
    
    def __init__(self,tag,value):
        """Inits Attribute with tag and value."""
        self.tag = mapping[tag]
        self.value = value

# The first approach works recursively through the grammar and assume that the
# Element is well-formed. It constructs the string by appending its components
# to a list, then joins and prints this list at the end.

def f1(elem):
    """Prints the encoded version of an XML Element.
    
    Args:
        elem: A well-formed Element instance.
    """
    builder = []
    print_elem(elem,builder)
    print(" ".join(builder))
    
def print_elem(elem,builder):
    """Appends to builder strings that, if joined together with 
    spaces, would form the encoded version of an input XML Element.
    
    Args:
        elem: A well-formed Element instance.
        builder: A list.
    """  
    builder.append(str(elem.tag))
    for attr in elem.attributes:
        builder.append(str(attr.tag))
        builder.append(attr.value)
    builder.append("0")
    for chld in elem.children:
        try:                          # Child could be an element object.
            print_elem(chld,builder)  
        except:                       # Alternatively, child could be string.
            builder.append(chld)           
    builder.append("0")
    
def test():
    """Tests the (non-exhaustive) example from the problem description.
    """  
    input1 = Element("family",                                   \
                     [Attribute("last_name","McDowell"),         \
                      Attribute("state","CA")],                  \
                     [Element("person",                          \
                              [Attribute("first_name","Gayle")], \
                              ["Some Message"])])                 
    
    f1(input1)