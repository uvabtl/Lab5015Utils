from datetime import datetime
import sys
import time
import logging
from optparse import OptionParser

sys.path.append("/home/cmsdaq/Lab5015Utils/")
from Lab5015_utils import Keithley2450

parser = OptionParser()
parser.add_option("--setV")
parser.add_option("--setState")
parser.add_option("--set4wire")
(options,args)=parser.parse_args()

mykey = Keithley2450()
mykey.set_V(float(options.setV))
mykey.set_4wire(str(options.set4wire))
mykey.set_state(int(options.setState))
(_, I, V) = mykey.meas_IV()
print (I,V)
