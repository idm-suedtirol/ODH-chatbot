# Fallback help type search
* out_of_scope
    - utter_default
* out_of_scope
    - utter_default
* out_of_scope
    - utter_what_help
* give_help_type{"help_type": "search"}
    - slot{"help_type": "search"}
    - action_help
    - action_restart

# Fallback more tellmemore
* out_of_scope
    - utter_default
* out_of_scope
    - utter_default
* out_of_scope
    - utter_what_help
* give_help_type{"help_type": "tellmemore"}
    - slot{"help_type": "tellmemore"}
    - action_help
    - action_restart

# Fallback more nevermind
* out_of_scope
    - utter_default
* out_of_scope
    - utter_default
* out_of_scope
    - utter_what_help
* give_help_type{"help_type": "nevermind"}
    - slot{"help_type": "nevermind"}
    - action_help
    - action_restart

# User greets
* greet
    - utter_greet
    - utter_bot_presentation

# User says thanks
* thanks
    - utter_thanks

# User compliments our fantastic bot
* compliment
    - utter_respond_compliment
    - action_restart

# User says bye
* bye
    - utter_bye
    - action_restart

# User asks for help
* request_help
    - utter_what_help
* give_help_type{"help_type": "search"}
    - slot{"help_type": "search"}
    - action_help
    - action_restart


## Some initial "base" stories defined by us to take care of the booking of restaurants

# User requests restaurant(Opt1: User requests restaurant without giving any parameters. Then gives the city)
* request_restaurant
     - action_search_restaurants
     - slot{"requested_slot": "city"}
* inform_city{"city":"Merano"}
     - action_search_restaurants
     - slot{"city": "Merano"}
     - slot{"requested_slot": "cuisine"}
* inform_cuisine{"cuisine": "chinese"}
     - action_search_restaurants
     - slot{"cuisine": "chinese"}
     - action_restart

# User requests restaurant(Opt2: User requests a restaurant with a specific cuisine type. Then gives the city)
* request_restaurant{"cuisine": "chinese"}
     - action_search_restaurants
     - slot{"cuisine": "chinese"}
     - slot{"requested_slot": "city"}
* inform_city{"city": "Bolzano"}
     - action_search_restaurants
     - slot{"city": "Bolzano"}
     - action_restart

# User requests restaurant(Opt3: User requests a restaurant in a certain city with a cuisine type)
* request_restaurant{"city": "Bolzano", "cuisine": "sushi"}
     - action_search_restaurants
     - slot{"city": "Bolzano"}
     - slot{"cuisine": "sushi"}
     - action_restart

# User requests restaurant(Opt4: User requests a restaurant in a certain city)
* request_restaurant{"city": "Bolzano"}
     - action_search_restaurants
     - slot{"city": "Bolzano"}
     - slot{"requested_slot": "cuisine"}
* inform_cuisine{"cuisine": "chinese"}
     - action_search_restaurants
     - slot{"cuisine": "chinese"}
     - action_restart

# User requests restaurant(Opt5: User requests a restaurant with all the parameters)
* request_restaurant{"city": "Bolzano", "cuisine": "sushi"}
     - action_search_restaurants
     - slot{"city": "Bolzano"}
     - slot{"cuisine": "sushi"}
     - action_restart

## Below we have stories generated from the RASA interactive learning, to make sure that we cover all cases based on the user input we have gotten by testing the bot. These are put below as they were created by testing and they are not just definitions like the one's above.

## Generated Story -3482635316772956271
* request_help
    - utter_what_help
* give_help_type{"help_type": "tellmemore"}
    - slot{"help_type": "tellmemore"}
    - action_help
* request_help
    - utter_what_help
* give_help_type{"help_type": "nevermind"}
    - slot{"help_type": "nevermind"}
    - action_help
* bye
    - utter_bye
    - action_restart

## Generated Story -5851471861522459799
* greet
    - utter_greet
    - utter_bot_presentation
* request_help
    - utter_what_help
* give_help_type{"help_type": "search"}
    - slot{"help_type": "search"}
    - action_help
* request_restaurant{"cuisine": "pizza", "city": "bolzano"}
    - action_search_restaurants
    - slot{"city": "bolzano"}
    - slot{"cuisine": "pizza"}
* thanks
    - utter_thanks
    - action_restart

## Generated Story 3556008137407677735
* request_restaurant{"cuisine": "pizza", "city": "merano"}
    - slot{"city": "merano"}
    - slot{"cuisine": "pizza"}
    - action_search_restaurants
* compliment
    - utter_respond_compliment
    - action_restart

## Generated Story 8671088023844346105
* greet
    - utter_greet
    - utter_bot_presentation
* request_restaurant{"cuisine": "pizza"}
    - slot{"cuisine": "pizza"}
    - action_search_restaurants
    - slot{"cuisine": "pizza"}
    - slot{"requested_slot": "city"}
* inform_city{"city": "bolzano"}
    - slot{"city": "bolzano"}
    - action_search_restaurants
    - slot{"city": "bolzano"}
    - action_restart

## Generated Story -322176397615619642
* thanks
    - utter_thanks
* bye
    - utter_bye
    - action_restart

## Generated Story -2733989667833620754
* greet
    - utter_greet
    - utter_bot_presentation
* request_help
    - utter_what_help
* give_help_type{"help_type": "search"}
    - action_help
    - slot{"help_type": "search"}
* inform_city{"city": "egna"}
    - action_search_restaurants
    - slot{"city": "egna"}
    - slot{"requested_slot": "cuisine"}
* inform_cuisine{"cuisine": "thai"}
    - action_search_restaurants
    - slot{"cuisine": "thai"}
    - action_restart

## Generated Story -2733985667833620754
* greet
    - utter_greet
    - utter_bot_presentation
* request_help
    - utter_what_help
* give_help_type{"help_type": "tellmemore"}
    - action_help
    - slot{"help_type": "tellmemore"}
* request_restaurant
    - action_search_restaurants
    - slot{"requested_slot": "city"}
* inform_city{"city": "Bolzano"}
    - action_search_restaurants
    - slot{"city": "Bolzano"}
    - slot{"requested_slot": "cuisine"}
* inform_cuisine{"cuisine": "Pasta"}
    - action_search_restaurants
    - slot{"cuisine": "Pasta"}
    - action_restart

## Generated Story -7533989612333620754
* request_restaurant{"cuisine": "spatzle", "city": "egna"}
    - action_search_restaurants
    - slot{"city": "egna"}
    - slot{"cuisine": "spatzle"}
    - action_restart

## Generated Story 1255782357612896178
* greet
    - utter_greet
    - utter_bot_presentation
* greet
    - utter_greet

