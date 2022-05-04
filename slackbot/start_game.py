from mod_adventurelib import *
from commands import look
from rooms import *
from items import *

def start_adventure(user_id):

    # Initialize new player:
    p = Player(user_id, shared_office_area, byers_items=Bag({chair, laptop_item, standing_desk}))
    p.initialize_room_items([shared_office_area, conference_room, demo_room, fridge, luke_byers_cubicle_area, zoe_madden_office, car, pdx_airport,
        wy_lobby, wy_back_office_area, wy_server_room, wy_injection_area, bc_lobby, bc_injection_area, bc_mixing_area, bc_front_desk,
        ts_main_area, xtract_booth, rosch_booth, cerner_booth])
    p.add_room_item(fridge, ranch)
    p.add_room_item(fridge, burrito)
    p.add_room_item(bc_mixing_area, vials)
    p.sale_rooms = {
        demo_room: "in the demo room at Xtract HQ",
        xtract_booth: "at Xtract's booth at the tradeshow"
    }
    current_players[user_id] = p  # Add player object to current_players dictionary

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
    msg += '\n\n' + look(p)
    return msg
