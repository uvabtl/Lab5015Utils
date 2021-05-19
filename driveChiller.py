from Lab5015_utils import SMChiller
from optparse import OptionParser

parser = OptionParser()

parser.add_option("--temp", dest="temp", default="19.5")
parser.add_option("--power", dest="power", default="0")
(options, args) = parser.parse_args()



SMC = SMChiller()

print("set temp to ", options.temp)
SMC.write_set_temp(options.temp)
print("set power to ", options.power)
SMC.set_state(options.power)


if float(SMC.read_set_temp()) != float(options.temp):
    print("wrong temp")


if int(SMC.check_state()) != int(options.power):
    print("power")
