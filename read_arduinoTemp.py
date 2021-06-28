#!/usr/bin/env python3

import serial
import time

command = '1'
out = ""

try:
    ser = serial.Serial("/dev/ttyACM0", 115200)
    ser.timeout = 1
except serial.serialutil.SerialException:
    #no serial connection
    print('not possible to establish connection with device')
    
data = ser.readline()[:-2] #the last bit gets rid of the new-line chars
x = ser.write(command+'\r\n')

# let's wait one second before reading output (let's give device time to answer)
time.sleep(1)
while ser.inWaiting() > 0:
    out += ser.read(1)
    
ser.close()
        
if out != "":
    out.replace("\r","").replace("\n","")
    
print(out)

