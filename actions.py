from rasa_sdk import Action
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet
import psycopg2
import imgscrapertest as imgscraper
import re

cat_slot_value = 0
brand_slot_value = 0

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
        cat_slot_value = tracker.get_slot('techCategory')
        global brand_slot_value 

        brand_dict = {"smartphones":"smartphoneBrand", "tablets":"tabletBrand", "laptops":"laptopBrand", "tvs":"tvBrand", "smartwatches":"smartwatchBrand"}
        
        tCat = ['smartphones', 'tablets', 'laptops', 'tvs', 'smartwatches']

        for category in tCat:
            if (cat_slot_value == category):
                brand_slot_value = tracker.get_slot(brand_dict[category])

                dispatcher.utter_message("You have chosen {}".format(category))
                dispatcher.utter_message("Brand is {}".format(brand_slot_value))

    
        return[]


class SmarthponeViewAction(Action):
    def name(self):
        return "action_display_brands_smartphones"
    
    def run(self, dispatcher, tracker, domain):

        con = psycopg2.connect(database="jjtestdb", user="postgres", password="hieg")
        off = 0
        with con:

            cur = con.cursor()
            smartphone_cards = [0, 1, 2, 3, 4, 5, 6, 7, 8]

            for i in range(0, 9):
                cur.execute("SELECT * FROM smartphones WHERE brand = %s LIMIT 1 OFFSET %s", (brand_slot_value, off))
                returned_phone = cur.fetchone()
                off += 1
                if returned_phone == None:
                    break
                regex = re.compile("\d+.")
                lDscnt = re.findall(regex, returned_phone[4])
                for j in lDscnt:
                    dscnt = j
                if dscnt == None:
                    dscnt = "No discount"
                else:
                    dscnt = "{} off".format(dscnt)
                smartphone_cards[i] = {
                        "title": returned_phone[1]+" "+returned_phone[2],
                        "subtitle": "KSh "+returned_phone[3]+" ("+dscnt+")",
                        "image_url": returned_phone[0],
                        "buttons": [
                            {
                                "type":"web_url",
                                "url": returned_phone[5],
                                "title":"Buy",
                                "webview_height_ratio": "tall",
                            }
                        ]
                    }
            dispatcher.utter_elements(*smartphone_cards)
                # dispatcher.utter_message("{}, it works!!".format(returned_phone))
        return[]


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
