#!/usr/bin/env python
"""
Main File for the seacer system. 

"""
__version__ = "0.0.1"
__copyright__ = "Copyright (c) 2011 Bryce Himebaugh. All rights reserved. Additional copyrights may follow."
__license__ = "GPL v3"

import sys
import os

from seacerconfig import SeacerConfig
from eispice import Circuit
from eac import EAC

class Seacer():
    def __init__(self,commandfile):
        if os.path.exists(commandfile):    
            self.commandfile = commandfile
        else:
            print "Error: Could not find command file",commandfile
            exit(1)
        self.configuration = SeacerConfig(commandfile)
        self.system_circuit = Circuit("System of EACs defined by command file") 
        for eac in self.configuration.eacs.keys():
            self.system_circuit.__setattr__(eac,EAC(eac,self.configuration.eacs[eac]))

    def report(self):
        self.system_circuit.devices()
        print "about to print keys"
        for key in self.system_circuit.__dict__.keys():
            print key
        print "done printing keys"
#        print self.system_circuit.__getattribute__('23#R8')
 #       print self.system_circuit.__getattribute__('23#R8').R
  #      self.system_circuit.__getattribute__('23#R8').R = 20.0
   #     print self.system_circuit.__getattribute__('23#R8').R

        
    def evaluate(self):
        self.system_circuit.tran(self.configuration.simconfig.step_t,self.configuration.simconfig.sim_t)

    def node_voltage(self, node, time):
        return self.system_circuit.v[node](time)
    
    def mesh_voltage(self, eac, time):
        mesh_dimensions = eval(self.configuration.eacs[eac].sheet_size)
        xrange = mesh_dimensions[0]
        yrange = mesh_dimensions[1]
        zrange = mesh_dimensions[2]
        mesh = []
        for z in range(zrange):
            sheet = []
            for y in range(yrange):
                row = []
                for x in range(xrange):
                    node = self.node_name(eac,x,y,z)
                    voltage = self.node_voltage(node, time)
                    row.append(voltage)
                sheet.append(row)
            mesh.append(sheet)
        return(mesh)

    def node_name(self, eac, x, y, z):
        return "%s-%d-%d-%d"%(eac,x,y,z)
        
if __name__ == '__main__':
    s = Seacer('bessel_constant.cfg')
    s.evaluate()
    meshv = s.mesh_voltage("E1","2n")
    sheet = meshv[0]
    print sheet 
    
