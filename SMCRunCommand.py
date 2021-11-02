import telepot
from decouple import config
import os, sys, time, random, datetime
from Lab5015_utils import SMChiller

WORKING_DIR = "/home/cmsdaq/Programs/Lab5015Utils"
LOG_DIR = WORKING_DIR+"/Alarms"

os.chdir(WORKING_DIR)
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
tlog_file = open(LOG_DIR+"/SMCRunCommand.log", "a")
tlog_file.write('I am listening...\n')
tlog_file.flush()


def handle(msg):
    SMC = SMChiller()

    chat_id = msg['chat']['id']
    command = msg['text']

    tlog_file.write('Got command: %s\n' % command )
    tlog_file.write(' from chat id = %s\n' % chat_id )
    tlog_file.flush()

#    if (chat_id == 145950543):
    if (chat_id != 0):
#    if (1):
        if (command == '/press' or command == 'Press'):
            my_press = SMC.read_meas_press()
            bot.sendMessage(chat_id, "pressure is: %s MPa" % my_press)

        elif (command == '/temp' or command == 'Temp'):
            my_temp = SMC.read_meas_temp()
            bot.sendMessage(chat_id, "temperature is: %s°C" % my_temp)

        elif (command == '/state' or command == 'State'):
            my_state = SMC.check_state()
            bot.sendMessage(chat_id, "state is: %s" % my_state)

        elif (command == '/how_is_life' or command == 'How is life?'):
            my_press = SMC.read_meas_press()
            my_temp = SMC.read_meas_temp()
            bot.sendMessage(chat_id, "I am fine thanks")
            bot.sendMessage(chat_id, "Pressure is %s MPa and water temp is %s°C" % (my_press, my_temp))

        elif (command == '/commands' or command == 'commands'):
            bot.sendMessage(chat_id, "Available commands are: /press, /temp, /state, /how_is_life")

        else:
            bot.sendMessage(chat_id, "I wish you a great day!")
    else:
        bot.sendMessage(chat_id, "I don't know you")





telegram_token = config('TELEGRAM_TOKEN')
bot = telepot.Bot(telegram_token)
bot.message_loop(handle)


while (1):
    time.sleep(10)
