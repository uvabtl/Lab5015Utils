import serial
from SerialClient import serialClient
import time
import sys


class movingTable():
    """Instrument class for controlling the movingTable
    Args:
        * portname (str): port name
    """

    def __init__(self, portname='tcp://127.0.0.1:5060'):
        if 'tcp://' in portname:
            self.instr = serialClient(portname)
        else:
            print("ERROR: specify TCP address for communication")

    def deltaXY(self, deltaX, deltaY):
        """Move table by deltaX, deltaY."""
        self.instr.write("delta "+str(deltaX)+" "+str(deltaY))
        return self.instr.readline().strip()

    def goToXY(self, deltaX, deltaY):
        """Move table to coordinates X, Y."""
        self.instr.write("go "+str(deltaX)+" "+str(deltaY))
        return self.instr.readline().strip()

    def getGlobalCoordinates(self):
        """Read table global coordinates"""
        self.instr.write("get")
        globalX, globalY = self.instr.readline().strip().split()
        return float(globalX), float(globalY)

    def goHome(self):
        """Move table to axis origin"""
        reply = self.goToXY(0.0, 0.0)
        return reply



class movingTableDirect():
    """Instrument class for controlling the movingTable
    Args:
        * portname (str): port name
    """

    def __init__(self, portname='/dev/cu.usbserial-146110'):
        self.instr = serial.Serial(portname, 115200)
        # Wake up grbl
        wakeUp = "\r\n\r\n"
        self.instr.write(wakeUp.encode())
        time.sleep(2)  # Wait for grbl to initialize
        self.instr.flushInput()  # Flush startup text in serial input

        #Homing cycle
        command = "$H\n"
        self.instr.write(command.encode()) # Send g-code block to grbl
        grbl_out = self.instr.readline()

        #set coordinateds to 0,0
        command = "G10 P0 L20 X0 Y0 Z0\n"
        self.instr.write(command.encode()) # Send g-code block to grbl
        grbl_out = self.instr.readline()

        self.globalX = 0.0
        self.globalY = 0.0
        self.absMaxX = 150
        self.absMaxY = 150

    #go home when done
    def __del__(self):
        self.goHome()

    def isSafe(self):
        if abs(self.globalX) < self.absMaxX and abs(self.globalY) < self.absMaxY:
            return 0
        else:
            self.goHome()
            print("COORDINATEDS OUT OF RANGE")
            sys.exit()

    def deltaX(self, delta):
        self.globalX += delta
        #self.isSafe()   #already coded in fw
        command = "G90 G0 X"+str(self.globalX)+" Y"+str(self.globalY)+"\n"
        self.instr.write(command.encode()) # Send g-code block to grbl
        grbl_out = self.instr.readline().decode()
        return grbl_out

    def deltaY(self, delta):
        self.globalY += delta
        #self.isSafe()   #already coded in fw
        command = "G90 G0 X"+str(self.globalX)+" Y"+str(self.globalY)+"\n"
        self.instr.write(command.encode()) # Send g-code block to grbl
        grbl_out = self.instr.readline().decode()
        return grbl_out

    def deltaXY(self, deltaX, deltaY):
        self.globalX += deltaX
        self.globalY += deltaY
        #self.isSafe()   #already coded in fw
        command = "G90 G0 X"+str(self.globalX)+" Y"+str(self.globalY)+"\n"
        self.instr.write(command.encode()) # Send g-code block to grbl
        grbl_out = self.instr.readline().decode()
        return grbl_out

    def getGlobalCoordinates(self):
        return self.globalX, self.globalY

    def goHome(self):
        self.globalX = 0.0
        self.globalY = 0.0
        command = "G90 G0 X"+str(self.globalX)+" Y"+str(self.globalY)+"\n"
        self.instr.write(command.encode()) # Send g-code block to grbl
        grbl_out = self.instr.readline().decode()
        return grbl_out
