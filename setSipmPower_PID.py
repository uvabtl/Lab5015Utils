#! /usr/bin/python3

import sys
import time
from Lab5015_utils import Keithley2231A
from optparse import OptionParser
from datetime import datetime
from simple_pid import PID

parser = OptionParser()

parser.add_option("--target", type=float, dest="target", default=0.435)
(options, args) = parser.parse_args()

debug = True

min_voltage = 0.
max_voltage = 2.

min_pow_safe = 0.
max_pow_safe = 2. # Watts

if options.target < min_pow_safe or options.target > max_pow_safe:
    print("### ERROR: set power outside allowed range ["+str(min_temp_safe)+"-"+str(max_temp_safe)+"]. Exiting...")
    sys.exit(-1)



SiPM = Keithley2231A()  #instantiate PowerSupply

state = SiPM.check_state()
print(datetime.now())
print(">>> PS::state: "+str(state))

if state is 0:
    print("--- powering on the PS")
    SiPM.set_V(0.0)
    SiPM.set_state(1)
    time.sleep(1)
    state = SiPM.check_state()
    print(">>> PS::state: "+str(state))
    if state == 0:
        print("### ERROR: PS did not power on. Exiting...")
        sys.exit(-2)


I = SiPM.meas_I()
V = SiPM.meas_V()
P = I * V - (I * I * 1.2) # hardcoded resistance of the cable

new_voltage = V
print("--- [Current SiPM power: "+str(P)+" W]\n")
sys.stdout.flush()

pid = PID(0.5, 0., 1., setpoint=options.target)
pid.output_limits = (-0.5, 0.5)



while True:
    try:

        I = SiPM.meas_I()
        V = SiPM.meas_V()
        P = I * V - (I * I * 1.3) # hardcoded resistance of the cable    
        
        output = pid(P)
        new_voltage += output
        
        #safety check
        new_voltage = min([max([new_voltage,min_voltage]),max_voltage])

        if debug:
            p, i, d = pid.components
            print("== DEBUG == P=", p, "I=", i, "D=", d)

        print(datetime.now())
        print("--- setting SiPM voltage to "+str(new_voltage)+" V    [sipm current: "+str(I)+" sipm power: "+str(P)+" W]")
        SiPM.set_V(new_voltage)
        sleep_time = 0.2
        print("--- sleeping for "+str(sleep_time)+" s   [kill at any time with ctrl-C]\n")
        sys.stdout.flush()
        time.sleep(sleep_time)
    
    except KeyboardInterrupt:
        break
        time.sleep(3)

print("--- powering off the PS")
SiPM.set_state(0)
time.sleep(2)
state = SiPM.check_state()
print(">>> PS::state: "+str(state))
if state == 1:
    print("### ERROR: PS did not power off. Exiting...")
    sys.exit(-3)
print("bye")
sys.exit(0)
