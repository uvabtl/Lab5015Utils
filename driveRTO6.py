#!/usr/bin/env python3

from datetime import datetime
import sys
import time
import logging
from optparse import OptionParser

sys.path.append("/home/cmsdaq/Lab5015Utils/")
from RTO6Wrapper import RTO6

parser = OptionParser()
#parser.add_option("--setV")
#parser.add_option("--setState")
#parser.add_option("--set4wire")
(options,args)=parser.parse_args()

mykey = RTO6()
