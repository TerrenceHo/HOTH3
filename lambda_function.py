from __future__ import print_function
import requests
from bs4 import BeautifulSoup
######## Recipe Parsing Functions ########

base_url = "http://forkthecookbook.com"
search_base_url = "http://forkthecookbook.com/search-recipes"

def get_recipe_URLs(search_term):
    links_list = []
    r = requests.get(search_base_url + "?q=" + search_term)
    soup = BeautifulSoup(r.text, "html.parser")
    soup = soup.find_all("a", {"class":"gallery-link"}, href=True)
    for i in range(len(soup)):
        links_list.append(base_url + soup[i]['href'])
    return links_list
    
def get_single_recipe_name(specific_url):
    name = ""
    r = requests.get(specific_url)
    soup = BeautifulSoup(r.text, "html.parser")
    name = soup.find("title").get_text()

    name=name.split("|")[0]
    return name
    
def get_data(specific_url):
    ingredients_list = []
    instructions_list = []
    r = requests.get(specific_url)
    soup = BeautifulSoup(r.text, "html.parser")

    ingredients_list = soup.find_all("td", class_="recipe-ingredients")
    for i in range(len(ingredients_list)):
        ingredients_list[i] = " ".join(ingredients_list[i].get_text().strip().split())
    
    instructions_list = soup.find("td", class_="recipe-instructions").find_all("li")
    for i in range(len(instructions_list)):
        instructions_list[i] = " ".join(instructions_list[i].get_text().strip().split())    #size of 1

    return ingredients_list, instructions_list


# Other functions

######## Response Builders ########
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
    
######## Intent Handlers (Behavior/Logic) ########
def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Easy Cook.  We read recipes to you."
    reprompt_text = "Please say that again"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def set_recipes_in_session(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    
    if 'value' in intent['slots']['item']:
        search_term = intent['slots']['item']['value']
        links_list = get_recipe_URLs(search_term)
        recipe_name = get_single_recipe_name(links_list[0])
        session_attributes = {
            "recipe_links":links_list,
            "recipe_index":0
        }
        speech_output = "I found a recipe called " + recipe_name + ". " \
                        "Would you like to use this recipe or another one?"
        reprompt_text = "I found a recipe called " + recipe_name + ". " \
                        "Would you like to use this recipe or another one?"
    else:
        print(intent['slots']['item'])
        speech_output = "I'm not sure what recipe you are searching for." \
                        "You can tell me to search for a recipe by saying, " \
                        "Find a recipe for chicken."
        reprompt_text = "I'm not sure what recipe you are searching for." \
                        "You can tell me to search for a recipe by saying, " \
                        "Find a recipe for chicken."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def next_recipe_in_session(intent, session):
    card_title = intent['name']
    should_end_session = False
    session_attributes = {}
    
    if session.get('attributes', {}) and "recipe_links" in session.get('attributes', {}):
        recipe_index = session['attributes']['recipe_index']
        recipe_links = session['attributes']['recipe_links']
        recipe_link = session['attributes']['recipe_links'][recipe_index+1]
        recipe_name = get_single_recipe_name(recipe_link)
        session_attributes = {
            "recipe_links":recipe_links,
            "recipe_index":recipe_index+1
        }
        speech_output = "I found a recipe called " + recipe_name + "." \
                        "Would you like to use this recipe or another one?"
        reprompt_text = "I found a recipe called " + recipe_name + "." \
                        "Would you like to use this recipe or another one?"
    else:
        speech_output = "I'm not sure what recipe you are searching for." \
                        "You can tell me to search for a recipe by saying, " \
                        "Find a recipe for chicken."
        reprompt_text = "I'm not sure what recipe you are searching for." \
                        "You can tell me to search for a recipe by saying, " \
                        "Find a recipe for chicken."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    
def set_instructions_in_session(intent, session):
    should_end_session = False
    session_attributes = {}

    if session.get('attributes', {}) and "recipe_links" in session.get('attributes', {}):
        recipe_index = session['attributes']['recipe_index']
        recipe_link = session['attributes']['recipe_links'][recipe_index]
        ingredients, instructions = get_data(recipe_link)
        session_attributes = {
            "instructions": instructions,
            "instructions_index":0
        }
        speech_output = "You have chosen a recipe. Here are the ingredients: "
        for ingredient in ingredients:
            speech_output += ingredient + ". "
        speech_output += "Say next or previous to continue"
        reprompt_text = "say next or previous to continue"
    else:
        speech_output = "You did not set a recipe. Say find a recipe to set a recipe" 
        reprompt_text = "You did not set a recipe. Say find a recipe to set a recipe"
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
    
def next_instruction(intent, session):
    should_end_session = False
    session_attributes = {}
        
    if session.get('attributes', {}) and "instructions" in session.get('attributes', {}):
        instructions_index = session['attributes']['instructions_index']
        instructions = session['attributes']['instructions']
        instruction = instructions[instructions_index]
        session_attributes = {
            "instructions":instructions,
            "instructions_index":instructions_index+1
        }
        speech_output = "Now, " + instruction + ". "
        speech_output += "Say Next step to move onto the next instruction"
        reprompt_text = "Say Next step to move onto the next instruction"
    else:
        speech_output = "You did not set a recipe. Say find a recipe to set a recipe" 
        reprompt_text = "You did not set a recipe. Say find a recipe to set a recipe"
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def repeat_instruction(intent, session):
    should_end_session = False
    session_attributes = {}
        
    if session.get('attributes', {}) and "instructions" in session.get('attributes', {}):
        instructions_index = session['attributes']['instructions_index']
        instructions = session['attributes']['instructions']
        instruction = instructions[instructions_index-1]
        session_attributes = {
            "instructions":instructions,
            "instructions_index":instructions_index
        }
        speech_output = "Now, " + instruction + ". "
        speech_output += "Say Next step to move onto the next instruction"
        reprompt_text = "Say Next step to move onto the next instruction"
    else:
        speech_output = "You did not set a recipe. Say find a recipe to set a recipe" 
        reprompt_text = "You did not set a recipe. Say find a recipe to set a recipe"
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def previous_instruction(intent, session):
    should_end_session = False
    session_attributes = {}
        
    if session.get('attributes', {}) and "instructions" in session.get('attributes', {}):
        instructions_index = session['attributes']['instructions_index']
        instructions = session['attributes']['instructions']
        instruction = instructions[instructions_index-2]
        session_attributes = {
            "instructions":instructions,
            "instructions_index":instructions_index-1
        }
        speech_output = "Now, " + instruction + ". "
        speech_output += "Say Next step to move onto the next instruction"
        reprompt_text = "Say Next step to move onto the next instruction"
    else:
        speech_output = "You did not set a recipe. Say find a recipe to set a recipe" 
        reprompt_text = "You did not set a recipe. Say find a recipe to set a recipe"
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
        
        
def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using our app. Have a nice day!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
    
######## Session Handlers ########
def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()

def on_intent(intent_request, session):
    """ Called when user specifies an intent for this skill """
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
         
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    if intent_name == "FindRecipeIntent":
        return set_recipes_in_session(intent, session)
    elif intent_name == "UseRecipeIntent":
        return set_instructions_in_session(intent, session)
    elif intent_name == "UseDifferentRecipeIntent":
        return next_recipe_in_session(intent, session)
    elif intent_name == "NextIntent":
        return next_instruction(intent, session)
    elif intent_name == "RepeatIntent":
        return same_instruction(intent, session)
    elif intent_name == "PreviousIntent":
        return previous_instruction(intent, session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    
    
    

######## Main Handler ########
def lambda_handler(event, context):
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
          
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
    
