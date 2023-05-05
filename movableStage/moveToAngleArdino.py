# Importing Libraries
import serial
import time
import os
import argparse

#define allowed angle range
minAngle = 0
maxAngle = 80


arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)
time.sleep(2)

#reading target angle from argument
parser = argparse.ArgumentParser(description='Insert target angle')
parser.add_argument("--angle", type=int, dest="angle", required=True, help=" insert (int) for target angle")
parser.add_argument("--speed", type=int, dest="speed", required=False, help=" insert (int) for target speed (step/sec)")

args = parser.parse_args()
target_angle  = args.angle
stepper_speed = args.speed



time.sleep(0.05)
filename = "log_rotating_stage.txt"

#read current angle from log file
with open(filename, "r") as f:
    angles = [int(x) for x in next(f).split()]


#define delta angle and pass argument to arduino
current_angle  = int(angles[0])
print("current_angle:", current_angle)
print("target_angle :", target_angle)

    
delta_angle = target_angle-current_angle
print("delta_angle  :", delta_angle)

if (delta_angle!=0 and target_angle>=minAngle and target_angle<=maxAngle):

    arduino.write(bytes(str(delta_angle), 'utf-8'))#write(str(delta_angle)).encode()
    sleep_time = abs(delta_angle/1.)
    print("moving to angle...  (will take", sleep_time, "seconds)")
    time.sleep(sleep_time)    
    current_angle = target_angle

    #printout arduino serial buffer
    data = ''
    while arduino.inWaiting() > 0:
        data += arduino.read(1).decode()
    if (data!=''):
        print(data)
    time.sleep(0.5)
        
elif (delta_angle==0):
    print("No rotation needed: you are already at the desired angle!")
elif (delta_angle!=0):
    print("WARNING: target angle is outside allowed range!")

    

    
#overwrite new current angle to log file
os.remove(filename)
with open(filename, "w+") as f:
    f.write(str(current_angle))
    
