#!/usr/bin/env python
"""
Mesh Class

Returns a subcircuit that with the circuit mesh. 

"""

__version__ = "0.0.1"
__copyright__ = "Copyright (c) 2011 Bryce Himebaugh. All rights reserved. Additional copyrights may follow."
__license__ = "GPL v3"

from eispice import PyB, Subckt, Circuit, GND, Current, Time, R, L, C
import networkx as nx

class Mesh(Subckt):
    '''  Builds a regular mesh of RLC components ''' 
    def __init__(self, eactag, xdim=5, ydim=5, zdim=1, r='1k', c='1n', l='1p'):
        self.__dict__['xdim'] = xdim
        self.__dict__['ydim'] = ydim
        self.__dict__['zdim'] = zdim
        self.__dict__['r'] = r
        self.__dict__['c'] = c
        self.__dict__['l'] = l
        self.__dict__['eactag'] = eactag
        self.__dict__['graph'] = nx.generators.classic.grid_graph([self.__dict__['xdim'], self.__dict__['ydim'], self.__dict__['zdim']])
        self.__dict__['int_node_cnt'] = 0

#        for current_edge in self.graph.edges():
#            self.graph.edge[current_edge[0]][current_edge[1]]['value'] = '10k'
            
#        for current_edge in self.graph.edges():
#            print self.graph.edge[current_edge[0]][current_edge[1]]['value']
     
        self.generate_graph(eactag, r, c, l)

    def generate_graph(self, eactag, r, c, l):            
        for node in self.graph.nodes():
            n1 = self.create_label(eactag,node)
            self.__setattr__("%s-C1"%(n1),C(n1,GND,c))

        for edge in self.graph.edges():
            n1 = self.create_label(eactag,edge[0])
            n2 = self.create_label(eactag,edge[1])
            self.__setattr__("%s-%s-R1"%(n1,n2),R(n1,self.next_node(),r))
            self.__setattr__("%s-%s-L1"%(n1,n2),L(self.current_node(),self.next_node(),l))
            self.__setattr__("%s-%s-R2"%(n1,n2),R(self.current_node(),n2,r))

    def current_node(self):
        return(self.node(self.int_node_cnt))

    def next_node(self):
        self.int_node_cnt = self.int_node_cnt + 1
        return(self.node(self.int_node_cnt))

    def create_label(self, eactag, node):
        return ("%s-%d-%d-%d"%(eactag,node[0],node[1],node[2]))
    
if __name__ == '__main__':
    print "Mesh Test Util"
    eac = Circuit("Simple EAC Mesh Test") 
    m = Mesh("E1",10,10,3,'10k')
    eac.__setattr__("Mesh 1", m)
    n = Mesh("E2",3,3,1,'10k')
    eac.__setattr__("Mesh 2",n)
    print eac.title
    print eac.devices()

