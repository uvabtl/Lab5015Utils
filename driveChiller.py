#!/usr/bin/env python3

from Lab5015_utils import SMChiller, LAUDAChiller
from optparse import OptionParser
import time

parser = OptionParser()

parser.add_option("--check-state", dest="check_state", action="store_true")
parser.add_option("--water-temp", dest="water_temp", action="store_true")
parser.add_option("--set-temp", dest="set_temp", action="store_true")
parser.add_option("--power-on", dest="power_on", action="store_true")
parser.add_option("--power-off", dest="power_off", action="store_true")
parser.add_option("--target", dest="target", default="23.0")
(options, args) = parser.parse_args()


if options.power_on and options.power_off:
    print("Error: cannot power on and off simultaneously. Choose only one option. Exiting...")
    exit()

SMC = LAUDAChiller()
state = int(SMC.check_state()) 
    
if options.check_state:
    print(state)

if options.water_temp:
    water_temp = SMC.read_meas_temp()
    print(water_temp)

if options.power_on:
    if state == 1:
        print("Chiller is already on. Doing nothing...")
    else:
        print("Power on chiller")
        SMC.set_state(1)
        time.sleep(1)
        
if options.power_off:
    if state == 0:
        print("Chiller is already off. Doing nothing...")
    else:
        print("Power off chiller")
        SMC.set_state(0)
        time.sleep(1)
    
if options.set_temp:
    if state == 0:
        print("Power on chiller")
        SMC.set_state(1)
    print("set temp to ", options.target)
    SMC.write_set_temp(options.target)
    time.sleep(3)
