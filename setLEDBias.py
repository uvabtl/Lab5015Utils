#!/usr/bin/env python3

from Lab5015_utils import AgilentE3633A
from Lab5015_utils import Keithley2231A 
from optparse import OptionParser
import time


parser = OptionParser()
parser.add_option("--power", dest="power", default="0")
parser.add_option("--target", dest="target", default="0")
(options,args)=parser.parse_args()

#ps = AgilentE3633A()
ps = Keithley2231A('ASRL/dev/keithley2231A-1::INSTR', 'CH2')

state = ps.check_state()

if state == 0 and options.power == '1':
    #ps.set_range('HIGH')
    #time.sleep(1)
    ps.set_V(float(options.target))
    time.sleep(0.2)
    ps.set_state(1)
    
    curr = ps.meas_I()
    volt = ps.meas_V()
    state = ps.check_state()
    print(state,volt,curr)

if state == 1 and options.power == '1':
    ps.set_V(float(options.target))
    time.sleep(0.2)
    
    curr = ps.meas_I()
    volt = ps.meas_V()
    state = ps.check_state()
    print(state,volt,curr)

elif state == 1 and options.power == '0':
    ps.set_V(0.)
    #ps.set_state(0)
    time.sleep(0.2)
    
    curr = ps.meas_I()
    volt = ps.meas_V()
    state = ps.check_state()
    print(state,volt,curr)

else:
    print('do nothing')
