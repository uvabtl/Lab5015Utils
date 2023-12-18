import minimalmodbus
import serial
import pyvisa
import subprocess
import time
import sys
from SerialClient import serialClient
from simple_pid import PID
from datetime import datetime



##########################
class RTO6():
    """Instrument class for RTO6

    Args:
        * portname (str): port name

    """

    def __init__(self, portname='TCPIP0::100.100.100.17::INSTR'):
        self.instr = pyvisa.ResourceManager('@py').open_resource(portname)
        query_out = self.instr.query("*IDN?").strip()
        print(query_out)
        out = self.instr.write("SYSTem:DISPlay:UPDate OFF")
        print(out)
        out = self.instr.write("REFCurve<1>:CLEar")
        print(out)
        out = self.instr.write("ACQuire:COUNt 4000")
        print(query_out)
        out = self.instr.write("SINGle; *OPC?")
        print(out)
        time.sleep(10)
        out = self.instr.write("EXPort:WAVeform:NAME \"C:\Users\Public\Documents\Rohde-Schwarz\RTx\RefWaveforms\DataExpWfm.bin\"")
        print(out)
        out = self.instr.write("CHANnel1:WAV1:HISTory:STATe ON")
        print(out)
        out = self.instr.write("EXPort:WAVeform:DLOGging ON")
        print(out)
        out = self.instr.write("EXPort:WAVeform:TIMestamps ON")
        print(out)
        out = self.instr.write("CHANnel1:WAV1:HISTory:STARt -3999")
        print(out)
        out = self.instr.write("CHANnel1:WAV1:HISTory:STOP 0")
        print(out)
        out = self.instr.write("CHANnel1:WAV1:HISTory:REPLay OFF")
        print(out)
        query_out = self.instr.query("CHANnel1:WAV1:HISTory:PLAY; *OPC?").strip()
        print(query_out)        
