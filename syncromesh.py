#!/usr/bin/env python
"""
SyncroMesh Class

Class that wraps the Mesh class to provide the necessary hooks for particle swarm optimization

"""

__version__ = "0.0.1"
__copyright__ = "Copyright (c) 2011 Bryce Himebaugh. All rights reserved. Additional copyrights may follow."
__license__ = "GPL v3"

from eispice import PyB, Subckt, Circuit, GND, Current, Time, R, L, C
from mesh import Mesh 
import networkx as nx
from eispiceunits import float

class SMLayer():
    
    def __init__(self, meshtag, meshckt, meshcktcnt):
        self.meshtag = meshtag
        self.meshckt = meshckt
        self.meshcktcnt = meshcktcnt

class SyncroMesh():
    
    def __init__(self, layertag='SM', height=1, xdim=5, ydim=5, zdim=1, r='1k', c='1n', l='1p'):
        self.system_circuit = Circuit("SyncroMesh for PSO")
        self.layertag = layertag
        self.height = height
        self.xdim = xdim
        self.ydim = ydim 
        self.zdim = zdim 
        self.r = r
        self.c = c 
        self.l = l

        self.stack = []

        for layer in range(height):
            meshtag = "%s%d"%(self.layertag,layer)
            mckt = Mesh(meshtag,self.xdim,self.ydim,self.zdim,self.r,self.c,self.l)
            layer = SMLayer(meshtag, mckt, mckt.subcktCnt)
            self.stack.append(layer)
            self.system_circuit.__setattr__(meshtag,mckt)

        self.graph = nx.generators.classic.grid_graph([self.xdim,self.ydim,self.zdim])
        self.groups = self.report_groups()
        
    def report_devices(self):
        self.system_circuit.devices()

    def report_resistors(self): 
        resistors = []
        layers = self.report_layers()
        for index in range(len(layers)):
            for edge in self.graph.edges():
                n1 = self.node_name(layers[index], edge[0])
                n2 = self.node_name(layers[index], edge[1])
                resistors.append("%d#%s-%s"%(index,n1,n2))
        return resistors

    def report_groups(self):
        groups = {}
        layers = self.report_layers()
        for edge in self.graph.edges():
            tag = "G-%d-%d-%d-G-%d-%d-%d"%(edge[0][0],edge[0][1],edge[0][2],edge[1][0],edge[1][1],edge[1][2])
            groups[tag] = []
            for index in range(len(layers)):
                n1 = self.node_name(layers[index], edge[0])
                n2 = self.node_name(layers[index], edge[1])
                groups[tag].append("%d#%s-%s"%(index,n1,n2))
        return groups

    def change_group_resistance(self, group, value):
        resistors = self.groups[group] 
        for resistor in resistors:
            self.change_resistor_pair(resistor, value)
    
    def node_name(self, layer, node):
        return "%s-%d-%d-%d"%(layer,node[0],node[1],node[2])

    def report_layers(self):
        meshtag_list = []
        for layer in self.stack:
            meshtag_list.append(layer.meshtag)
        return (meshtag_list)

    def run_op(self):
        self.system_circuit.op()

    def change_all_resistors(self, value):
        resistors = self.report_resistors()
        for resistor in resistors:
            self.change_resistor_pair(resistor, value)

    def change_resistor_pair(self, resistor, combined_value):
        value = float(combined_value)/2.0
        self.change_resistor("%s-R1"%(resistor),value)
        self.change_resistor("%s-R2"%(resistor),value)

    def change_resistor(self, resistor, value):
        self.system_circuit.__getattribute__(resistor).R = float(value)

    def change_resistor_sync(self, resistor, value):
        pass

if __name__ == '__main__':
    sm = SyncroMesh(height=8, xdim=10, ydim=10, zdim=1) 
    sm.change_group_resistance("G-7-3-0-G-7-4-0", '45k')
    sm.report_devices()

