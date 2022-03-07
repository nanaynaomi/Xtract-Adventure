import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.flask import SlackRequestHandler
from mod_adventurelib import *
from game import *

# logging.basicConfig(level=logging.DEBUG)
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# @app.middleware # or app.use(log_request)
# def log_request(logger, body, next):
#     logger.debug(body)
#     return next()

@app.event("message")
def handle_message(message, say):
    if get_context() == 'game_over':
        say("GAME OVER")
    elif (message['text'].lower() == "start adventure" and get_context() == 'beginning') or get_context() != 'beginning':
        res = handle_command(message['text'].lower())
        if res is not None:
            say(res)

from flask import Flask, request

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)
     
if __name__ == "__main__":

    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

    # Run our app on our externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run(host='0.0.0.0', port=3000)
