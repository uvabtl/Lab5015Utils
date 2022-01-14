#!/usr/bin/env python3

from movingTable import movingTable
from optparse import OptionParser
import time

parser = OptionParser()

parser.add_option("-x", dest="x", default="0")
parser.add_option("-y", dest="y", default="0")
(options, args) = parser.parse_args()

myTable = movingTable()
print("moving to x=",x," y=",y)
myTable.goToXY(1,1)

x,y = myTable.getGlobalCoordinates()
print("coordinates are now: ", x, y)
print("DONE")
