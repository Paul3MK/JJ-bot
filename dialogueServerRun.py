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
# from fbmessenger import BaseMessenger
# from fbmessenger.thread_settings import (
#     GreetingText,
#     GetStartedButton,
#     PersistentMenuItem,
#     PersistentMenu,
#     MessengerProfile,
# )

def runIt(port):  
    logging.basicConfig(level=logging.DEBUG)
    port_value = int(port)
    runB(model="models/dialogue", endpoints="endpoints.yml", credentials="credentials.yml", port=port_value)
    return(print("Up and running on port {}".format(port_value)))

assigned_port = int(os.environ.get("PORT", 5000)) #port assigned by  Heroku


# class Messenger(BaseMessenger):
#     def __init__(self, page_access_token):
#         self.page_access_token = page_access_token
#         super(Messenger, self).__init__(self.page_access_token)

#     def init_bot(self):
#         self.add_whitelisted_domains('https://facebook.com/')
#         greeting = GreetingText(text='Greetings, my friend! My name is Shopa Jr., and I\'m here to give you an exciting shopping experience!')
#         self.set_messenger_profile(greeting.to_dict())

#         get_started = GetStartedButton(payload='/getStarted')
#         self.set_messenger_profile(get_started.to_dict())

#         menu_item_1 = PersistentMenuItem(
#             item_type='postback',
#             title='Menu',
#             payload='/viewMenu',
#         )
#         menu_item_2 = PersistentMenuItem(
#             item_type='postback',
#             title='Promos',
#             payload='/viewPromos',
#         )
#         persistent_menu = PersistentMenu(menu_items=[
#             menu_item_1,
#             menu_item_2
#         ])

#         self.set_messenger_profile(persistent_menu.to_dict())


# messenger = Messenger("EAAWtJ6GdnowBAAQvgHd9BHPRmqvzBfUPW1UadXuUXhofveak7BvFrpXn1VGXZACYVT0X4nkarxGQ1k0CxZB4YZA4zb3ywZBqeKj0t8e4hsyUrp4DRnAA5m5inThmRThN8uJqKBDvyssu05p9tuDRZBDxEPc8h0LNZAUxXSmJKXggZDZD")
# messenger.init_bot()

runIt(assigned_port)