import minimalmodbus
import zmq
import serial
import minimalmodbus
from time import sleep

class SMCServer( minimalmodbus.Instrument ):
    def __init__(self, portname='/dev/ttyS0', slaveaddress=1, port=5050):
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)
        self.serial.baudrate = 19200
        self.serial.bytesize = 7
        self.serial.parity   = serial.PARITY_EVEN
        self.serial.timeout  = 0.3
        self.mode = minimalmodbus.MODE_ASCII

        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://*:%d"%port)

        print("SerialServer listening at *:%d relaying to %s" % (port,portname))

    def loop(self):
        while True:
            msg = self.socket.recv().decode("utf-8").strip()
            print("Processing %s" % msg)
            msg = msg.split()

            reply = ""
            if "write" in msg:
                self.write(msg[1], msg[2], msg[3])
                reply = "OK"
                self.socket.send(reply.encode())

            if "read" in msg:
                reply = str(self.read(msg[1], msg[2]))
                self.socket.send(reply.encode())

            sleep(0.5)

            

    def write(self, register, precision, value):
        self.write_register(int(register), float(value), int(precision))

    def read(self, register, precision):
        return self.read_register(int(register), int(precision))
            


from optparse import OptionParser
parser = OptionParser()
parser.add_option("-p","--port")
parser.add_option("-d","--device")
(options,args)=parser.parse_args()

myServer = SMCServer(port=int(options.port),portname=options.device)
myServer.loop()
