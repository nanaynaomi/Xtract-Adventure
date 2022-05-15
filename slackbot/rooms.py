from mod_adventurelib import *

# You ____.\n
room_entry = {
    'soa':"go to the general shared office area",
    'lb':"go to the large cubicle that is shared by Luke and Byers",
    'dr':"go to the demo room",
    'cr':"go to the conference room",
    'zm':"go to Zoë and Madden's office",
    'ws':"go to the workshop",
    'open_fridge': "walk over to the fridge and open it",
    'close_fridge': "close the fridge",

    'car': "go to your car",
    'xhq': "drive to Xtract HQ and go inside",
    'bc': "drive to Dr. Baker's clinic and go inside",
    'pdx':"fly back to PDX airport", # default is fly back to, but if they're in car they'll drive
    'wy': "fly to the Weyland-Yutani clinic and go in",
    'ts': "fly to the Trade Show and go in",

    'open_laptop':"open the laptop",
    'close_laptop':"close the laptop",
    'open_slack':"open Slack",
    'close_slack':"close Slack",
    'open_github':"open GitHub",
    'close_github':"close Github",

    'wyl':"go to the lobby of the Weyland-Yutani clinic",
    'wyb':"go to the back office area",
    'wys':"go to the server room",
    'wyi':"go to the injection area",

    'bcl':"go to the lobby of Dr. Baker's clinic",
    'bci':"go to the injection area",
    'bcm':"go to the mixing area",
    'bcf':"go to the front desk",

    'mch':"go to the main area of the convention hall",
    'xb':"go to the Xtract Solutions booth",
    'rb':"go to the Rosch booth",
    'cb':"go to the cerner booth",
}

# Rooms: ---------------------------------------------------------

# Xtract HQ Rooms: ------
Room.after_event = None

shared_office_area = Room("""
This room, the main shared office area of Xtract HQ, contains several desks and is connected to a few other rooms as well as a front door which leads out to the parking lot.
There is a Furby on a bookshelf in the corner... its eyes seem to follow you as you move about the room.
There is a small kitchen area with a mini-fridge.
Wei is at her desk, testing software. Graham is on the phone with a customer. You see Martin and Andrew standing around talking - they dont seem to be doing much of anything but their physical presence in the office makes you uncomfortable. 
""")

conference_room = Room("""
There is a TV on the wall.
There is a whiteboard on the wall with some random gibberish on it that looks like it's been there for a long time.
You look at the table. There are miscellaneous vials and mechanical contraptions sitting here.
A mug is here.
""")

demo_room = Room("""
When you come into this room, you hear the computer making a noise,
its the notification for a virtual demo that is about to start. You could *join the call*...
""")
demo_room.after_event = """
This room is quiet and empty right now. Nothing much to do in here...
"""

fridge = Room("""
You examine the contents of the mini-fridge.
""")

luke_byers_cubicle_area = Room("""
You see both Luke and Byers working. Byers is sitting at his computer. Luke is pacing back and forth and talking into his bluetooth headset. 
You look at Luke's computer, but there are too many chrome tabs open to see anything of use.
""")

zoe_madden_office = Room("""
This room is exceptionally well organized in comparison to the rest of the office.
There is a 'customer tracking' whiteboard on the wall which is so full that there isn't the tiniest bit of space for another customer...
Zoë is at her desk, but Madden isn't here.
""")
zoe_madden_office.after_event = """
You notice that your customer, Weyland-Yutani, has been added to the 'customer tracking' whiteboard. The board was already so full that your customer's info had to be written on the wall next to it.
Zoë is at her desk, but Madden isn't here.
"""


# PDX airport and car ------

car = Room("""
You find yourself driving on 217... Where will you go?
XHQ - Xtract HQ
BC - Dr. Baker's Clinic
PDX - Portland International Airport
""")

pdx_airport = Room("""
You are at the Portland International Airport (PDX). Where will you go?
Car - Leave airport and go to your car
TS - Trade Show
""")
pdx_airport.after_event = """
You are at the Portland International Airport (PDX). Where will you go?
Car - Leave airport and go to your car
TS - Trade Show
WY - Weyland-Yutani Clinic
"""

# Laptop "Rooms" ------

laptop = Room("""
You are on the desktop. There are two shortcuts. What will you open?
GitHub
Slack
""")

slack = Room("""
""")

github = Room("""
You are in an Xtract Solutions GitHub Repository, on the "Issues" page. If someone suggested a feature to you, perhaps you should *create a new issue* about it. 
Maybe this new feature could even help you make a sale!
""")


# New Customer Rooms ------
wy_lobby = Room("""
Many patients are impatiently waiting.
There is a Microsoft Surface Login Kiosk.
""")
wy_lobby.after_event = """
Everyone in the lobby seems to be in a good mood, and there are only a couple of patients waiting.
There is a Microsoft Surface Login Kiosk.
"""

wy_back_office_area = Room("""
Back office area. 
Madden is meeting with the customer's project manager and several doctors.
The doctors are complaining that the software doesn't do what they need and the project shouldn't be taking place. Madden looks stressed out.
The nurses are frantically running around complaining that they cant treat patients because the system doesn't work.
""")
wy_back_office_area.after_event = """
Everyone is so happy because Summit is working and everything is amazing. The doctors have lifted madden in the air and she is crowd surfing on a sea of hands like a rock star.
"""

