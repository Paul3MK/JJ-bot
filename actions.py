from rasa_sdk import Action
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, FollowupAction, Restarted, AllSlotsReset
import psycopg2
import imgscrapertest as imgscraper
import re
import os

cat_slot_value = ""
brand_slot_value = ""
off = 0
offAppend = 0

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
        brand_dict = {"smartphones":"smartphoneBrand", "tablets":"tabletBrand", "laptops":"laptopBrand", "TVs":"tvBrand", "smartwatches":"smartwatchBrand"}
        
        tCat = ['smartphones', 'tablets', 'laptops', 'TVs', 'smartwatches']

        for category in tCat:
            if (cat_slot_value == category):
                brand_slot_value = tracker.get_slot(brand_dict[category])

                dispatcher.utter_message("The top {} from {}!".format(category, brand_slot_value))
        
        off = 0
        offAppend = 0
        return[FollowupAction("action_display_brands_devices")]


class HardwareCatForm(FormAction):

    def name(self):
        return "hardware_form"

    @staticmethod
    def required_slots(tracker):

        if tracker.get_slot('hardwareCategory') == 'power_banks':
            return ["hardwareCategory", "power_bankBrand"]
        elif tracker.get_slot('hardwareCategory') == 'chargers':
            return ["hardwareCategory", "chargerBrand"]
        elif tracker.get_slot('hardwareCategory') == 'headphones':
            return ["hardwareCategory", "headphoneBrand"]
        elif tracker.get_slot('hardwareCategory') == 'memory_cards':
            return ["hardwareCategory", "memory_cardBrand"]
        elif tracker.get_slot('hardwareCategory') == 'mice':
            return ["hardwareCategory", "mouseBrand"]
        else:
            return ["hardwareCategory", "keyboardBrand"]

    def submit(self, dispatcher, tracker, domain):

        global cat_slot_value
        global brand_slot_value

        cat_slot_value = tracker.get_slot('hardwareCategory')
        acc_brand_dict = {"power banks":"power_bankBrand", "chargers":"chargerBrand", "headphones":"headphoneBrand", "memory cards":"memory_cardBrand", "mice":"mouseBrand", "keyboards":"keyboardBrand"}

        aCat = ["power banks", "chargers", "headphones", "memory cards", "mice", "keyboards"]

        for category in aCat:
            if (cat_slot_value == category):

                brand_slot_value = tracker.get_slot(acc_brand_dict[category])
                dispatcher.utter_message("Here are {} from {}".format(category, brand_slot_value))

        return[FollowupAction("action_display_brands_devices")]      


class HealthForm(FormAction):
    def name(self):
        return "health_form"

    @staticmethod
    def required_slots(tracker):
        
        if tracker.get_slot('healthCategory') == 'makeup':
            return["healthCategory", "makeupBrand"]
        elif tracker.get_slot('healthCategory') == 'maleFragrances':
            return["healthCategory", "maleFragranceBrand"]
        elif tracker.get_slot('healthCategory') == 'femaleFragrances':
            return["healthCategory", "femaleFragranceBrand"]
        elif tracker.get_slot('healthCategory') == 'skinCare':
            return["healthCategory", "skinCareBrand"]
        else:
            return["healthCategory", "hairCareBrand"]
    
    def submit(self, dispatcher, tracker, domain):

        global cat_slot_value
        global brand_slot_value

        cat_slot_value = tracker.get_slot('healthCategory')
        he_brand_dict = {"makeup":"makeupBrand", "maleFragrances":"maleFragranceBrand", "femaleFragrances":"femaleFragranceBrand", "skinCare":"skinCare", "hairCare":"hairCareBrand"}

        hCat = ["makeup", "maleFragrances", "femaleFragrances", "skinCare", "hairCare"]

        for category in hCat:
            if (cat_slot_value == category):
                brand_slot_value = tracker.get_slot(he_brand_dict[category])

                dispatcher.utter_message("Check out these personal care products 💥")

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
                regex = re.compile(r"\d+.")
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
                        "title":"That's it from me.",
                        "image_url":"https://cdn1.iconfinder.com/data/icons/robot-emoji-line-faces/32/robot_emoji_sad-512.png",
                        "buttons": [
                            {
                                "type":"postback",
                                "title":"Menu",
                                "payload":"/viewMenu",
                            },
                            {
                                "type":"web_url",
                                "url":"https://jumia.co.ke",
                                "title":"Browse more stuff",
                                "webview_height_ratio":"full"
                            }
                        ]
                    }
                )
            dispatcher.utter_elements(*devices_cards)
                # dispatcher.utter_message("{}, it works!!".format(returned_device))
        #off = off + 1
        offAppend = offAppend + 9
        return[SlotSet("techCategory", None), SlotSet("hardwareCategory", None), SlotSet("healthCategory", None), SlotSet("smartphoneBrand", None), SlotSet("smartwatchBrand", None), SlotSet("tabletBrand", None), SlotSet("laptopBrand", None), SlotSet("tvBrand", None), SlotSet("power_bankBrand", None), SlotSet("chargerBrand", None), SlotSet("headphoneBrand", None), SlotSet("memory_cardBrand", None), SlotSet("mouseBrand", None), SlotSet("keyboardBrand", None), SlotSet("makeupBrand", None), SlotSet("maleFragranceBrand", None), SlotSet("femaleFragranceBrand", None), SlotSet("skinCareBrand", None), SlotSet("hairCareBrand", None)]
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
                        "type": "web_url",
                        "title": "Shop now",
                        "url":"https://c.jumia.io/?a=146734&c=9&p=r&E=kkYNyk2M4sk%3D&ckmrdr=https%3A%2F%2Fwww.jumia.co.ke%2Fversace-bright-crystal-for-women-edt-90-ml-573534.html&utm_campaign=146734",
                        "webview_height_ratio": "tall"
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
                "title": "Beats Beats Studio Headphones Remastered - Blue",
                "subtitle": "KSh 32,995",
                "image_url": "https://ke.jumia.is/KA6JlF4QE1ZWkgQ5Z3qnV9_W1WA=/fit-in/680x680/filters:fill(white):sharpen(1,0,false):quality(100)/product/16/984/3.jpg?4007",
                "buttons" : [
                    {
                        "type": "web_url",
                        "title": "Shop",
                        "url": "https://c.jumia.io/?a=146734&c=9&p=r&E=kkYNyk2M4sk%3D&ckmrdr=https%3A%2F%2Fwww.jumia.co.ke%2Fbeats-studio-headphones-remastered-blue-beats-by-dre-mpg106045.html&utm_campaign=146734",
                        "webview_height_ratio": "tall"
                    }
                ]
            }
        ]

        dispatcher.utter_elements(*beatsCard)
        return []

