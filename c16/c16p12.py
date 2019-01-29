# c16p12

# XML Encoding: Since XML is very verbose, you are given a way of encoding it 
# where each tag gets mapped to a pre-defined integer value. The 
# language/grammar is as follows:
#
# Element --> Tag Attributes END Children END
# Attribute --> Tag Value
# END --> 0
# Tag --> some predefined mapping to int
# Value --> string value
#
# For example, the following XML might be converted into the compressed string
# below (assuming a mapping of family -> 1, person ->2, firstName -> 3, 
# lastName -> 4, state-> 5).
#
# <family lastName="McDowell" state="CA">
#   <person firstName="Gayle">Some Message</person>
# </family>
#
# Becomes:
#
# 1 4 McDowell 5 CA 0 2 3 Gayle 0 Some Message 0 0
#
# Write code to print the encoded version of an XML element (passed in Element
# and Attribute objects). 

##############################################################################

# First, given that the input consist of Element and Attribute objects, it is
# necessary to develop classes for these.

# The grammar is somewhat unclear so it would be important to clarify: Can 
# CHILDREN be any number of Elements? Or can CHILDREN also contain Values, 
# such as a string "Some Message"? My implementation assumes that each child 
# in CHILDREN can be only an Element or Attribute instance, or a string.

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

# The below approach works recursively through the grammar and assume that the
# input is either a well-formed Element or a well-formed Attribute instance. 
# It constructs the string by appending its components to a list, then joins
# and prints the resulting string.

class Builder:
    """String builder for encodings."""
    
    def __init__(self):
        """Inits a Builder instance for an empty encoding."""
        self.b = []
    
    def grab(self,st):
        """Adds another string to the encoding."""
        self.b.append(st)
    
    def to_encoding(self):
        """Returns a correctly-spaced encoding string."""
        return " ".join(self.b)

def f1(elem):
    """Prints the encoded version of an XML Element.
    
    Args:
        elem: A well-formed Element or Attribute instance.
    """
    builder = Builder()
    parse_object(elem,builder)
    print(builder.to_encoding())
    
def parse_object(thing,builder):
    """Appends to builder strings that, if joined together with 
    spaces, would form the encoded version of an input XML Element.
    
    Args:
        elem: A well-formed Element or Attribute instance.
        builder: A list.
    """  
    
    # Both Element and Attribute instances are encoded first by their 
    # "tag" attribute. After this, we determine thing's type. If it has
    # a "value" attribute, we treat thing as an Attribute instance. 
    # Otherwise, we treat thing as an Element instance.
        
    builder.grab(str(thing.tag))
    
    try:
    
        builder.grab(thing.value)
    
    except:
    
        for attr in thing.attributes:
            parse_object(attr,builder)
        
        builder.grab("0")
    
        # Each child is either another Element or Attribute instance, 
        # in which case it can be parsed recursively, or it is a 
        # string, in which case it may be grabbed immediately.
    
        for chld in thing.children:
            
            try:
                parse_object(chld,builder)  
            except:
                builder.grab(chld)
        
        builder.grab("0")        

def test():
    """Tests on both an Element and Attribute instance."""  
    input1 = Element("family",                                   \
                     [Attribute("last_name","McDowell"),         \
                      Attribute("state","CA")],                  \
                     [Element("person",                          \
                              [Attribute("first_name","Gayle")], \
                              ["Some Message"])])                 
    
    input2 = Attribute("last_name","Carmichael")
    
    f1(input1)
    f1(input2)