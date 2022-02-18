import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
# from coinbot import CoinBot
from mod_adventurelib import *
from demo_game_test import *

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
# Create an events adapter and register it to an endpoint in the slack app for event injestion.
slack_events_adapter = SlackEventAdapter(os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))

# Get the bot ID
BOT_ID = slack_web_client.api_call("auth.test")['user_id']

def say(msg, channel_id):
    """Print a message."""
    msg = str(msg)
    # message = {"type": "section", "text": {"type": "mrkdwn", "text": msg}}
    slack_web_client.chat_postMessage(channel=channel_id, text=msg)


# When a 'message' event is detected by the events adapter, forward that payload
# to this function.
@slack_events_adapter.on("message")
def message(payload):
    """Parse the message event...
    """
    event = payload.get("event", {}) # Get the event data from the payload
    user_id = event.get('user')      # Get the user that the message came from
    text = event.get("text")         # Get the text from the event that came through
    

    # Make sure that user_id is not None and message is not from a bot
    if user_id != None and BOT_ID != user_id: 

        channel_id = event.get('channel')
        say("", channel_id)
        #### Later on I want to set it up so that user can start, restart, and exit the game.
        if text.lower() == "start adventure": # or text.lower() == "restart adventure":
            return say(look(), channel_id)    
        elif text.lower() == "test":
            return say("Luke gets eaten by a dragon", channel_id)  
        else:
            res = handle_command(text)
            if res is not None:
                return say(res, channel_id) 
                
if __name__ == "__main__":
    # Create the logging object
    logger = logging.getLogger()

    # Set the log level to DEBUG. This will increase verbosity of logging messages
    logger.setLevel(logging.DEBUG)

    # Add the StreamHandler as a logging handler
    logger.addHandler(logging.StreamHandler())

    # Run our app on our externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run(host='0.0.0.0', port=3000)