wy_server_room = Room("""
An IT guy is here, watching you. He follows you wherever you move and stays close to you at all times.
There is a terminal here.
""")
wy_server_room.after_event = """
The IT guy is still lurking around, but the server is all good now!
"""

wy_injection_area = Room("""
Stephanie is training several injection nurses on how to use Summit but nothing is working.
""")
wy_injection_area.after_event = """
The nurses in here are talking about how amazing Summit is and how they are treating patients in record time.
"""

# Baker Clinic Rooms ------
bc_lobby = Room("""
You are standing in a large open lobby filled with chairs. A few patients are waiting.
There is a Microsoft surface sitting on the front desk.
""")

bc_injection_area = Room("""
There is a computer being used by a nurse who is giving a patient their allergy injections.
""")

bc_mixing_area = Room("""
There is a refrigerator.
There is a desk with a nurse sitting at it who is mixing vials.
There is an Automated Mixing Assistant in the corner.
""")

bc_front_desk = Room("""
This is the front desk office area. Nothing much to do in here...
""")


# Trade Show ------
ts_main_area = Room("""
You enter a large convention hall with rows and rows of booths. Among them you notice booths representing Xtract Solutions (XB), Cerner (CB), and Rosch (RB).
""")

xtract_booth = Room("""
This booth is very active!  
To the left you see James entertaining a group of prospective clients.
To the right you see madden and scott talking.
Ahead you see a large poster with a circular graphic with the words "Test > Prescribe > Mix > Outsource > Inject > Comply" and table with Xtract Solutions branded conference goodies. You spot a *potential client* standing by it that you could talk to...
""")

rosch_booth = Room("""
There is no one here, just an empty booth with an antiquated computer covered in a thick layer of dust...
""")

cerner_booth = Room("""
This booth is unlike all the others... the floors are marble and there are giant crystal chandeliers hanging from the ceilings. People in black tuxedos and stunning ballgowns are mingling.
There is a huge banquet table with free champagne and shrimp cocktails.
""")


# Room attributes: ----------------------------------------------------------
Room.is_laptop_room = False
laptop.is_laptop_room = True
github.is_laptop_room = True
slack.is_laptop_room = True

# Rooms that change on event 6:
Room.change_on_6 = False
wy_lobby.change_on_6 = True
wy_back_office_area.change_on_6 = True
wy_server_room.change_on_6 = True
wy_injection_area.change_on_6 = True

slack.messages = [
        "Martin posted pictures of his cats in #catfeed and people are going crazy",
        "A seemingly random string of memes has been posted in #random",
        "People are discussing something called Flamin' Hot Oat Bran in #snack-chat",
        "Luke has written some kind congratulatory messages in #general",
        "In #general, you see that Madden is threatening to quit again"
    ]

slack.notifications = [
    "",
    "",
    "Message from Zoë: \"If you hear any good ideas for Summit changes, be sure to create a git issue!\"",
    "Message from Zoë: \"If you hear any good ideas for Summit changes, be sure to create a git issue!\"",
    "Notification: Your issue has been completed and there is a new release of Summit. The customers will love this. This would have taken months before Addama...",
    "Everyone is panicking in the support channel because Summit isn't working at the Weyland-Yutani clinic. You should probably do something about it...",
    "You have been invited back to the office for a party.",
    "Not too many important messages for you on Slack right now."
]


# Room connections: ---------------------------------------------------------

shared_office_area.connections = [conference_room, demo_room, fridge, luke_byers_cubicle_area, zoe_madden_office, car, laptop]
conference_room.connections = [shared_office_area, laptop]
demo_room.connections = [shared_office_area, laptop]
fridge.connections = [shared_office_area, laptop]
luke_byers_cubicle_area.connections = [shared_office_area, laptop]
zoe_madden_office.connections = [shared_office_area, laptop]

car.connections = [shared_office_area, bc_lobby, pdx_airport]

pdx_airport.connections = [car, ts_main_area, laptop, wy_lobby]

laptop.connections = [slack, github] # laptop can also access or be accessed from whatever room you are currently in
slack.connections = [laptop, github]
github.connections = [laptop, slack]

wy_lobby.connections = [pdx_airport, wy_back_office_area, laptop]
wy_back_office_area.connections = [wy_lobby, wy_server_room, wy_injection_area, laptop]
wy_server_room.connections = [wy_back_office_area, laptop]
wy_injection_area.connections = [wy_back_office_area, laptop]

bc_lobby.connections = [car, bc_injection_area, laptop]
bc_injection_area.connections = [bc_lobby, bc_mixing_area, laptop]
bc_mixing_area.connections = [bc_injection_area, bc_front_desk, laptop]
bc_front_desk.connections = [bc_mixing_area, laptop]

ts_main_area.connections = [pdx_airport, xtract_booth, rosch_booth, cerner_booth, laptop]
xtract_booth.connections = [ts_main_area, laptop]
rosch_booth.connections = [ts_main_area, laptop]
cerner_booth.connections = [ts_main_area, laptop]


