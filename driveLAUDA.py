#!/usr/bin/env python3

from Lab5015_utils import LAUDAChiller
from optparse import OptionParser
import time



LAUDA = LAUDAChiller()
print(LAUDA.write_set_temp(32.0))
