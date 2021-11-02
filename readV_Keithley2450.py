#! /usr/bin/python2

import sys

sys.path.append("/home/cmsdaq/Programs/Lab5015Utils/")
from Lab5015_utils_p2 import Keithley2450

mykey = Keithley2450()
(_, V) = mykey.meas_V()
print (V)
