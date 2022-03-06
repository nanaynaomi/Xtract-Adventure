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
    'ts': "fly to the tradeshow and go in",

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
its the notification for a virtual demo that is about to start. You could join the call...
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

# Fun idea: If they type 'steal a car' or 'hotwire a car' or 'steal Luke's car', it will let them, and then put them in the car Room.
car = Room("""
You find yourself driving on 217... Where will you go?
XHQ - Xtract HQ
BC - Dr. Baker's Clinic
PDX - Portland International Airport
""")

pdx_airport = Room("""
[description of pdx airport here...] Do you wanna get on plane? Where you wanna go?
""")


# Laptop Rooms ------

laptop = Room("""
You are on the desktop. There are two shortcuts. What will you open?
GitHub
Slack
""")

slack = Room("""
You have 7 notifications. Users Madden, Martin, and Zoe are online.
""")

github = Room("""
You are in an Xtract Solutions GitHub Repository, on the "Issues" page. If someone suggested a feature to you, perhaps you should create a new issue about it. 
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
An IT guy is here, watching you.
""")

wy_injection_area = Room("""
Stephanie is training several injection nurses on how to use Summit but nothing is working.
""")
wy_injection_area.after_event = """
The nurses in here are talking about how amazing Summit is and how they are treating patients in record time.
"""

# Baker Clinic Rooms ------
bc_lobby = Room("""
You are standing in a large open lobby filled with chairs.
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
You enter a large convention hall with rows and rows of booths. Among them you notice booths representing Xtract Solutions, Cerner, and Rosch
""")
xtract_booth = Room("""
This booth is very active!  
To the left you see James entertaining a group of prospective clients.
To the right you see madden and scott talking.
Ahead you see a large poster with a circular graphic with the words "Test > Prescribe > Mix > Outsource > Inject > Comply" and table with Xtract Solutions branded conference goodies. There are several potential clients standing around it that you could talk to...
""")
# xb_scott_madden = Room("""
# """)
# xb__

rosch_booth = Room("""
There is no one here, just an empty booth with an antiquated computer covered in a thick layer of dust...
""")
cerner_booth = Room("""
This booth is unlike all the others... the floors are marble and there are giant crystal chandeliers hanging from the ceilings. Men in black tuxedos and women in stunning ballgowns are mingling.
There is a huge banquet table with free champagne and shrimp cocktails.
""")

# Room attributes: ----------------------------------------------------------
Room.is_laptop_room = False
laptop.is_laptop_room = True
github.is_laptop_room = True
slack.is_laptop_room = True

# Room.list_people = True
# luke_byers_cubicle_area.list_people = False
# xtract_booth.list_people = False

# rooms where a sale can be made.
Room.can_make_sale_here = False
demo_room.can_make_sale_here = True
xtract_booth.can_make_sale_here = True
sale_rooms = {
    demo_room: "in the demo room at Xtract HQ",
    xtract_booth: "at Xtract's booth at the tradeshow"
}

Room.change_on_6 = False
wy_lobby.change_on_6 = True
wy_back_office_area.change_on_6 = True
wy_server_room.change_on_6 = True
wy_injection_area.change_on_6 = True



# Connections: (I might as well add connections/directions just to be safe right? Worry about this LATER though...)
# starting_room.north = forest
# forest.north = forest_edge

# MAKE A NESTED DICTIONARY??

# Room connections: ---------------------------------------------------------
room_connections = {
    shared_office_area : [conference_room, demo_room, fridge, luke_byers_cubicle_area, zoe_madden_office, car, laptop],
    conference_room : [shared_office_area, laptop],
    demo_room : [shared_office_area, laptop],
    fridge : [shared_office_area, laptop],
    luke_byers_cubicle_area : [shared_office_area, laptop],
    zoe_madden_office : [shared_office_area, laptop],

    car : [shared_office_area, bc_lobby, pdx_airport],

    pdx_airport : [wy_lobby, ts_main_area, laptop], # wy_lobby should only be accessible after successful demo or tradeshow

    laptop : [slack, github], # laptop can also access or be accessed from whatever room you are currently in...
    slack : [laptop],
    github : [laptop],

    wy_lobby : [pdx_airport, wy_back_office_area, laptop],
    wy_back_office_area : [wy_lobby, wy_server_room, wy_injection_area, laptop],
    wy_server_room : [wy_back_office_area, laptop],
    wy_injection_area : [wy_back_office_area, laptop],

    bc_lobby : [car, bc_injection_area, laptop],
    bc_injection_area : [bc_lobby, bc_mixing_area, laptop],
    bc_mixing_area : [bc_injection_area, bc_front_desk, laptop],
    bc_front_desk : [bc_mixing_area, laptop],

    ts_main_area : [xtract_booth, rosch_booth, cerner_booth, laptop],
    xtract_booth : [ts_main_area, laptop],
    rosch_booth : [ts_main_area, laptop],
    cerner_booth : [ts_main_area, laptop]
}


room_guide = {
    shared_office_area : "SOA - Shared office area",
    conference_room : "CR - Conference room",
    demo_room : "DR - Demo room",
    fridge : "Open fridge",
    luke_byers_cubicle_area : "LB - Luke and Byers cubicle area",
    zoe_madden_office : "ZM - Zoë and Madden's office",

    car : "Car - Leave current building and go to your car",

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

    # 'fly to' if current_room is pdx_airport
    wy_lobby : "WY - Weyland-Yutani Clinic",
    ts_main_area : "TS - Tradeshow"
}


# Initialize current room: ----
current_room = shared_office_area
previous_room = current_room
