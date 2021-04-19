from Lab5015_utils import SMChiller
from optparse import OptionParser

parser = OptionParser()

parser.add_option("--temp", dest="temp", default="19.5")
parser.add_option("--power", dest="power", default="0")
(options, args) = parser.parse_args()



SMC = SMChiller()

print("set temp")
SMC.write_set_temp(options.temp)
print("set power")
SMC.set_state(options.power)

