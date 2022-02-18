# import os
# import logging
# from flask import Flask
# from slack import WebClient
# from slackeventsapi import SlackEventAdapter
# from coinbot import CoinBot

# # Initialize a Flask app to host the events adapter
# app = Flask(__name__)
# # Create an events adapter and register it to an endpoint in the slack app for event injestion.
# slack_events_adapter = SlackEventAdapter(os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)

# # Initialize a Web API client
# slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))

# # Get the bot ID
# BOT_ID = slack_web_client.api_call("auth.test")['user_id']

# def flip_coin(channel):
#     """Craft the CoinBot, flip the coin and send the message to the channel
#     """
#     # Create a new CoinBot
#     coin_bot = CoinBot(channel)

#     # Get the onboarding message payload
#     message = coin_bot.get_message_payload()

#     # Post the onboarding message in Slack
#     slack_web_client.chat_postMessage(**message)


# # When a 'message' event is detected by the events adapter, forward that payload
# # to this function.
# @slack_events_adapter.on("message")
# def message(payload):
#     """Parse the message event, and if the activation string is in the text, 
#     simulate a coin flip and send the result.
#     """
#     event = payload.get("event", {}) # Get the event data from the payload
#     user_id = event.get('user')      # Get the user that the message came from
#     text = event.get("text")         # Get the text from the event that came through

#     # Make sure that user_id is not None and message is not from a bot
#     if user_id != None and BOT_ID != user_id: 
#         # Check and see if the activation phrase == the text of the message. 
#         # If so, execute the code to flip a coin.
#         if text.lower() == "start adventure":    
#             # Since the activation phrase was met, get the channel ID that the event
#             # was executed on
#             channel_id = event.get('channel')

#             # Execute the flip_coin function and send the results of
#             # flipping a coin to the channel
#             return flip_coin(channel_id)

# if __name__ == "__main__":
#     # Create the logging object
#     logger = logging.getLogger()

#     # Set the log level to DEBUG. This will increase verbosity of logging messages
#     logger.setLevel(logging.DEBUG)

#     # Add the StreamHandler as a logging handler
#     logger.addHandler(logging.StreamHandler())

#     # Run our app on our externally facing IP address on port 3000 instead of
#     # running it on localhost, which is traditional for development.
#     app.run(host='0.0.0.0', port=3000)
