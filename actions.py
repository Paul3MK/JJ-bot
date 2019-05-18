from rasa_core_sdk import Action
from rasa_core_sdk.forms import FormAction
from rasa_core_sdk.events import SlotSet
import psycopg2

"""class TechCategoriesForm(FormAction):
    # This form will take   care of the user's choice of category (within Tech) and the brand as well.
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

class SmartphoneForm(FormAction):
    
    def name(self):

        return "smartphone_form"

    @staticmethod
    def required_slots(tracker):

        return ["techCategory", "smartphoneBrand"] 

    def submit(self, dispatcher, tracker, domain):
        slot_value = tracker.get_slot('smartphoneBrand')

        con = psycopg2.connect(database="jjtestdb", user="postgres", password="hieg")
        off = 0
        with con:

            cur = con.cursor()
            
            for i in range(0, 9):
                cur.execute("SELECT * FROM smartphones WHERE brand=%s LIMIT 1 OFFSET %s", (slot_value, off))
                returned_phone = cur.fetchone()
                off += 1
                if returned_phone == None:
                    break
                dispatcher.utter_message("{}, it works!!".format(returned_phone))
        return[]

class DisplayMenu(Action):

    def name(self):
        return "action_show_Menu"

    def run(self, dispatcher, tracker, domain):

        qckReply = [
                    {
                        "content_type":"text",
                        "title":"Deals",
                        "payload":"/viewDeals"
                    },
                    {
                        "content_type":"text",
                        "title":"Categories",
                        "payload":"/viewCategories"
                    },
                    {
                        "content_type":"text",
                        "title":"Help",
                        "payload":"/viewHelp"
                    },
                    {
                        "content_type":"text",
                        "title":"Subscribe",
                        "payload":"/viewSubscribe"
                    },
                    {
                        "content_type":"text",
                        "title":"Feedback",
                        "payload":"/viewFeedback"
                    }  
        ]

        dispatcher.utter_custom_quick_reply(*qckReply)
        return []

class DisplayOnboardingVersace(Action):

    def name(self):
        return "action_show_versace"

    def run(self, dispatcher, tracker, domain):
        versaceCard = [
            {
                "title": "VERSACE Bright Crystal For Women EDT - 90 ml",
                "subtitle": "versace women's bright crystal",
                "image_url": "https://ke.jumia.is/YsNpaoCY8BZkWdZ0_HAZeeUGYws=/fit-in/500x500/filters:fill(white):sharpen(1,0,false):quality(100)/product/43/5375/1.jpg?1323",
                "buttons" : [
                    {
                        "type": "postback",
                        "title": "Buy",
                        "payload": '/action_show_menu'
                    }
                ]
            }
        ]

        dispatcher.utter_custom_message(*versaceCard)
        return []

class DisplayOnboardingBeats(Action):

    def name(self):
        return "action_show_beats"

    def run(self, dispatcher, tracker, domain):
        beatsCard = [
            {
                "title": "beats Solo2 Wired Over-Ear Headphone On-Ear Stereo Music Headset ANC Noise Reduction Earphone White Second-hand No Package No Accessories",
                "subtitle": "beats solo2 wired",
                "image_url": "https://ke.jumia.is/FZcjHsJvmR7tQBijpFq-Jmov4jI=/fit-in/500x500/filters:fill(white):sharpen(1,0,false):quality(100)/product/52/157001/1.jpg?0416",
                "buttons" : [
                    {
                        "type": "postback",
                        "title": "Buy",
                        "payload": '/action_show_menu'
                    }
                ]
            }
        ]

        dispatcher.utter_custom_message(*beatsCard)
        return []
