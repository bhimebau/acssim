#!/usr/bin/env python
""" Extended Analog Computer Simulator 

This is the top level simulator model for the distributed Extended Analog Computer simulator (dEACs).
The simulator relies on eispice to generate a reactive mesh and instantiate behavioral models for 
lla circuits. 

The configuration of the interconnects 


"""

__version__ = "0.0.1"
__copyright__ = "Copyright (c) 2011 Bryce Himebaugh. All rights reserved. Additional copyrights may follow."
__license__ = "GPL v3"

from eispice import PyB, Subckt, Circuit, GND, Current, Time, R, L, C, I
from eispice.units import float
from re import compile
from numpy import zeros

# Component Class Imports
from mesh import Mesh
from resistor import Resistor, BorderResistors
from constant import Constant
from lla import LLA
from wave import Wave


class EAC(Subckt):
    '''
    Class that instantiates spice models for the mesh, source, waveform, resistors. 
    ''' 
    def __init__(self, eactag, config=None):
#        self.dump_config(eactag, config)
        sheet_size = eval(config.sheet_size)
        r = config.r
        l = config.l
        c = config.c
        xdim=sheet_size[0]        
        ydim=sheet_size[1]        
        zdim=sheet_size[2]

        # Instantiate the mesh 
        self.__setattr__("%s-ms"%(eactag),Mesh(eactag,xdim,ydim,zdim,r,c,l))

        # Instantiate the border and individual resistors
        self.__setattr__("%s-br"%(eactag),BorderResistors(eactag,sheet_size,config.border))

        for resistor in config.resistors:
            self.__setattr__("%s-%s"%(eactag,resistor),Resistor(eactag,config.resistors[resistor].resspec))    
                       
        # Instantiate the constant sources
        for constant in config.constants:
            self.__setattr__("%s-%s"%(eactag,constant),Constant(eactag,config.constants[constant].constspec))    

        # Instantiate the LLAs 
        for lla in config.llas:
            self.__setattr__("%s-%s"%(eactag,lla),LLA(eactag,config.llas[lla].llaspec))        

        # Instantiate the waveforms 
        for waveform in config.waveforms: 
            self.__setattr__("%s-%s"%(eactag,waveform),Wave(eactag,config.waveforms[waveform].wavespec))        

    def dump_config(self, eactag, config):
        print eactag
        print config.r
        print config.l
        print config.c
        print config.sheet_size
        print config.border
        for lla in config.llas:
            print eactag,lla, config.llas[lla].llaspec
        for constant in config.constants:
            print eactag,constant, config.constants[constant].constspec            
        for waveform in config.waveforms:
            print eactag,waveform,config.waveforms[waveform].wavespec 
        for resistor in config.resistors:
            print eactag,resistor,config.resistors[resistor].resspec        
        
if __name__ == '__main__':
    pass