class ViewPromos(Action):
    def name(self):
        return "action_view_promos"

    def run(self, dispatcher, tracker, domain):
        promo_elements = [
            {
                "title": "Super Brand Day",
                "subtitle": "October 8th only!",
                "image_url": "https://ke.jumia.is/cms/2019/W41/SBD_Live/KE_W40_GenS_SBD_D.jpg",
                "default_action": {
                    "type": "web_url",
                    "url": "https://c.jumia.io/?a=146734&c=9&p=r&E=kkYNyk2M4sk%3D&ckmrdr=https%3A%2F%2Fwww.jumia.co.ke%2Fsuper-brand-day%2F%3Fsource%3DS_W41&utm_campaign=146734",
                    "webview_height_ratio": "tall"
                },
                "buttons": [
                    {
                        "type": "web_url",
                        "title": "Go to page",
                        "url": "https://c.jumia.io/?a=146734&c=1624&p=r&E=kkYNyk2M4sk%3D&utm_campaign=146734&utm_term=",
                        "webview_height_ratio": "full"
                    }
                ]
            },
            {
                "title": "FIFA 20",
                "subtitle": "Pre-order",
                "image_url": "https://ke.jumia.is/cms/2019/W37/KE_W37_FiFa_S_Pre-order_D.jpg",
                "default_action": {
                    "type": "web_url",
                    "url": "https://c.jumia.io/?a=146734&c=1640&p=r&E=kkYNyk2M4sk%3D&utm_campaign=146734&utm_term=",
                    "webview_height_ratio": "tall"
                },
                "buttons": [
                    {
                        "type": "web_url",
                        "url": "https://c.jumia.io/?a=146734&c=1640&p=r&E=kkYNyk2M4sk%3D&utm_campaign=146734&utm_term=",
                        "title": "Go to page",
                        "webview_height_ratio": "full"
                    }
                ]
            },
            {
                "title": "Carrefour",
                "subtitle": "Groceries",
                "image_url": "https://ke.jumia.is/cms/2019/W37/corrections/Carrefour-Groceries_WK37_DBanner.jpg",
                "default_action": {
                    "type": "web_url",
                    "url": "https://c.jumia.io/?a=146734&c=9&p=r&E=kkYNyk2M4sk%3D&ckmrdr=https%3A%2F%2Fwww.jumia.co.ke%2Fcarrefour%2F%3Fsource%3DHP_DoubleBanner_W37&utm_campaign=146734",
                    "webview_height_ratio": "tall"
                },
                "buttons": [
                    {
                        "type": "web_url",
                        "url": "https://c.jumia.io/?a=146734&c=9&p=r&E=kkYNyk2M4sk%3D&ckmrdr=https%3A%2F%2Fwww.jumia.co.ke%2Fcarrefour%2F%3Fsource%3DHP_DoubleBanner_W37&utm_campaign=146734",
                        "title": "Go to page",
                        "webview_height_ratio": "full"
                    }
                ]
            },
            {
                "title":"Top Deals",
                "image_url":"https://ke.jumia.is//cms/2019/W39/TOP-DEALS.jpg",
                "buttons": [
                    {
                        "type":"web_url",
                        "url":"https://www.jumia.co.ke/top-deals/?source=HP_placement_W39",
                        "title":"Go to page",
                        "webview_height_ratio":"full"
                    }
                ]
            }
        ]

        dispatcher.utter_elements(*promo_elements)
        return []

class ResetSlot(Action):

    def name(self):
        return "action_reset_slot"

    def run(self, dispatcher, tracker, domain):
        #return [SlotSet(brand_slot_value, None), SlotSet(cat_slot_value, None)]
        return[AllSlotsReset()]   

class RestartChat(Action):

    def name(self):
        return "action_restart"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Restarting chat...")
        dispatcher.utter_message("Done!")
        return[Restarted(), FollowupAction("utter_Menu")]