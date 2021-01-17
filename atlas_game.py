from __future__ import print_function
from api import get_countries_list
from ssml import *
import random
from alexa_ssml import *
from more_info import *

#Basic list for testing
country_list = []
move_history = []
user_letter_to_play = ""
counter = 0
last_neg = 0
last_pos = 0

negative_responses = bad_responses
pos_responses = good_responses

# --------------- Helpers that build all of the responses ----------------------

#--------------- Helper Functions for the game ------------------------#



# --------------- Functions that control the skill's behavior ------------------

def get_country_response(event):
    global move_history, country_list, user_letter_to_play, pos_responses, negative_responses, previous_reply_index
    session_attributes = {}
    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False
    card_title = "Country"
    
    #gets the user's response 
    #TO DO: check if the country is valid
    temp = event['request']['intent']['slots']['country']['value']
    country = "" + temp
    global counter, Number_of_invalid_country, Number_of_invalid_letter, last_pos, last_neg
    
    if not is_valid_country(country):
        index = random.randint(0, Number_of_invalid_country)
        while index==last_neg:
            index  = random.randint(0, Number_of_invalid_country)
        last_neg = index
        speech_output = negative_responses[index] + ". " + alexa_disappointed(country + ' is not a country. ')

        # should_end_session = True
        counter = 0
        return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    else:
        if not is_letter_valid(country):
            index = random.randint(Number_of_invalid_country, Number_of_invalid_country+Number_of_invalid_letter)
            while index== last_neg:
                index  = random.randint(Number_of_invalid_country, Number_of_invalid_country+Number_of_invalid_letter)
            last_neg = index

            speech_output = (negative_responses[index] + ". " + alexa_disappointed("The country should start with " + user_letter_to_play) + " Please try again. ") 
            
            return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        else:
            if move_played(country):
                speech_output = alexa_disappointed("That country has already been said. Try another" )
                return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
            
        
    index = random.randint(0, len(pos_responses)-1)
    while index==last_pos:
        index = random.randint(0, len(pos_responses)-1)
    last_pos = index
    alexa_country, should_end_session = alexa_response(country[len(country)-1])
    speech_output =  (pos_responses[index] + ". My next country is " + str(alexa_country) + 
    " Your next country should start with " + alexa_country[-1])
    move_history.append(country.upper())
    move_history.append(alexa_country.upper())
    user_letter_to_play = alexa_country[-1]
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def move_played(country):
    global move_history
    if country.upper() in move_history:
        return True
    else:
        return False
    
def alexa_response(letter):
    global country_list
    list_start_w_let = [country for country in country_list
                        if country.startswith(letter.upper())]
    index = 0
    while(index >= 0 and index < len(list_start_w_let)):
        if move_played(list_start_w_let[index]):
            index += 1
        else:
            return (list_start_w_let[index], False )
    
    else:
        return ("<break time=\"1s\"/>" + "I can't think of a Country with this letter. I lost..", True)
    return (response, True)

def is_letter_valid(country):
    global user_letter_to_play
    if country[0].upper() == user_letter_to_play.upper():
        return True
    else:
        return False


    
def is_valid_country(country_name):
    global country_list
    if country_name.upper() in country_list:
        return True
    else: 
        return False
    

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    global country_list, user_letter_to_play, move_history
    if not country_list:
        temp = get_countries_list()
        country_list.extend(temp)
    session_attributes = {}
    card_title = "Welcome"
    first_turn = random.randint(0,len(country_list)-1)
    last_letter = country_list[first_turn][-1]
    user_letter_to_play = last_letter
    move_history.append(country_list[first_turn])

    # first_turn = "Yemen"
    # move_history.append(first_turn.upper())
    # last_letter = first_turn[-1]
    # user_letter_to_play = last_letter
    speech_output = ("Welcome to the Atlas Game, a fun activity to do while also enhancing your geographical knowledge! How we play is I give you a country" +
    "and you reply with another country starting with the last letter of the one I give. " +
    "For example, I say Kenya. You could say Argentina because it starts with an A." + "<break time=\"1s\"/>" + "Got it?" 
    + "<break time=\"2s\"/>" + " I'll start with " + country_list[first_turn]  + "<break time=\"1s\"/>" +
    " Your country should start with " + last_letter)
    reprompt_text = "I don't know if you heard me, welcome to the atlas game"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def get_more_info(event):
    global user_letter_to_play
    reprompt_text = ""
    session_attributes = {}
    card_title = "Information"
    global country_list
    
    t = event['request']['intent']['slots']['info']['value']
    country = "" + t
    info = country_info(country)
    speech_output = ""
    if not info:
        speech_output = ("Sorry I could not find any information about" + country )
    else:
        speech_output = (country + " is in " + str(info[1]) +" . It has a population of " + str(info[2]) + " . The capital is " + str(info[0]) 
        + "<break time=\"1s\"/>" + " . It is still your turn to play a country that starts with " + user_letter_to_play )
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for playing. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific 
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass

    

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session,event):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name'] 

    # Dispatch to your skill's intent handlers
    if intent_name == "ReplyACountry":
        return get_country_response(event)
    elif intent_name == "MoreInfo":
        return get_more_info(event)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'],event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
        

if __name__ == "__main__":
    # execute only if run as a script
    lambda_handler(None,None)
