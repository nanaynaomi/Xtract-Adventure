import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.flask import SlackRequestHandler
from mod_adventurelib import *
from game import *

logging.basicConfig(level=logging.DEBUG)
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.middleware # or app.use(log_request)
def log_request(logger, body, next):
    logger.debug(body)
    return next()

@app.event("message")
def handle_message(message, say):
    user_id = message["user"]
    player = current_players.get(user_id)
    msg = message['text'].lower()
    if player:
        if msg == "start adventure":
            say("You already have a game running with this account. To clear your progress so you can start over, say: \"quit adventure\"")
        elif msg == "quit adventure":
            say("Are you sure? This will delete all of your game progress and you will not be able to get it back.\n"
                "Please say exactly: \"I understand and I want to quit the game\" to confirm.")
        elif msg == "i understand and i want to quit the game":
            current_players.pop(user_id)
            del player
            say("CONFIRMED. Deleting your progress. If you would like to start a new adventure after this, say: \"start adventure\"")
        elif player.get_context() == "game_over":
            current_players.pop(user_id)
            del player
            say("GAME OVER.\nTo restart and try again, say: \"start adventure\".")
        else:
            res = handle_command(msg, player)
            if res is not None:
                say(res)
    elif msg == "start adventure" and not player:
        res = start_adventure(user_id)
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
