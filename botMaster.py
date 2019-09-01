import os
import logging
import subprocess
import botTrain
import schedule
from rasa.run import run as runB
import psycopg2
import sys
import urllib
import time

# if __name__ == "__main__":
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
assigned_port = int(os.environ.get("PORT", 5000)) #port assigned by  Heroku
asr = subprocess.Popen(["python", "actionServerRun.py"]) #here we're launching the action server and moving on; necessary otherwise Python would hang after this command, as it would wait for the server to stop before continuing
asr

def killAll():
    ap.kill()
    dsr.kill()
    asr.kill()
    sys.exit()

schedule.every().day.at("07:25").do(killAll) 
print("Job successfully scheduled")

while True:
    schedule.run_pending()
    time.sleep(2)

