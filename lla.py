#!/usr/bin/env python
"""

"""

__version__ = "0.0.1"
__copyright__ = "Copyright (c) 2011 Bryce Himebaugh. All rights reserved. Additional copyrights may follow."
__license__ = "GPL v3"

from eispice import PyB, Subckt, Circuit, GND, Current, Voltage, Time, R, L, C
from eispice.units import float
from re import compile
from types import FunctionType
from tfunc import TFunc

class EispicePort(PyB):

    def __init__(self, eactag, outputtype, innode_pos, innode_neg, function_file, outnode):
        PyB.__init__(self, outnode, GND, outputtype, self.v(innode_pos), self.v(innode_neg), Time)
        self.eactag = eactag
        self.tf = TFunc(function_file) 
 
    def model(self, vP, vN, time):
        output=self.tf.lookup((float(vP)-float(vN)))
        return (output)

class LLA(Subckt):

    def __init__(self, eactag, spec):
        input_type = spec[0]
        iterm_pos = spec[1]
        iterm_neg = spec[2]
        oterm = spec[3]
        func_file = spec[4]
        if input_type == 'I':
            self.__setattr__("R1",R(iterm_pos,GND,'10'))
            self.__setattr__("EIP1",EispicePort(eactag,Current,iterm_pos, iterm_neg, func_file, oterm))
        elif input_type == 'V':
            self.__setattr__("EIP1",EispicePort(eactag,Voltage,iterm_pos, iterm_neg, func_file, oterm))
        else:
            print "Could not determine type of LLA: %s, %s"%(input_type,spec)
            exit(0)
if __name__ == '__main__':
    pass


    

    
