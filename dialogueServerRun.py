import os
import logging
import subprocess
import dbconn
import botTrain
import schedule
from rasa.run import run as runB
import psycopg2
import os
import urllib

def runIt(port):  
    logging.basicConfig(level=logging.DEBUG)
    port_value = int(port)
    runB(model="models/dialogue", endpoints="endpoints.yml", credentials="credentials.yml", port=port_value)
    return(print("Up and running on port {}".format(port_value)))

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
        urllib.request.urlopen("https://google.co.uk/")
        botTrain.main()
    elif '1' in count:
        pass

urllib.request.urlopen("https://google.co.uk/")
subprocess.Popen(["python", "appPinger.py"])
assigned_port = int(os.environ.get("PORT", 5000)) #port assigned by  Heroku
subprocess.Popen(["python", "actionServerRun.py"]) #here we're launching the action server and moving on; necessary otherwise Python would hang after this command, as it would wait for the server to stop before continuing
runIt(assigned_port)