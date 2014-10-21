#!/usr/bin/env python
"""
Constant Supply Class 

"""

__version__ = "0.0.1"
__copyright__ = "Copyright (c) 2011 Bryce Himebaugh. All rights reserved. Additional copyrights may follow."
__license__ = "GPL v3"

from eispice import PyB, Subckt, Circuit, GND, Current, Time, I, V 

class Constant(Subckt): 

    ''' Creates a subcircuit to add constants supplies to the system ''' 
    def __init__(self, eactag, spec):
        if spec[0] == 'I':
            self.__setattr__("I1",I(spec[1],spec[2],spec[3]))
        elif spec[0] == 'V':
            self.__setattr__("V1",V(spec[1],spec[2],spec[3]))
        else: 
            print "Could not resolve constant source type in %s at spec %s"%(eactag, spec)
            exit(0)

if __name__ == '__main__':
    pass
