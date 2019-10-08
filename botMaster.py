import os
import logging
import subprocess
import botTrain
import schedule
from rasa.run import run as runB
import psycopg2
import sys
import urllib
import time as uniqueTime
import appPinger
from datetime import time, datetime

def main(kill=None):
    DATABASE_URL = os.environ['DATABASE_URL']
    # con = psycopg2.connect(database="jjtestdb", user="postgres", password="hieg") #for local work
    con =  psycopg2.connect(DATABASE_URL, sslmode='require')
    with con:

        cur = con.cursor()
        cur.execute("SELECT * FROM trained_counter")
        count = str(cur.fetchall())
        
        if '0' in count:
            subprocess.Popen(["python", "dbconn.py"])
            botTrain.main()
            pass
        elif '1' in count:
            pass


    ap = subprocess.Popen(["python", "appPinger.py"])
    ap
    dsr = subprocess.Popen(["python", "dialogueServerRun.py"])
    dsr
    asr = subprocess.Popen(["python", "actionServerRun.py"]) #here we're launching the action server and moving on; necessary otherwise Python would hang after this command, as it would wait for the server to stop before continuing
    asr

    if kill:
        uniqueTime.sleep(30)
        print("Killing all processes and exiting.")
        ap.kill()
        dsr.kill()
        asr.kill()
        sys.exit(0)
        print("Should not get printed... If you see this, there is a bug.")

    main.has_been_called = True # in python, everything is an object. Here we make an attribute of the function, for use later on

main.has_been_called = False # here we set the attribute to false initially; required. We're essentially giving this an initial value

while True:
    if appPinger.is_time_between(time(4,00), time(9,00)): #+3 hours because Kenya is GMT+3
        print("Exit.")
        sys.exit(0)
        print("This should never get printed.")
    elif appPinger.is_time_between(time(9,00), time(10,00)):
        if main.has_been_called:
            sys.exit(0)
        else:
            main.has_been_called = True
            main(1) # because the if block in the main function checks whether a parameter exists, this will trigger it
    elif appPinger.is_time_between(time(10,00), time(11,00)):
        sys.exit(0)
        print("This should not get printed either.")
    else:
        if main.has_been_called:
            pass
        else:
            main()
    uniqueTime.sleep(60)

main()