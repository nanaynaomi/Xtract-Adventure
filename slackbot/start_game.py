from mod_adventurelib import *
from commands import look

@when('start adventure', context='beginning')
def start_adventure():
    set_context(None)
    msg = ("Welcome to XAS (Xtract Adventure System)!\n"
        "Helpful commands: (Note - commands are NOT case sensitive)\n"
        "   'where can I go' - where you can go and what to type\n"
        "   'help' -  general assistance and explanation of commands\n"
        "Let's begin!\n"
        "\n"
        "\n"
        "You enter Xtract HQ. Luke has everyone gathered for an all hands meeting in the main room. "
        "As soon as you walk in, Luke calls you up to the front, and you approach with caution. "
        "Luke: \"I'd like to introduce you to our newest employee! "
        "As you know we are at a critical point in Xtract's growth so I've hired them to do all the things! "
        "They will be responsible for immediately generating the revenue we need!\" "
        "After Luke announces this, he continues to talk about other things that probably would have been helpful had you been listening. "
        "Soon, the meeting ends and everyone disperses. Luke tells you to see Byers about any accounts or equipment you need. "
        )
    msg += '\n\n' + look()
    return msg
