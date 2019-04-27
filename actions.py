from rasa_core_sdk import Action
from rasa_core_sdk import forms
from rasa_core_sdk.events import SlotSet
import psycopg2

class CategoriesForm(FormAction):
    """This form will take care of the user's choice of category and the brand as well.
    The value of the brand slot can be used to create a database query right here, and the values will be returned from the db.
    We will do this in the ActionReturnSmartphones block, so we must call this action from here."""
    
    def name(self):

        return "categories_form"

    @staticmethod
    def required_slots(tracker):

        return ["category", "brand"]

    def submit(self, dispatcher, tracker, domain):
        slot_value = tracker.get_slot('brand')
        # we will call the ActionReturnSmartphones in this method, or perhaps code the db connection here straightaway
        # the db result must be returned here, and then formatted for FBMessenger

class ActionReturnSmartphones(Action):
    def name(self):
        return "action_returnSmartphones"

    def run(self, dispatcher, tracker, domain):
        # a db connection must be opened, with relevant 
              