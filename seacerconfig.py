#!/usr/bin/env python
"""
Class to parse the input command file into a class to be passed to the spice simulation core. 
"""

__version__ = "0.0.1"
__copyright__ = "Copyright (c) 2011 Bryce Himebaugh. All rights reserved. Additional copyrights may follow."
__license__ = "GPL v3"

import sys
import os
import ConfigParser
import optparse
import re 
from eispiceunits import float
from tfunc import TFunc
from eispice import GND

class ConfigBase: 
    def __init__(self):
        pass

    def replace_value(self, target_list, oldval, newval):
        for index, item in enumerate(target_list):
            if item == oldval:
                target_list[index] = newval
        return target_list


class ConstConfig(ConfigBase):
    """ Constant Voltage or Current Source Configuration
    
    This class is designed to enable the capture of the specification of constant sources that are passed in through "constspec" at instantiation. 

    SXX = [type, positive, negative, value]

    SXX: this will become the label used as the Key to reference this source. 
    type: "V" or "I" - a constant supply can be either control voltage or current. 
    positive - node on the sheet where the positive input of the supply should be connected - this is specified as an x-y tuple such as (2,2) 
    negative - node for the lower reference - this will typically be "GND" but may also be an x-y tuple node specifier similar to positive 
    value - magnitude of the source - this will be passed to eispice so typical spice units should be used. 

    Example: 
    
    S01 = ["I", (3,3), "200u"]

    """
    def __init__(self, constspec):
        self.constspec = eval(constspec)
        self.constspec = self.replace_value(self.constspec,'GND',GND)
        if len(self.constspec) == 4:
            self.type = self.constspec[0]
            self.pos = self.constspec[1]
            self.neg = self.constspec[2]
            self.output_value = self.constspec[3]
        else:
            print "Error: constant supply specification error:", self.constspec

    def value(self):
        return self.output_value
    
class LLAConfig(ConfigBase): 

    def __init__(self, llaspec):
        self.llaspec=eval(llaspec)
        self.llaspec = self.replace_value(self.llaspec,'GND',GND)
        self.type = self.llaspec[0]                          # V or I input, Current output 
        self.pos = self.llaspec[1]                           # Sheet input coordinate of positive terminal
        self.neg = self.llaspec[2]                           # Sheet input coordinate of negative terminal - this can also be "GND"
        self.output_loc = self.llaspec[3]                        # Output coordinate or 'None' if this is a terminal LLA 
        self.transfer_function = TFunc(self.llaspec[4])      # TFunc class that has the parsed transfer fucntion data 

    def value(self, input):
        return self.transfer_function.lookup(input)

class ResistorConfig(ConfigBase): 

    def __init__(self, resspec):
        self.resspec=eval(resspec)                           # Evaluate the resistor spcification because it is a python expression.  
        self.resspec = self.replace_value(self.resspec,'GND',GND)
        self.terminal_a = self.resspec[0]                    # V or I input, Current output 
        self.terminal_b = self.resspec[1]                    # Sheet input coordinate tuple
        self.output = self.resspec[2]                        # Output coordinate or 'None' if this is a terminal LLA 

class WaveformConfig(ConfigBase): 

    def __init__(self,wavespec):
        self.wavespec=eval(wavespec)                          # Evaluate the resistor spcification because it is a python expression.  
        self.wavespec = self.replace_value(self.wavespec,'GND',GND)
        self.type = self.wavespec[0]
        self.output = self.wavespec[1]
        self.transfer_function = TFunc(self.wavespec[2])      # TFunc class that has the parsed transfer function data 
        
    def value(self, input):
        return self.transfer_function.lookup(input)

class EACConfig:
    ''' parses eac config specs provided by the config parser ''' 
    def __init__(self, eacspec):

        # Component configs are held in dicts of objects of the associated type. 
        self.llas = {}
        self.constants = {}
        self.resistors = {}
        self.waveforms = {}

        # Parameters are held as values
        self.sheet_size = (5,5) 
        self.r = '2k'
        self.c = '.001n'
        self.l = '.001p'
        self.border = 'Z'

        self.lla_exp = re.compile("^L[0-9]+")
        self.constant_exp = re.compile("^S[0-9]+")
        self.resistor_exp = re.compile("^R[0-9]+")
        self.waveform_exp = re.compile("^W[0-9]+")
        
        for element in eacspec:
            key = element[0].upper()
            value = element[1]
            if self.lla_exp.match(key):
                self.llas[key] = LLAConfig(value)
            elif self.constant_exp.match(key):
                self.constants[key] = ConstConfig(value)
            elif self.resistor_exp.match(key):
                self.resistors[key] = ResistorConfig(value)
            elif self.waveform_exp.match(key):
                self.waveforms[key] = WaveformConfig(value)
            else:
                if key.upper() == 'RESISTANCE':
                    self.r = value
                elif key.upper() == 'CAPACITANCE':
                    self.c = value 
                elif key.upper() == 'INDUCTANCE':
                    self.l = value
                elif key.upper() == 'DIMENSIONS':
                    self.sheet_size = value
                elif key.upper() == 'BORDER':
                    self.border = value
                else: 
                    print "Could not find key", key, value
                    exit(0)

class SimConfig: 
    def __init__(self, simspec):
        self.step_t = '1n'
        self.sim_t = '100n'
        for element in simspec:
            key = element[0].upper()
            value = element[1]
            if key == 'STEP_T':
                self.step_t = value
            elif key == 'SIM_T':
                self.sim_t = value
            else:
                print "ERROR: Unknown simulation parameter:", element
                exit(0)

class SeacerConfig:
    ''' Class that guides the parsing of the configuration file '''
    def __init__(self, configfile):
        self.eacs = {}
        self.eac_exp = re.compile("^E")
        self.sim_exp = re.compile("^SIM")
        self.configdata = ConfigParser.RawConfigParser()
        self.configdata.read(configfile)
        for s in self.configdata.sections():
            if self.sim_exp.match(s.upper()): 
                self.simconfig = SimConfig(self.configdata.items(s))
            elif self.eac_exp.match(s.upper()):
                self.eacs[s] = EACConfig(self.configdata.items(s)) 
            else:
                print "Parse Error:",configfile,"- unexpected section type:",s
                sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if os.path.exists(sys.argv[1]):    
            commandfile = sys.argv[1]    
        else:
            print "Error: Could not find command file",sys.argv[1]
            print "Usage: seacerconfig.py commandfile"
            exit (1)
    else: 
        print "Error: Wrong number of arguments - should only be one: command file"
        print "Usage: seacerconfig.py commandfile"
        exit (1)

    sp = SeacerConfig(commandfile)
 
    print sp.simconfig.step_t
    print sp.simconfig.sim_t
 
    for eac in sp.eacs.keys():
        print sp.eacs[eac].r
        print sp.eacs[eac].l
        print sp.eacs[eac].c
        print sp.eacs[eac].sheet_size
        print sp.eacs[eac].border

        for lla in sp.eacs[eac].llas:
            print eac,lla, sp.eacs[eac].llas[lla].llaspec
        for constant in sp.eacs[eac].constants:
            print eac,constant, sp.eacs[eac].constants[constant].constspec            
        for waveform in sp.eacs[eac].waveforms:
            print eac,waveform,sp.eacs[eac].waveforms[waveform].wavespec 
        for resistor in sp.eacs[eac].resistors:
            print eac,resistor,sp.eacs[eac].resistors[resistor].resspec 

    
