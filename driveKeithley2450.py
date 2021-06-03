from datetime import datetime
import sys
import time
import logging
from optparse import OptionParser

sys.path.append("/home/cmsdaq/Lab5015Utils/")
from Lab5015_utils import Keithley2450

parser = OptionParser()
parser.add_option("--setV")
(options,args)=parser.parse_args()

mykey = Keithley2450()
mykey.set_V(float(options.setV))
mykey.set_state(1)
(_, I, V) = mykey.meas_IV()
print (I,V)
