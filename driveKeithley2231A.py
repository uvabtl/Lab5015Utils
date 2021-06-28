#!/usr/bin/env python3

from datetime import datetime
import sys
import time
import logging
from optparse import OptionParser

sys.path.append("/home/cmsdaq/Lab5015Utils/")
from Lab5015_utils import Keithley2231A

parser = OptionParser()
parser.add_option("--setV")
parser.add_option("--setState")
(options,args)=parser.parse_args()

mykey = Keithley2231A()
mykey.set_V(float(options.setV))
mykey.set_state(int(options.setState))

time.sleep(2)
I = mykey.meas_I()
V = mykey.meas_V()
print (I,V)
