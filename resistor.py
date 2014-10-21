#!/usr/bin/env python
"""
Resistor Class 

Handles the border and stray resistors. 

"""

__version__ = "0.0.1"
__copyright__ = "Copyright (c) 2011 Bryce Himebaugh. All rights reserved. Additional copyrights may follow."
__license__ = "GPL v3"

from eispice import PyB, Subckt, Circuit, GND, Current, Time, R, L, C

class Resistor(Subckt): 

    ''' Creates a subcircuit that will connect two areas of the sheet ''' 

    def __init__(self, eactag, spec):
        self.__setattr__("R1",R(spec[0],spec[1],spec[2]))

class BorderResistors(Subckt):  
    
    ''' Creates a subcircuit that includes all of the resistors around the perimeter of the sheet ''' 

    def __init__(self, eactag, sheet_size, r='1k', all_layers=False):

        # If the specification is for high impedance then exit
        if r=="\"Z\"":
            return(None)

        x = sheet_size[0]
        y = sheet_size[1]
        z = sheet_size[2]
  
        # Check to see if a resistor border should be placed on all layers on just on layer z=0
        if all_layers == False:
            z = 1

        r_index = 1
        for z_index in range(z):
            # Top Row
            for x_index in range(x):
                node_name = self.nodename(eactag,(x_index,0,z_index))
                self.__setattr__("R%d"%(r_index),R(node_name,GND,r))
                r_index+=1
            # Right Column
            for y_index in range(y):
                node_name = self.nodename(eactag,((x-1),y_index,z_index))
                self.__setattr__("R%d"%(r_index),R(node_name,GND,r))
                r_index+=1
            # Bottom Row
            for x_index in range(x):
                node_name = self.nodename(eactag,(x_index,(y-1),z_index))
                self.__setattr__("R%d"%(r_index),R(node_name,GND,r))
                r_index+=1
            # Left Column
            for y_index in range(y):
                node_name = self.nodename(eactag,(0,y_index,z_index))
                self.__setattr__("R%d"%(r_index),R(node_name,GND,r))
                r_index+=1
         
    def nodename (self, tag, coordinate):
        return "%s-%d-%d-%d"%(tag,coordinate[0],coordinate[1],coordinate[2])

if __name__ == '__main__':
    pass
