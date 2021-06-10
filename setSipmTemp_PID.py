#! /usr/bin/python3

import sys
import time
from Lab5015_utils import Keithley2450
from Lab5015_utils import read_arduino_temp
from optparse import OptionParser
from datetime import datetime
from simple_pid import PID

parser = OptionParser()

parser.add_option("--target", type=float, dest="target", default=22.0)
(options, args) = parser.parse_args()

debug = True

min_voltage = -5.
max_voltage =  5.

min_temp_safe = 10.
max_temp_safe = 40.

if options.target < min_temp_safe or options.target > max_temp_safe:
    print("### ERROR: set temperature outside allowed range ["+str(min_temp_safe)+"-"+str(max_temp_safe)+"]. Exiting...")
    sys.exit(-1)



TEC = Keithley2450()  #instantiate PowerSupply

state = TEC.check_state()
print(datetime.now())
print(">>> PS::state: "+str(state))

if state is 0:
    print("--- powering on the PS")
    TEC.set_V(0.0)
    TEC.set_state(1)
    time.sleep(2)
    state = TEC.check_state()
    print(">>> PS::state: "+str(state))
    if state == 0:
        print("### ERROR: PS did not power on. Exiting...")
        sys.exit(-2)


sipm_temp = 25.
while True:
    try:
        sipm_temp = float(read_arduino_temp()[4])
        break
    except ValueError as e:
        print(e)
        time.sleep(2)
        continue


(_,I,V) = TEC.meas_IV()
new_voltage = V
print("--- [Current SiPM temperature: "+str(sipm_temp)+"° C]\n")
sys.stdout.flush()

pid = PID(-0.5, 0., -1, setpoint=options.target)
pid.output_limits = (-2, 2)



while True:
    try:

        try:
            sipm_temp = float(read_arduino_temp()[4])
        except ValueError as e:
            print(e)
            time.sleep(2)
            continue
        
        output = pid(sipm_temp)
        new_voltage += output
        
        #safety check
        new_voltage = min([max([new_voltage,min_voltage]),max_voltage])

        if debug:
            p, i, d = pid.components
            print("== DEBUG == P=", p, "I=", i, "D=", d)

        (_,I,V) = TEC.meas_IV()
        print(datetime.now())
        print("--- setting TEC voltage to "+str(new_voltage)+" V    [sipm temperature: "+str(sipm_temp)+"° C]")
        TEC.set_V(new_voltage)
        sleep_time = 2
        print("--- sleeping for "+str(sleep_time)+" s   [kill at any time with ctrl-C]\n")
        sys.stdout.flush()
        time.sleep(sleep_time)
    
    except KeyboardInterrupt:
        break

print("--- powering off the PS")
TEC.set_state(0)
time.sleep(2)
state = TEC.check_state()
print(">>> PS::state: "+str(state))
if state == 1:
    print("### ERROR: PS did not power off. Exiting...")
    sys.exit(-3)
print("bye")
sys.exit(0)
