from rasa_core_sdk import Action
from rasa_core_sdk.forms import FormAction
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.forms import EntityFormField
from rasa_core_sdk.forms import BooleanFormField

import requests
import checkToken
import ast

# This uses our checkToken script to see if the API bearer token needs to be updated or not
checkToken.checkTokenValidity()

# After checking if the auth token is valid we can then get the whole headers declaration from our api_credentials file
with open('api_credentials.txt', 'r') as file:
    credentials = file.readlines() 
bearer = credentials[2]
bearer = credentials[2].replace('\n', '') # Remove any new line coming after the bearer token to make sure there are no mistakes because of it.

# Variable declarations for the API calls like the endpoints and the headers. The bearer token is used to authenticate the API use 
district_endpoint = "http://tourism.opendatahub.bz.it/api/MunicipalityReduced?language=en&elements=0"
gastronomy_endpoint = "http://tourism.opendatahub.bz.it/api/GastronomyLocalized"
headers = {"Authorization":"Bearer " + bearer}

file.close() # close file stream

# Variable declarations of the dictionaries that will contain data from API calls like the Municipalties, Cuisines etc. We need these to make our final API call to the Gastronomy endpoint
municipality_dictionary = {}

idm_cuisine_dictionary = {
    "Vegetarian": "1",
    "Glutenfree": "2",
    "Lactosefree": "4",
    "Spicy": "8",
    "Local": "16",
    "Gourmet": "32",
    "Italian": "64",
    "International": "128",
    "Pizza": "256",
    "Fish": "512",
    "Asian": "1024",
    "Wild": "2048",
    "Diet": "8192",
    "Grill": "16348",
    "Ladin": "32768",
    "Kidmenu": "16777216",
    "Lunchmenu": "33554432"
}

dish_mapping_example = {
    "Sushi": "Asian",
    "Thai": "Asian",
    "Thailandese": "Asian",
    "Chinese": "Asian",
    "Japanese": "Asian",
    "Indian": "Asian",
    "Knodel": "Local",
    "Canederli": "Local",
    "Traditional": "Local",
    "Wurstel": "Local",
    "Gulasch": "Local",
    "Speck": "Local",
    "Spatzle": "Local",
    "Krapfen": "Local",
    "Typical": "Local",
    "Meat": "Local",
    "Pasta": "Italian",
    "Lasagna": "Italian"
}

print(headers)

# Make a get request with the parameters to get the municipalities(we use these as cities in the bot) from the API
municipalities_api_call = requests.get(district_endpoint, headers=headers)

# Transform the response data to a usable json object
apiResponse = municipalities_api_call.json()

# Fill the municipality dictionary with tuples of the format (City Name: Id)
for item in apiResponse:
    municipality_dictionary.update({item['Name']: item['Id']})

# Method definitions for calling the Gastronomy API
def searchRestaurantsAPIcall(city, cuisine):
    parameters = {
    "cuisinecodefilter": cuisine,
    "locfilter": "mun"+city
    }
    # Make a get request with the parameters to get the municipalities(we use these as cities in the bot) from the API
    gastronomy_api_call = requests.get(gastronomy_endpoint, params=parameters, headers=headers)

    # Transform the response data to a usable json object
    apiResponse = gastronomy_api_call.json()

    return apiResponse



# INFORMATION ABOUT RASA ACTIONS:
# Classes define the custom actions that we want to use inside of RASA Core. Below are two custom actions 
# that we'll be using when the user asks for help and one for finding restaurants. These actions are made up of two methods:
# one called name which sets the name of the action(it should be euqual to the name defined in the domain.yml file) 
# and another called run which is the actual action. The parameters are specific to RASA. 
# Dispatcher sends back user messages, the tracker keeps track of the conversation using slots and the domain is well... the domain
# For more info: https://www.rasa.com/docs/core/customactions/



class ActionHelp(Action):
    def name(self):
        return "action_help"

    def run(self, dispatcher, tracker, domain):
        # This tracker variable is the RASA's dialogue tracker and it basically keeps track of the slots
        # and their values. The dispatcher is what we use to send back messages)
        if tracker.get_slot("help_type") == "search":
            dispatcher.utter_message("Sure thing. If you want to find a restaurant just tell me where and what you want to eat (e.g: Bolzano Pizza) and I'll find something for you :)")
        elif tracker.get_slot("help_type") == "tellmemore":
            dispatcher.utter_message("Open Data Hub is your access point to South Tyrol’s relevant data. To learn more click here: hhttps://opendatahub.bz.it/")
        elif tracker.get_slot("help_type") == "nevermind":
            dispatcher.utter_message("Ok then, carry on.")    
       
        return []


class ActionSearchRestaurants(FormAction):

    RANDOMIZE = False
   
   # The reason for definig this static method here is that the restaurant search is a Form Action. 
   # A way to think of that is just like with an HTML/JS form. This way we make sure that the action will not run
   # unless the user provides both of the values we need to search for a restaurant (city and cuisine in our case)
    @staticmethod
    def required_fields():
        return [
            EntityFormField("city", "city"),
            EntityFormField("cuisine", "cuisine"),
        ]

    def name(self):
        return 'action_search_restaurants'

    def submit(self, dispatcher, tracker, domain):
        user_input_city = tracker.get_slot("city").title()
        user_input_cuisine = tracker.get_slot("cuisine").title()
        city = ""
        cuisine = ""

        # Now below we perform some validation checks(bad input or input we can't recognise/use to make API calls)
        # Check if the city the user provided is in our list of municipalities of South Tyrol(if not then the user inputed something wrong)
        for key in municipality_dictionary.keys():
            if user_input_city in key:
                city = municipality_dictionary[key]

        for key in idm_cuisine_dictionary.keys():
            if user_input_cuisine in key:
                cuisine = idm_cuisine_dictionary[user_input_cuisine]
        
        for key in dish_mapping_example:
            if user_input_cuisine in key:
                cuisine = idm_cuisine_dictionary[dish_mapping_example[key]]    
        if  city == "" or city == None:
            dispatcher.utter_message("I can't seem to find the location you gave me. Please try again and make sure you are giving me a city in South Tyrol.")
            return []
        elif cuisine == "" or cuisine == None:
            dispatcher.utter_message("I can't seem to find your requested cuisine anywhere. Please try again and make sure you are giving me a cuisine type.")
            return []
        else:       
            
            dispatcher.utter_message("I'm searching for restaurants based on your preferences.")
            
            # dispatcher.utter_message('Dev P.S: Using city code ' + city + ' and cuisine code  ' + cuisine) [debugging purpose: shows the city and cuisine key that we are calling the api with]
            # call IDM opendatahub API as defined in the function above and get the data
            # then use a for loop to display the results in our predefined format in the domain file
            result = searchRestaurantsAPIcall(city, cuisine)
            
            for item in result['Items']:
                template_elements = {
                    "title": item['Shortname'],
                    "subtitle": item['ContactInfos']['Address'] + " " + item['ContactInfos']['City'],
                    "image_url": item['ImageGallery'][0]['ImageUrl'],
                    "buttons": [
                        {
                        "type": "web_url",
                        "url": item['ContactInfos']['Url'],
                        "title": "Visit Website",
                        },
                        {
                        "type": "phone_number",
                        "title": "Call Restaurant",
                        "payload": item['ContactInfos']['Phonenumber']
                        }
                    ]
                }
                dispatcher.utter_custom_message(template_elements)
            
            dispatcher.utter_message("Search finished 😁")
            return []
        