#!/usr/bin/env python
"""
Bessel Function Demonstation 
"""
__version__ = "0.0.1"
__copyright__ = "Copyright (c) 2011 Bryce Himebaugh. All rights reserved. Additional copyrights may follow."
__license__ = "GPL v3"

from seacer import Seacer 
from scipy.io import savemat

if __name__ == '__main__':
    bc = Seacer('bessel.cfg')
    bc.report()
    bc.evaluate()

    # Select the Sheet and instant in time
    time = "5u"
    eacs = ["E1","E2","E3","E4"]
    data = {} 
    for eac in eacs:
        meshv = bc.mesh_voltage(eac,time)
        sheet = meshv[0]
        data[eac] = sheet

    # Write out the matlab file
    savemat("bessel",data)



