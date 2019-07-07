import os
import logging
import subprocess
from rasa.core.agent import Agent
from rasa.core.interpreter import RegexInterpreter
from rasa.model import get_model
from rasa.core.channels.facebook import FacebookInput
from rasa.core.policies.memoization import MemoizationPolicy
from rasa.core.policies.keras_policy import KerasPolicy
from rasa.core.policies.form_policy import FormPolicy
#from rasa.cli.run import run_actions
from rasa.run import run as runB
import subprocess
import asyncio
import dbconn

def runIt(port):  
    logging.basicConfig(level=logging.DEBUG)
    port_value = int(port)
    runB(model="models/dialogue", endpoints="endpoints.yml", credentials="credentials.yml", port=port_value)

# if __name__ == "__main__":
subprocess.Popen(["python", "botTrain.py"]) # here we're launching the training script and moving on without waiting for it to complete
dbconn.DatabaseProvisioning() # and we provision the database. Training should finish before DB provisioning

assigned_port = int(os.environ.get("PORT", 5000)) #port assigned by  Heroku
subprocess.Popen(["python", "actionServerRun.py"]) #here we're launching the action server and moving on; necessary otherwise Python would hang after this command, as it would wait for the server to stop before continuing
runIt(assigned_port)