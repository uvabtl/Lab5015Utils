import zmq
import serial
from time import sleep

class LAUDAServer():
    def __init__(self, portname='/dev/ttyS0', port=5050):
        self.instr = serial.Serial(portname, 9600, timeout=2)

        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://*:%d"%port)

        print("SerialServer listening at *:%d relaying to %s" % (port,portname))

    def loop(self):
        while True:
            msg = self.socket.recv().decode("utf-8").strip()
            print("Processing %s" % msg)

            reply = ""
            self.instr.write(str(msg+"\r\n").encode())
            reply = self.instr.readline()
            self.socket.send(reply)
                
            sleep(0.5)

            




from optparse import OptionParser
parser = OptionParser()
parser.add_option("-p","--port")
parser.add_option("-d","--device")
(options,args)=parser.parse_args()

myServer = LAUDAServer(port=int(options.port),portname=options.device)
myServer.loop()
