import pyvisa
from pyvisa import constants

rm = pyvisa.ResourceManager()
print(rm.list_resources())

my_instrument = rm.open_resource('ASRL/dev/ttyUSB0::INSTR', baud_rate=19200)
my_instrument.read_termination = '\n'
my_instrument.write_termination = '\n'

while 1 :

    inkey = ''
    inkey = input(">> ")

    if inkey == 'exit':
        exit()
    else:
        answer = my_instrument.query(inkey)
        print(answer)
