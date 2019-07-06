from rasa_sdk import Action
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, FollowupAction
import psycopg2
import imgscrapertest as imgscraper
import re
import os

cat_slot_value = ""
brand_slot_value = ""
off = 0
offAppend = 0

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

class TechCatForm(FormAction):
    
    def name(self):

        return "tech_form"

    @staticmethod
    def required_slots(tracker):

        if tracker.get_slot('techCategory') == 'smartphones':
            return ["techCategory", "smartphoneBrand"]
        elif tracker.get_slot('techCategory') == 'tablets':
            return ["techCategory", "tabletBrand"]
        elif tracker.get_slot('techCategory') == 'laptops':
            return ["techCategory", "laptopBrand"]
        elif tracker.get_slot('techCategory') == 'tvs':
            return ["techCategory", "tvBrand"]
        else:
            return ["techCategory", "smartwatchBrand"]

    def submit(self, dispatcher, tracker, domain):
        
        global cat_slot_value
        global brand_slot_value
        global off
        global offAppend

        cat_slot_value = tracker.get_slot('techCategory')
        brand_dict = {"smartphones":"smartphoneBrand", "tablets":"tabletBrand", "laptops":"laptopBrand", "tvs":"tvBrand", "smartwatches":"smartwatchBrand"}
        
        tCat = ['smartphones', 'tablets', 'laptops', 'tvs', 'smartwatches']

        for category in tCat:
            if (cat_slot_value == category):
                brand_slot_value = tracker.get_slot(brand_dict[category])

                dispatcher.utter_message("You have chosen {}".format(category))
                dispatcher.utter_message("Brand is {}".format(brand_slot_value))

        
        off = 0
        offAppend = 0
        return[FollowupAction("action_display_brands_devices")]


class DeviceViewAction(Action):
    def name(self):
        return "action_display_brands_devices"
    
    def run(self, dispatcher, tracker, domain):

        global off
        global offAppend
        DATABASE_URL = os.environ['DATABASE_URL']
        # con = psycopg2.connect(database="jjtestdb", user="postgres", password="hieg") #for local work
        con =  psycopg2.connect(DATABASE_URL, sslmode='require')

        with con:

            cur = con.cursor()
            devices_cards = []

            for i in range(0, 9):
                execution = "SELECT * FROM "+cat_slot_value+" WHERE brand = %s LIMIT 1 OFFSET %s"
                cur.execute(execution, (brand_slot_value, off))
                returned_device = cur.fetchone()
                off += 1
                if returned_device == None:
                    break
                regex = re.compile("\d+.")
                lDscnt = re.findall(regex, returned_device[4])
                dscnt = ""
                for j in lDscnt:
                    dscnt = j
                if dscnt == None:
                    dscnt = None
                else:
                    dscnt = " ({} off)".format(dscnt)
                devices_cards.append({
                        "title": returned_device[1]+" "+returned_device[2],
                        "subtitle": "KSh "+returned_device[3]+dscnt,
                        "image_url": returned_device[0],
                        "buttons": [
                            {
                                "type":"web_url",
                                "url": returned_device[5],
                                "title":"Shop now",
                                "webview_height_ratio": "tall",
                            }
                        ]   
                    }
                )    
            length_check = "SELECT * FROM "+cat_slot_value+" WHERE brand = %s LIMIT 10 OFFSET %s"
            cur.execute(length_check, (brand_slot_value, offAppend))
            all_products = cur.fetchall()
            if (len(all_products) > 9):
                devices_cards.append(
                    {
                        "title":"Wanna see some more?",
                        "image_url":"https://printables.space/files/uploads/download-and-print/large-printable-numbers/plus-a4.jpg",
                        "buttons": [
                            {
                                "type":"postback",
                                "title":"Sure!",
                                "payload":"/DeviceViewAction",
                            },
                            {
                                "type":"postback",
                                "title":"Nah, thanks.",
                                "payload":"/viewMenu",
                            }
                        ]
                    }
                )
            else:
                devices_cards.append(
                    {
                        "title":"That's it.",
                        "image_url":"https://cdn1.iconfinder.com/data/icons/robot-emoji-line-faces/32/robot_emoji_sad-512.png",
                        "buttons": [
                            {
                                "type":"postback",
                                "title":"Menu",
                                "payload":"/viewMenu",
                            }
                        ]
                    }
                )
            dispatcher.utter_elements(*devices_cards)
                # dispatcher.utter_message("{}, it works!!".format(returned_device))
        #off = off + 1
        offAppend = offAppend + 9
        return[SlotSet("techCategory", None), SlotSet("smartphoneBrand", None), SlotSet("smartwatchBrand", None), SlotSet("tabletBrand", None), SlotSet("laptopBrand", None), SlotSet("tvBrand", None)]
        #return[]


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

        dispatcher.utter_elements(*versaceCard)
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

        dispatcher.utter_elements(*beatsCard)
        return []

class ResetSlot(Action):

    def name(self):
        return "action_reset_slot"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet(brand_slot_value, None), SlotSet(cat_slot_value, None)]
