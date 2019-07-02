import os
import logging
import subprocess
from rasa.core.agent import Agent
from rasa.core.interpreter import RegexInterpreter
from rasa.model import get_model
from rasa.core.channels.facebook import FacebookInput
#from rasa.cli.run import run_actions
from rasa.run import run as runB

def runIt(port):  
    logging.basicConfig(level=logging.DEBUG)
    
    unpacked_model = get_model("models")
    port_value = int(port)
    runB(model="models", endpoints="endpoints.yml", credentials="credentials.yml", port=port_value)
    agent = Agent.load(unpacked_model, interpreter=RegexInterpreter())

    input_channel = FacebookInput(verify="JJbot", secret="ec21c7ab5f81ea576a043ce42da28846", page_access_token="EAAWtJ6GdnowBAAQvgHd9BHPRmqvzBfUPW1UadXuUXhofveak7BvFrpXn1VGXZACYVT0X4nkarxGQ1k0CxZB4YZA4zb3ywZBqeKj0t8e4hsyUrp4DRnAA5m5inThmRThN8uJqKBDvyssu05p9tuDRZBDxEPc8h0LNZAUxXSmJKXggZDZD")
    agent.handle_channels([input_channel], port_value, serve_forever=True)

    

# if __name__ == "__main__":
assigned_port = int(os.environ.get("PORT", 5000)) #port assigned by  Heroku
runIt(5001)
