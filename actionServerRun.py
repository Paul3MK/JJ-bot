import logging
from rasa_sdk.endpoint import run

def runActionServer():
    logging.basicConfig(level=logging.DEBUG)
    run(action_package_name="actions", port=5055)


runActionServer()