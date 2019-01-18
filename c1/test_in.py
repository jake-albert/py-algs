import sys
sys.path.append('..')

from data_structs import Stack

def f1():
    bob = Stack()
    bob.push(77)
    bob.display()
    print('done')