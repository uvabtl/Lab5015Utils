#!/usr/bin/env python
import sys
import time
from optparse import OptionParser
from Lab5015_utils import Keithley2231A

mapping = {}
mapping['keithley2231A-1'] = ['CH1']

parser = OptionParser()
parser.add_option("--power", dest="power", default="0")
parser.add_option("--target", dest="target", default="2")
(options, args) = parser.parse_args()

for usb in mapping.keys():
    channels = mapping[usb]
    for ch in channels:
        mykey = Keithley2231A('ASRL/dev/'+usb+'::INSTR', ch)
        
        currV = mykey.meas_V()
        print("current voltage is %.2f V") % currV
        
        if options.power == "1":
            print("ramping up...")
            mykey.set_V(options.target)
            mykey.set_state(1)
            time.sleep(0.5)
            
        elif options.power == "0":
            print("ramping down...")
            mykey.set_V(0.)
            mykey.set_state(1)
            time.sleep(0.5)
        
        else:
            print("doing nothing")
        
        time.sleep(0.5)
        I = mykey.meas_I()
        V = mykey.meas_V()
        print("voltage: %.2f V   current: %.3f A") %(V,I)
