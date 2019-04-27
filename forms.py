from rasa_core_sdk import forms

class CategoriesForm(FormAction):

    def name(self):

        return "categories_form"

    @staticmethod
    def required_slots(tracker):

        return ["menuItem", "category", "brand"]

    def submit(self, dispatcher, tracker, domain):
        slot_value = tracker.get_slot('brand')
        

                