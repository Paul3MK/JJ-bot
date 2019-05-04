from rasa_core_sdk import Action
from rasa_core_sdk import forms
from rasa_core_sdk.events import SlotSet
import psycopg2

"""class TechCategoriesForm(FormAction):
    # This form will take care of the user's choice of category (within Tech) and the brand as well.
    # The value of the brand slot can be used to create a database query right here, and the values will be returned from the db.
    # We will do this in the ActionReturnSmartphones block, so we must call this action from here.
    
    def name(self):

        return "categories_form"

    @staticmethod
    def required_slots(tracker):

        return ["category", "brand"] 

    def submit(self, dispatcher, tracker, domain):
        slot_value = tracker.get_slot('brand')

        con = psycopg2.connect(database="jjtestdb", user="postgres", password="hieg")
        off = 0
        with con:

	        cur = con.cursor()

            for i in range(0, 50):
                cur.execute("SELECT * FROM smartphones LIMIT 1 OFFSET %s WHERE brand=%s", (off, slot_value))
                off ++


            
        # we will call the ActionReturnSmartphones in this method, or perhaps code the db connection here straightaway
        # the db result must be returned here, and then formatted for FBMessenger"""

class ActionChooseSmartphoneBrand(Action):
    def name(self):
        return "action_returnSmartphones"

    def run(self, dispatcher, tracker, domain):
        chosen_brand = tracker.get_slot('brand')

        con = psycopg2.connect(database="jjtestdb", user="postgres", password="hieg")
        off = 0
        with con:

	        cur = con.cursor()

            for i in range(0, 9):
                returned_phone = cur.execute("SELECT * FROM smartphones LIMIT 1 OFFSET %s WHERE brand=%s", (off, chosen_brand))
                off ++
                dispatcher.utter_message("{}, it works!!".format(returned_phone))
        return[]
        
              