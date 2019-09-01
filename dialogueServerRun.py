import os
import logging
import subprocess
import dbconn
import botTrain
import schedule
from rasa.run import run as runB
import psycopg2
import sys
import urllib
import time

def runIt(port):  
    logging.basicConfig(level=logging.DEBUG)
    port_value = int(port)
    runB(model="models/dialogue", endpoints="endpoints.yml", credentials="credentials.yml", port=port_value)
    return(print("Up and running on port {}".format(port_value)))

assigned_port = int(os.environ.get("PORT", 5000)) #port assigned by  Heroku

runIt(assigned_port)