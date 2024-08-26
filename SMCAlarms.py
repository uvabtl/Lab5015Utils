#!/usr/bin/python3
#run this command to start daemon each time the pi is switched off

import os
import time
import datetime
import pathlib

import requests
from logging import Handler, Formatter
import logging
from decouple import config

from optparse import OptionParser
from Lab5015_utils import SMChiller

TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
TELEGRAM_CHAT_LIST = ["-569856912"] # lab5015 alarm group
TELEGRAM_CHAT_ID = "-569856912"

WORKING_DIR = "/home/cmsdaq/Programs/Lab5015Utils"
ALARMS_DIR = WORKING_DIR+"/Alarms"


class RequestsHandler(Handler):
    def emit(self, record):
        log_entry = self.format(record)
        payload =        {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': log_entry,
            'parse_mode': 'HTML'
        }
        return requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=TELEGRAM_TOKEN), data=payload).content




class LogstashFormatter(Formatter):
    def __init__(self):
        super(LogstashFormatter, self).__init__()
    def format(self, record):
        t = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        return "<i>{datetime}</i><pre>\n{message}</pre>".format(message=record.msg, datetime=t)     




# global vars
period = 0.5 # log every nsec
delay = 2 # time delay between check state and check press
press_high_alert = 0.35 #MPa
press_low_alert = 0.10 #MPa

def main():
    parser = OptionParser()
    parser.add_option("--log", dest="log", default="")
    (options, args) = parser.parse_args()

    SMC = SMChiller()

    os.chdir(WORKING_DIR)

    logger = logging.getLogger('trymeApp')
    logger.setLevel(logging.WARNING)
    
    for ichat in TELEGRAM_CHAT_LIST:
        TELEGRAM_CHAT_ID = ichat
        #print('chat_id: ',ichat)
        handler = RequestsHandler()
        formatter = LogstashFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)


    chillerState = pathlib.Path("/home/cmsdaq/Programs/Lab5015Utils/chillerState.txt")

    while (1):

        my_press = SMC.read_meas_press()
        my_state = SMC.check_state()            

        # getting local day and time
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        lastAction = datetime.datetime.fromtimestamp(chillerState.stat().st_mtime)

        if (now - lastAction).total_seconds() < delay:
            time.sleep(delay)
            continue



        if options.log != "":
            if not os.path.exists(ALARMS_DIR):
                os.mkdir(ALARMS_DIR)
            tlog_file = open(ALARMS_DIR+"/"+options.log, "a")
            tlog_file.write("Time: "+current_time+" State: "+str(my_state)+" Press: "+str(my_press)+"\n")
            tlog_file.close()

            tlog_file = open(ALARMS_DIR+"/"+options.log, "r")
            lines = tlog_file.readlines()
            tlog_file.close()

            tlog_file = open(ALARMS_DIR+"/"+options.log, "w")
            lines = lines[-200000:] #buffer last 200000 seconds in the log file
            for line in lines:
                tlog_file.write(line)
            # close log file
            tlog_file.close()


        #send alert if temperature above thresholds
        if my_state:
            if (float(my_press)>=float(press_high_alert) or float(my_press)<=float(press_low_alert)):
                logger.error('Houston we have a problem!\nPressure reading from SMC is: '+str(my_press)+' MPa. Turning OFF the chiller..')
                SMC.set_state(0)

        # sleep for period
        time.sleep(period)



if __name__=="__main__":
    main()