room_guide = {
    shared_office_area : "SOA - Shared office area",
    conference_room : "CR - Conference room",
    demo_room : "DR - Demo room",
    fridge : "Open fridge",
    luke_byers_cubicle_area : "LB - Luke and Byers cubicle area",
    zoe_madden_office : "ZM - Zoë and Madden's office",

    car : "Car - Leave current building and go to your car",
    pdx_airport : "PDX - Portland International Airport",

    laptop : "Open laptop", # laptop can also access or be accessed from whatever room you are currently in...
    slack : "Open Slack",
    github : "Open GitHub",

    wy_lobby : "WYL - Lobby",
    wy_back_office_area : "WYB - Back office area",
    wy_server_room : "WYS - Server room",
    wy_injection_area : "WYI - Injection area",

    bc_lobby : "BCL - Lobby",
    bc_injection_area : "BCI - Injection area",
    bc_mixing_area : "BCM - Mixing area",
    bc_front_desk : "BCF - Front desk office area",

    ts_main_area : "MCH - Main convention hall",
    xtract_booth : "XB - Xtract booth",
    rosch_booth : "RB - Rosch booth",
    cerner_booth : "CB - Cerner booth"
}

# Drive/Fly to
car_pdx_room_guide = {

    # 'drive to'
    shared_office_area : "XHQ - Xtract HQ",
    bc_lobby : "BC - Dr. Baker's Clinic",

    # 'drive to' if current_room is car,  'fly back to' if current_room is (wy_lobby or ts_main_area)
    pdx_airport : "PDX - Portland International Airport",
    car : "Car - Leave airport and go to your car",
    laptop: "Open laptop",

    # 'fly to' if current_room is pdx_airport
    wy_lobby : "WY - Weyland-Yutani Clinic",
    ts_main_area : "TS - Trade Show"
}

# Maps: ---------------------------------------------------------

xhq_map = {
    "type": "image", 
    "title": {"type": "plain_text","text": "Map of Xtract HQ"},
    "block_id": "xhq_map",
    "image_url": "https://xtract-adventure-maps-xas.s3.us-west-2.amazonaws.com/xhq_map.jpg",
    "alt_text": "Map of Xtract HQ"
}
bc_map = {
    "type": "image", 
    "title": {"type": "plain_text","text": "Map of Dr. Baker Clinic"},
    "block_id": "bc_map",
    "image_url": "https://xtract-adventure-maps-xas.s3.us-west-2.amazonaws.com/bc_map.jpg",
    "alt_text": "Map of Dr. Baker Clinic"
}
carpdx1_map = {
    "type": "image", 
    "title": {"type": "plain_text","text": "Map of places to travel"},
    "block_id": "carpdx1_map",
    "image_url": "https://xtract-adventure-maps-xas.s3.us-west-2.amazonaws.com/carpdx1_map.jpg",
    "alt_text": "Map of places to travel"
}
carpdx2_map = {
    "type": "image", 
    "title": {"type": "plain_text","text": "Map of places to travel"},
    "block_id": "carpdx2_map",
    "image_url": "https://xtract-adventure-maps-xas.s3.us-west-2.amazonaws.com/carpdx2_map.jpg",
    "alt_text": "Map of places to travel"
}
ts_map = {
    "type": "image", 
    "title": {"type": "plain_text","text": "Map of Trade Show"},
    "block_id": "ts_map",
    "image_url": "https://xtract-adventure-maps-xas.s3.us-west-2.amazonaws.com/ts_map.jpg",
    "alt_text": "Map of Trade Show"
}
wy_map = {
    "type": "image", 
    "title": {"type": "plain_text","text": "Map of Weyland-Yutani Clinic"},
    "block_id": "wy_map",
    "image_url": "https://xtract-adventure-maps-xas.s3.us-west-2.amazonaws.com/wy_map.jpg",
    "alt_text": "Map of Weyland-Yutani Clinic"
}
laptop_map = {
    "type": "section",
    "text": {"type": "mrkdwn", "text": "To view the map, please close the laptop first."}
}


shared_office_area.location_map = xhq_map
conference_room.location_map = xhq_map
demo_room.location_map = xhq_map
fridge.location_map = xhq_map
luke_byers_cubicle_area.location_map = xhq_map
zoe_madden_office.location_map = xhq_map

car.location_map = {1:carpdx1_map, 2:carpdx2_map}
pdx_airport.location_map = {1:carpdx1_map, 2:carpdx2_map}

laptop.location_map = laptop_map
slack.location_map = laptop_map
github.location_map = laptop_map

wy_lobby.location_map = wy_map
wy_back_office_area.location_map = wy_map
wy_server_room.location_map = wy_map
wy_injection_area.location_map = wy_map

bc_lobby.location_map = bc_map
bc_injection_area.location_map = bc_map
bc_mixing_area.location_map = bc_map
bc_front_desk.location_map = bc_map

ts_main_area.location_map = ts_map
xtract_booth.location_map = ts_map
rosch_booth.location_map = ts_map
cerner_booth.location_map = ts_map
