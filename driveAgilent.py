#!/usr/bin/env python3

from Lab5015_utils import AgilentE3633A
from optparse import OptionParser
import time


parser = OptionParser()
parser.add_option("--setV")
parser.add_option("--setState")
(options,args)=parser.parse_args()

ps = AgilentE3633A()

ps.set_V(float(options.setV))
ps.set_range('HIGH')
ps.set_state(int(options.setState))

curr = ps.meas_I()
print("Current: ",curr)
volt = ps.meas_V()
print("Tension: ",volt)
state = ps.check_state()
print("State: ",state)

