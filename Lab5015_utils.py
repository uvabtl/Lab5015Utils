import minimalmodbus
import serial
import pyvisa
import subprocess
import time
import sys
from simple_pid import PID
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
        * channel (str): channel name

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
        volt = self.instr.query("MEAS:VOLT?").strip()
        return(float(volt))

    def meas_I(self):
        """measure current"""
        curr = self.instr.query("MEAS:CURR?").strip()
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
class sipmPower():
    """class to control the power delivered to SiPMs

    Args:
        * target (str): target power

    """

    def __init__(self, target=0.432):
        self.target = float(target)
        self.sipm = Keithley2231A(chName="CH1")

        self.min_voltage = 0.
        self.max_voltage = 2.

        self.min_pow_safe = 0.
        self.max_pow_safe = 2. # Watts   

        self.debug = True
        
        if self.target < self.min_pow_safe or self.target > self.max_pow_safe:
            raise ValueError("### ERROR: set power outside allowed range")

        self.state = self.sipm.check_state()
        self.I = 0.
        self.V = 0.
        self.P = 0.
        self.new_voltage = self.V

        self.pid = PID(0.5, 0., 1., setpoint=self.target)
        self.pid.output_limits = (-0.5, 0.5)


    def power_on(self):
        if self.state is 0:
            print("--- powering on the PS")
            self.sipm.set_V(0.0)
            self.sipm.set_state(1)
            time.sleep(2)
            self.state = self.sipm.check_state()
            if self.state == 0:
                raise ValueError("### ERROR: PS did not power on")

    def power_off(self):
        if self.state is 1:
            print("--- powering off the PS")
            self.sipm.set_V(0.0)
            self.sipm.set_state(0)
            time.sleep(2)
            self.state = self.sipm.check_state()
            if self.state != 0:
                raise ValueError("### ERROR: PS did not power off")


    def compute_voltage(self):
        self.power_on()

        self.I = self.sipm.meas_I()
        self.V = self.sipm.meas_V()
        self.P = self.I * self.V - (self.I * self.I * 1.3) # hardcoded resistance of the cable

        output = self.pid(self.P)
        self.new_voltage += output

        #safety check
        self.new_voltage = min([max([self.new_voltage,self.min_voltage]),self.max_voltage])

        if self.debug:
            print(datetime.now())
            p, i, d = self.pid.components
            print("== DEBUG == P=", p, "I=", i, "D=", d)
            print("--- setting SiPM voltage to "+str(self.new_voltage)+" V    [sipm current: "+str(self.I)+" sipm power: "+str(self.P)+" W]\n")
            sys.stdout.flush()

        self.sipm.set_V(self.new_voltage)
        sleep_time = 0.5



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
