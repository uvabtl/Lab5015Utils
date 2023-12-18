#!/usr/bin/env python3

from datetime import datetime
import sys
import time
import logging
from optparse import OptionParser

sys.path.append("/home/cmsdaq/Lab5015Utils/")
from Lab5015_utils import KeithleyDMM6500

parser = OptionParser()
(options,args)=parser.parse_args()

mykey = KeithleyDMM6500()
#for it in range(0,10):
V = mykey.readScan(4)
print(V)
time.sleep(2)
