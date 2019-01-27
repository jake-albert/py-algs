# py-algs  
Author: Jake Albert  
Comprehensive review of algorithms and data structures written and tested on Python 3.7.0.  
Designed for side-by-side viewing of source code and testing in interactive mode in a terminal.   
Acknowledgement: Majority of practice problems sourced from *Cracking the Coding Interview, 6th Edition* ("CCI6") by Gayle Laakman McDowell.

Directory map:  
  * The "data_structs" directory acts as a Python package. It holds my implementations of data structures such as binary search trees, linked lists, tries, etc.
  * The "other_problems" directory holds miscellaneous algorithms problems not from CCI6. They are ordered arbitrarily.
  * Any directory of the form "c{x}" holds my discussion of and solutions to problems from the x-th chapter of CCI6. Filenames in these directories are of the form "c{x}p{y}.py", where y is the number of the problem in that chapter.

Usage:  
  * Clone: `git clone https://github.com/jake-albert/py-algs.git`
  * Test: In a directory containing problems, begin interactive mode in Python 3 and import the file as a module. Solution and testing functions may be accessed as attributes of the module:  
        
        >>> import c16p5
        >>> help(c16p5.f1)
        Help on function f1 in module c16p5:
        
        f1(n)
            Computes the number of trailing zeros in n factorial.  
            
            Args:
                n: A non-negative integer.
                
            Raises:
                ValueError: n is negative.  
         >>> c16p13.f1(28)  
         6  
         >>> c16p13.test()  
         >>>                # Uses assert statements so no output when correct.
      
