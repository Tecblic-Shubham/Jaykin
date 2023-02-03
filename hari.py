# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from new import new
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted


class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "Action_run"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        hj = tracker.latest_message['text']
        target_language='ar'
        if detect(hj) == target_language :
            jay = detect_translate(hj)
            translated_message = detect_and_translate(new(jay))
            dispatcher.utter_message(text=translated_message)
        else:
            translated_message = new(hj)
            dispatcher.utter_message(text=translated_message)

        return [UserUtteranceReverted]
    
from rasa_sdk import Action
from langdetect import detect
from translate import Translator
import translators as ts
from rasa_sdk import Action, Tracker
from typing import Any, Text, Dict, List
from rasa_sdk.executor import CollectingDispatcher
from deep_translator import GoogleTranslator

def detect_and_translate(message, target_language='ar'):
    detected_language = detect(message)
    if detected_language != target_language:
        message = GoogleTranslator(source='auto', target='ar').translate(message)
    return message


def detect_translate(message, target_language='en'):
    detected_language = detect(message)
    if detected_language != target_language:
        message = GoogleTranslator(source='auto', target='en').translate(message)
    return message


