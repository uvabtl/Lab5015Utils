import minimalmodbus
import serial
import pyvisa
import subprocess
from datetime import datetime



###################################################
class SMChiller( minimalmodbus.Instrument ):
    """Instrument class for SMC chiller.

    Args:
        * portname (str): port name
        * slaveaddress (int): slave address in the range 1 to 247

    """

    def __init__(self, portname='/dev/ttyS0', slaveaddress=1):
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)
        self.serial.baudrate = 19200
        self.serial.bytesize = 7
        self.serial.parity   = serial.PARITY_EVEN
        self.serial.timeout  = 0.3
        self.mode = minimalmodbus.MODE_ASCII


    def read_meas_temp(self):
        """Return the measured circulating fluid discharge temperature [°C]."""
        return self.read_register(0, 1)

    def read_set_temp(self):
        """Return the circulating fluid set temperature [°C]."""
        return self.read_register(11, 1)

    def read_meas_press(self):
        """Return the measured circulating fluid discharge pressure [MPa]."""
        return self.read_register(2, 2)

    def write_set_temp(self, value):
        """Set the working temperature [°C]"""
        self.write_register(11, float(value), 1)

    def check_state(self):
        """Return the chiller state (0: OFF, 1: RUNNING)"""
        return self.read_register(12, 0)

    def set_state(self, value):
        """Set the chiller state (0: OFF, 1: RUNNING)"""
        self.write_register(12, float(value), 0)



###################################################
class PiLas():
    """Instrument class for PiLas laser

    Args:
        * portname (str): port name

    """

    def __init__(self, portname='ASRL/dev/ttyUSB0::INSTR'):
        self.instr = pyvisa.ResourceManager().open_resource(portname)
        self.instr.baud_rate = 19200
        self.instr.read_termination = '\n'
        self.instr.write_termination = '\n'

    def read_tune(self):
        """Return the laser tune [%]"""
        print(self.instr.query("tune?"))

    def read_freq(self):
        """Return the laser frequency [Hz]"""
        print(self.instr.query("f?"))

    def check_state(self):
        """Return the laser state (0: OFF, 1: RUNNING)"""
        print(self.instr.query("ld?"))

    def set_state(self, value):
        """Set the laser state (0: OFF, 1: RUNNING)"""
        print(self.instr.query("ld="+str(value)))
        
    def set_tune(self, value):
        """Set the laser tune [%]"""
        print(self.instr.query("tune="+str(value)))

    def set_freq(self, value):
        """Set the laser frequency [Hz]"""
        print(self.instr.query("f="+str(value)))



##########################

def read_box_temp():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    out = subprocess.run(['ssh', 'pi@100.100.100.5', './getTemperature.py ', current_time],
                         stdout=subprocess.PIPE)
    result = out.stdout.decode('utf-8').rstrip('\n').split()
    
    if len(result) != 2:
        raise Exception("Could not read box temperature")
    else:
        return result[1]
