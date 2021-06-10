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

    def __init__(self, portname='ASRL/dev/pilas::INSTR'):
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
class Keithley2450():
    """Instrument class for Keithley 2450

    Args:
        * portname (str): port name

    """

    def __init__(self, portname='TCPIP0::100.100.100.7::INSTR'):
        self.instr = pyvisa.ResourceManager().open_resource(portname)
        self.mybuffer = "\"defbuffer1\""
        self.instr.write(":TRAC:CLE "+self.mybuffer) #clear buffers and prepare for measure

    def query(self, query):
        """Pass a query to the power supply"""
        print(self.instr.query(query).strip())

    def meas_V(self):
        """Return time and voltage"""
        query_out = self.instr.query(":MEASure:VOLT? "+self.mybuffer+", SEC, READ").strip()
        time = query_out.split(",")[0]
        volt = query_out.split(",")[1]
        return(float(time), float(volt))

    def meas_I(self):
        """Return time and current"""
        query_out = self.instr.query(":MEASure:CURR? "+self.mybuffer+", SEC, READ").strip()
        time = query_out.split(",")[0]
        curr = query_out.split(",")[1]
        return(float(time), float(curr))

    def meas_IV(self):
        """Return time and current"""
        self.instr.query(":MEASure:CURR? "+self.mybuffer+", READ")

        query_out = self.instr.query("FETCh? "+self.mybuffer+", SEC,READ,SOURCE").strip()
        time = query_out.split(",")[0]
        curr = query_out.split(",")[1]
        volt = query_out.split(",")[2]
        return(float(time), float(curr), float(volt))

    def set_V(self, value):
        """Set operating voltage"""
        return(self.instr.write("SOUR:VOLT "+str(value)))

    def set_state(self, value):
        """Set the PS state (0: OFF, 1: RUNNING)"""
        return(self.instr.write("OUTP "+str(value)))

    def check_state(self):
        """Check the PS state (0: OFF, 1: RUNNING)"""
        return(int(self.instr.query("OUTP?").strip()))


##########################
class Keithley2231A():
    """Instrument class for Keithley 2231A

    Args:
        * portname (str): port name

    """

    def __init__(self, portname='ASRL/dev/keithley2231A::INSTR', chName="CH1"):
        self.instr = pyvisa.ResourceManager().open_resource(portname)
        self.chName = chName
        self.instr.write("SYSTem:REMote")
        self.instr.write("INST:SEL "+self.chName)

    def query(self, query):
        """Pass a query to the power supply"""
        print(self.instr.query(query).strip())

    def meas_V(self):
        """read set voltage"""
        volt = self.instr.query("MEAS:VOLT? "+self.chName).strip()
        return(float(volt))

    def meas_I(self):
        """measure current"""
        curr = self.instr.query("MEAS:CURR? "+self.chName).strip()
        return(float(curr))

    def set_V(self, value):
        """set voltage"""
        return(self.instr.write("APPL "+self.chName+","+str(value)))

    def set_state(self, value):
        """Set the PS state (0: OFF, 1: RUNNING)"""
        return(self.instr.write("OUTP "+str(value)))

    def check_state(self):
        """Check the PS state (0: OFF, 1: RUNNING)"""
        return(int(self.instr.query("OUTP?").strip()))


##########################
def read_box_temp():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    out = subprocess.run(['ssh', 'pi@100.100.100.5', './getTemperature.py ', current_time],
                         stdout=subprocess.PIPE)
    result = out.stdout.decode('utf-8').rstrip('\n').split()
    
    if len(result) != 2:
        raise ValueError("Could not read box temperature")
    else:
        return result[1]


##########################
def read_arduino_temp():
    out = subprocess.run(['ssh', 'pi@100.100.100.5', './read_arduinoTemp.py'],
                         stdout=subprocess.PIPE)
    result = out.stdout.decode('utf-8').rstrip('\n').split()
    
    if len(result) != 7:
        raise ValueError("Could not read arduino temperature")
    else:
        return result
