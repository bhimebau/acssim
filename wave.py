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
from wfunc import WFunc

class WavePort(PyB):

    def __init__(self, eactag, outputtype, function_file, outnode):
        PyB.__init__(self, outnode, GND, outputtype, Time)
        self.eactag = eactag
        self.wf = WFunc(function_file) 
 
    def model(self, time):
        output=self.wf.lookup(float(time))
        return (output)

class Wave(Subckt):

    def __init__(self, eactag, spec):
        output_type = spec[0]
        oterm = spec[1]
        func_file = spec[2]
        if output_type == 'I':
            self.__setattr__("WIP1",WavePort(eactag,Current,func_file, oterm))
        elif output_type == 'V':
            self.__setattr__("WVP1",WavePort(eactag,Voltage,func_file, oterm))
        else:
            print "Could not determine type of Waveform: %s, %s"%(input_type,spec)

if __name__ == '__main__':
    pass


    

    
