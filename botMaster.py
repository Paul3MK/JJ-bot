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

def pingFunc():
    urllib.request.urlopen("https://jjbot-test.herokuapp.com/")
    print("pinged your app")

def appPing():
    """This function is repsonsible for keeping the bot online (kinda like Pingdom or Kaffeine). It pings the app's domain every 29 minutes (because the apps on Heroku's free tier fall asleep after 30 minutes) by running the pingFunc function. This to minimise the bot's response time and to prevent db provisioning & dialogue training all the time"""
    schedule.every(14).minutes.do(pingFunc)
    schedule.run_pending()

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


    dsr = subprocess.Popen(["python", "dialogueServerRun.py"])
    dsr
    asr = subprocess.Popen(["python", "actionServerRun.py"]) #here we're launching the action server and moving on; necessary otherwise Python would hang after this command, as it would wait for the server to stop before continuing
    asr

    if kill:
        uniqueTime.sleep(30)
        print("Killing all processes and exiting.")
        dsr.kill()
        asr.kill()
        sys.exit(0)
        print("Should not get printed... If you see this, there is a bug.")

    main.has_been_called = True # in python, everything is an object. Here we make an attribute of the function, for use later on

main.has_been_called = False # here we set the attribute to false initially; required. We're essentially giving this an initial value

while True:
    DATABASE_URL = os.environ['DATABASE_URL']
    # con = psycopg2.connect(database="jjtestdb", user="postgres", password="hieg") #for local work
    con =  psycopg2.connect(DATABASE_URL, sslmode='require')
    with con:

        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS botCrash(attemptedRestarts CHAR(1))")
        cur.execute("SELECT * FROM botCrash")
        resVar = str(cur.fetchall())

        if appPinger.is_time_between(time(22,00), time(22,30)): #-3 hours because Kenya is GMT+3
            cur.execute("DROP TABLE IF EXISTS botCrash")
            cur.execute("CREATE TABLE botCrash(attemptedRestarts CHAR(1))")
            cur.execute("INSERT INTO botCrash VALUES ('0')")
            con.commit()
            print("Exit.")
            main(1)
            print("This should never get printed.")
        elif '0' in resVar:
            cur.execute("UPDATE botCrash SET attemptedRestarts='1' WHERE attemptedRestarts='0'")
            con.commit()
            print("First restart")
            sys.exit(0)
        elif '1' in resVar:
            cur.execute("UPDATE botCrash SET attemptedRestarts='2' WHERE attemptedRestarts='1'")
            con.commit()
            print("Second restart")
            sys.exit(0)
        elif '2' in resVar:
            cur.execute("UPDATE botCrash SET attemptedRestarts='3' WHERE attemptedRestarts='2'")
            con.commit()
            print("Third restart")
            sys.exit(0)
        elif '3' in resVar:
            cur.execute("UPDATE botCrash SET attemptedRestarts='4' WHERE attemptedRestarts='3'")
            con.commit()
            print("Fourth restart")
            sys.exit(0)
        elif '4' in resVar:
            cur.execute("UPDATE botCrash SET attemptedRestarts='5' WHERE attemptedRestarts='4'")
            con.commit()
            print("Fifth restart")
            main(1) #this is to trigger the main function's kill logic; line 46
        elif '5' in resVar:
            cur.execute("UPDATE botCrash SET attemptedRestarts='6' WHERE attemptedRestarts='5'")
            con.commit()
            print("Sixth restart")
            sys.exit(0)
        else:
            if main.has_been_called:
                pingFunc()
                uniqueTime.sleep(840)
            else:
                main()
    uniqueTime.sleep(60)

main()