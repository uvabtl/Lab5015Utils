#!/usr/bin/env python
import sys
import time
from optparse import OptionParser
from Lab5015_utils import Keithley2231A

parser = OptionParser()
parser.add_option("--power", dest="power", default="0")
parser.add_option("--target", dest="target", default="47")
parser.add_option("--combine-ps", dest="combinePS", default="0", help="combine two different power supplies")
(options, args) = parser.parse_args()


if options.combinePS == '1':
    
    mapping = {}
    mapping['keithley2231A-0'] = ['CH1']
    mapping['keithley2231A-1'] = ['CH1']
    
    it = 0
    for usb in mapping.keys():
        channels = mapping[usb]
        for ch in channels:
            mykey = Keithley2231A('ASRL/dev/'+usb+'::INSTR', ch)
            
            currV = mykey.meas_V()
            print("current voltage is %.2f V") % currV
            
            if options.power == "1" and currV < 0.1:
                print("ramping up...")
                for volt in range(0,int((int(options.target)+it)/2)+1,1):
                    mykey.set_V(volt)
                    mykey.set_state(1)
                    time.sleep(0.5)
            
            elif options.power == "0" and currV > 0.1:
                print("ramping down...")
                for volt in range(int(currV),-1,-1):
                    mykey.set_V(volt)
                    mykey.set_state(1)
                    time.sleep(0.5)
            
            else:
                print("doing nothing")
            
            time.sleep(2)
            I = mykey.meas_I()
            V = mykey.meas_V()
            print("voltage: %.2f V   current: %.3f A") %(V,I)
        
        it += 1

if options.combinePS == '0':
    
    mapping = {}
    mapping['keithley2231A-0'] = ['CH1']
    
    for usb in mapping.keys():
        channels = mapping[usb]
        for ch in channels:
            mykey = Keithley2231A('ASRL/dev/'+usb+'::INSTR', ch)
            
            currV = mykey.meas_V()
            print("current voltage is %.2f V") % currV
            
            if options.power == "1" and currV < 0.1:
                print("ramping up...")
                for volt in range(0,int(options.target)+1,1):
                    mykey.set_V(volt)
                    mykey.set_state(1)
                    time.sleep(0.5)
            
            elif options.power == "0" and currV > 0.1:
                print("ramping down...")
                for volt in range(int(currV),-1,-1):
                    mykey.set_V(volt)
                    mykey.set_state(1)
                    time.sleep(0.5)
                
            else:
                print("doing nothing")
        
            time.sleep(2)
            I = mykey.meas_I()
            V = mykey.meas_V()
            print("voltage: %.2f V   current: %.3f A") %(V,I)
