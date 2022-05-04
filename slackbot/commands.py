from mod_adventurelib import *
from rooms import *
from characters import *
from items import *
import random

# NAVIGATION: ---------------------------------------------------------------------

@when('lb', e_key='lb', room=luke_byers_cubicle_area)
@when('dr', e_key='dr', room=demo_room)
@when('cr', e_key='cr', room=conference_room)
@when('zm', e_key='zm', room=zoe_madden_office)
@when('soa', e_key='soa', room=shared_office_area)
@when('ws', e_key='ws', room=None)
@when('open fridge', e_key='open_fridge', room=fridge)
@when('close fridge', e_key='close_fridge', room=shared_office_area)

@when('car', e_key='car', room=car)
@when('xhq', e_key='xhq', room=shared_office_area)
@when('bc', e_key='bc', room=bc_lobby)
@when('pdx', e_key='pdx', room=pdx_airport)
@when('wy', e_key='wy', room=wy_lobby) 
@when('ts', e_key='ts', room=ts_main_area)

@when('wyl', e_key='wyl', room=wy_lobby)
@when('wyb', e_key='wyb', room=wy_back_office_area)
@when('wys', e_key='wys', room=wy_server_room)
@when('wyi', e_key='wyi', room=wy_injection_area)

@when('bcl', e_key='bcl', room=bc_lobby)
@when('bci', e_key='bci', room=bc_injection_area)
@when('bcm', e_key='bcm', room=bc_mixing_area)
@when('bcf', e_key='bcf', room=bc_front_desk)

@when('mch', e_key='mch', room=ts_main_area)
@when('xb', e_key='xb', room=xtract_booth)
@when('rb', e_key='rb', room=rosch_booth)
@when('cb', e_key='cb', room=cerner_booth)
def go_to(p, room, e_key):
    if p.get_context() != None:
        p.set_context(None)
    if room in room_connections[p.current_room]: 
        if p.current_room == car and room == pdx_airport:
            msg = "You drive to PDX airport.\n"
        elif room == wy_lobby and p.get_event_level() < 5:
            return "You cannot access that place, silly goose!"
        else:
            msg = f"You {room_entry[e_key]}.\n"
        p.set_current_room(room)
        if room == shared_office_area and p.get_event_level() == 6:
            msg += the_end(p)
        else:
            msg += look(p)
    elif e_key == 'ws' and p.current_room == shared_office_area:
        msg = ("It\'s a dark, scary place. You are likely to be eaten by a grue.\n"
        "You turn back in fear and do not enter the room")
    elif e_key == 'open_fridge' and p.current_room == bc_mixing_area:
        return interact(p, 'open', 'fridge')
    elif e_key == 'bcf' and p.current_room == bc_lobby:
        msg = "You can't climb over the desk."
    else:
        msg = "You cannot access that from where you currently are."
    return msg


def the_end(p):
    p.set_event_level(7) 
    msg = ("\n*~ ~ YOU HAVE WON!!! CONGRATS!! ~ ~*\n\n"
        "Everyone gathers for a celebratory meeting about the successful sale and install."
        " There is cake and Big's Chicken.\nBefore anyone has a chance to take a bite..."
        " A giant winged beast emerges from the shop! Luke is eaten by a dragon...\n\n"
        "*~ ~ THE END ~ ~*")
    return msg


@when('open laptop', e_key='open_laptop', room=laptop)
@when('close laptop', e_key='close_laptop', room=None) 
@when('open slack', e_key='open_slack', room=slack)
@when('slack', e_key='open_slack', room=slack)
@when('close slack', e_key='close_slack', room=laptop)
@when('close github', e_key='close_github', room=laptop)
@when('open github', e_key='open_github', room=github)
@when('github', e_key='open_github', room=github)
def laptop_access(p, room, e_key):
    global previous_room
    if p.inventory.find('laptop'): 
        if p.current_room == laptop and e_key == 'close_laptop':
            msg = laptop_navigation(p, previous_room, e_key)
        elif room and room in room_connections[p.current_room]:
            if e_key == 'open_laptop':
                previous_room = p.current_room
            msg = laptop_navigation(p, room, e_key)
        else:
            msg = "You can't access that from where you currently are."
    else:
        msg = "You need a laptop to do that."
    return msg


def laptop_navigation(p, room, e_key):
    if p.inventory.find('laptop'):
        if p.get_context() != None:
            p.set_context(None)
        msg = f"You {room_entry[e_key]}.\n"
        p.set_current_room(room)  # **** p.set_current_room(room)
        msg += '\n'+look(p)
    return msg


@when('where can i go')
def where_can_i_go(p):
    ''' Tells a player where they can go based on their current location/Room'''
    if p.current_room == fridge:
        msg = "You must close fridge."
    else:
        ignore_laptop = False if p.inventory.find('laptop') else True
        msg = "Where you can go:"
        if p.current_room == car or p.current_room == pdx_airport:
            rm_guide = car_pdx_room_guide
        else:
            rm_guide = room_guide
        for room in room_connections[p.current_room]:
            if (ignore_laptop and room == laptop) or (room == wy_lobby and p.get_event_level() < 5):
                msg += ""
            else:
                msg += f"\n{rm_guide[room]}"
        if p.current_room == shared_office_area:
            msg += f"\nWS - Workshop"
        elif p.current_room == laptop:
            msg += f"\nClose laptop"
    return msg
   

# GITHUB AND SLACK STUFF: ----------------------------------------------------------------

@when('create a new issue')
@when('create new issue')
@when('create issue')
@when('log issue')
@when('new issue')
@when('create github issue')
@when('github issue')
def github_issue(p):
    if p.current_room == github:
        if p.get_event_level() >= 4:
            msg = "You already created a good issue. That's enough for today."
        else:
            p.set_context('creating_issue')
            msg = "You are now creating an issue. Please enter the title of your issue like so: 'issue YOUR TITLE'"
    else:
        msg = "You need to be on GitHub to do that."
    return msg


@when('issue TITLE', context='creating_issue')
def issue_title(p, title):
    key_words = ["cat videos", "cat video", "cats", "more information", "smaller space", "red lines", "transparent ink", "transparent red", "red"]
    if any(word in title for word in key_words):
        msg = "Issue created! - Success! \n ~ You have a new Slack notification. ~"
        p.set_event_level(4)
    else:
        msg = "Issue created! - Issue rejected by Andrew with comment: \"no\"."
    p.set_context(None)
    msg += '\n' + "You are in an Xtract Solutions GitHub Repository, on the \"Issues\" page."
    return msg

@when('check notifications')
@when('check slack notifications')
@when('notifications')
@when('notification')
@when('check slack')
def slack_notifications(p):
    if p.current_room == slack:
        level = p.get_event_level()
        if level == 2 or level == 3:
            msg = "Message from Zoë: \"If you hear any good ideas for Summit changes, be sure to create a git issue!\""
        elif level == 4:
            msg = ("Notification: Your issue has been completed and there is a new release of Summit."  
                " The customers will love this. This would have taken months before Addama...")
        elif level == 5:
            msg = "Everyone is panicking in the support channel because Summit isn't working at the Weyland-Yutani clinic."
        elif level == 6:
            msg = "Everyone is going back to the office for a party."
        else: # 7
            msg = "Not too many important messages for you on Slack right now."
    else:
        msg = "Open Slack (in the game) to view notifications"
    return msg

def get_slack_messages(p):
    random.seed()
    num = random.randint(0,len(slack.messages)-1)
    msg = slack.messages[num]
    if p.have_notifications:
        msg += "\n:exclamation: You have notifications"
        p.have_notifications = False
    return msg



# GENERAL: ----------------------------------------------------------------


@when('take ITEM')
def take(p, item):
    if p.current_room.is_laptop_room:
        msg = "You cannot pick up items while using laptop."
    elif item == 'mug' and p.current_room == conference_room:
        msg = "Hmm... instant oatmeal... Steve has been here. You leave the mug on the table."
    elif item in ['needle', 'injection needle', 'syringe'] and p.current_room == wy_injection_area:
        msg = "You try to take the injection needle but the nurse karate chops it out of your hand."
    elif p.current_room == cerner_booth and item in ['cocktail', 'champagne', 'shrimp cocktail', 'drink', 'shrimp']:
        msg = "You eat shrimp and drink champagne until you begin shamelessly flirting with the cute bartender."
    else: 
        obj = p.take_room_item(p.current_room, item)
        if obj:
            p.inventory.add(obj)
            msg = f"You pick up the {obj}."
        else:
            if item == 'furby' and p.current_room == shared_office_area:
                msg = "You cannot take the furby. It does not want to go with you."
            elif p.byers_items.find(item):
                msg = "You'll have to ask Byers for that..."
            elif item in ['honey stingers', 'honey stinger', 'beer cozies', 'beer cozy'] and p.current_room == xtract_booth:
                msg = "You should leave those for the customers... Maybe when the conference is over you can steal some..."
            else:
                msg = f"There is no {item} here."
    return msg


@when('drop THING')
def drop(p, thing):
    if p.current_room.is_laptop_room:
        msg = "You cannot drop items while using the laptop."
    else:
        obj = p.inventory.take(thing)
        if not obj:
            msg = ('You do not have a %s.' % thing)
        else:
            p.add_room_item(p.current_room, obj)
            msg = ('You drop the %s.' % obj)
    return msg


@when('look')
def look(p):
    if p.current_room.after_event:
        if p.get_event_level() >= 6 and p.current_room.change_on_6:
            msg = str(p.current_room.after_event)
        elif p.get_event_level() >= 5 and not p.current_room.change_on_6:
            msg = str(p.current_room.after_event)
        else:
            msg = str(p.current_room)
    elif p.current_room == slack:
        msg = get_slack_messages(p)
    else:
        msg = str(p.current_room)
    if p.current_room not in [laptop, github, slack]:
        room_items = p.get_room_items(p.current_room)
        if room_items:
            for i in room_items:
                if i is not vials:
                    msg += '\n' + ('A %s is here.' % i)
    return msg


@when('inventory')
def show_inventory(p):
    msg = 'You have:'
    for thing in p.inventory:
        msg += '\n' + str(thing)
    return msg


@when('give RECIPIENT the THING', action='give')
@when('give THING to RECIPIENT', action='give')
@when('feed THING to RECIPIENT', action='feed')
@when('feed RECIPIENT the THING', action='feed')
def feed(p, recipient, thing, action):
    food = p.inventory.take(thing)
    character = characters.find(recipient)
    if not food:
        msg = (f"You do not have a {thing}.")
    elif not character:
        msg = f"You can only {action} things to humans."
    elif not p.current_room.people.find(recipient):
        msg = (f"{recipient} is not here.")
    elif recipient == 'luke' and food == ranch:
        msg = (f"You {action} Luke the ranch."
            " Luke mutes his call to thank you, opens 3 new tabs, and then returns to his call, pacing noticeably faster now.")
    elif recipient == 'byers' and food == burrito:
        p.set_event_level(1)
        msg = (f"You {action} Byers the half breakfast burrito.\n"
            "Byers: \"Thanks! I feel much better now. Do you need anything? An office chair, laptop, standing desk?\"")
    else:
        msg = (f"{recipient} does not want the {thing}.")
        p.inventory.add(food)
    return msg


# Ask Byers for chair, laptop, or desk
@when('ask for ITEM')
@when('ask byers for ITEM')
@when('take ITEM from byers')
@when('ask for ITEM from byers')
@when('get ITEM from byers')
def take_item_from_byers(p, item):
    if p.get_room_items(p.current_room).find(item):
        msg = take(item)
    elif p.current_room == luke_byers_cubicle_area and p.get_event_level() >= 1:
        byers_obj = p.byers_items.take(item)
        if byers_obj:
            p.inventory.add(byers_obj)
            if byers_obj == chair:
                msg = ("Byers proceeds to ask: \"Should it be a rolling chair? What color do you want? Cloth or leather?\""
                    " The two of you discuss this important matter for a while until he eventually gives you a chair.")
            elif byers_obj == laptop_item:
                msg = "Byers gives you the laptop and informs you that he created GitHub and Slack accounts for you."
                p.set_event_level(2)
            else:
                msg = (f"Byers gives you a {item}.") 
        else:
            msg = (f"Byers does not have a {item}.")
    else:
        msg = "You can't do that."
    return msg

@when('talk to a PERSON') # ex: "talk to a patient"
@when('talk to PERSON')
def talk(p, person):
    character = characters.find(person)
    if p.current_room == cerner_booth and person in ['waiter', 'people', 'people in tuxedos', 'person', 
        'people in black tuxedos', 'people in ballgowns', 'people in stunning ballgowns', 'person in ballgown']:
        return "They are occupied at the moment..."
    if not character:
        return "You can only talk to other humans."
    elif not p.current_room.people.find(person):
        return f"{person} cannot hear you."
    level = p.get_event_level()
    msg = character.get_msg(p.current_room, level)
    if character == byers:
        if (level >= 1) and p.byers_items:
            msg += " He asks if you need anything."
            for i in p.byers_items:
                msg += (f" A {i}?")
    elif level == 2 and (character == james or character == nurse):
        p.set_event_level(3)
    elif character == potential_client:
        if p.can_make_sale_here(p.current_room):  # if they can still make a sale here:
            msg += (" At some point, you have the opportunity to make a sale.\n"
                "Do you want to try making the sale? (yes or no)")
            p.set_context('sale_prompt')
        else:
            msg += " After a few minutes of this, they randomly walk away without saying anything. You notice that their pockets are full of the free beer cozies..."
    return msg


# INTERACTIONS WITH THINGS IN ROOM
@when('install teamviewer', action='install', thing='')
@when('install teamviewer on computer', action='install', thing='')
@when('install teamviewer on terminal', action='install', thing='')
@when('join the call', action='join call', thing='')
@when('join call', action='join call', thing='')
@when('erase whiteboard', action='erase board', thing='')
@when('write on whiteboard', action='write on board', thing='')
@when('drink THING', action='drink')
@when('turn on THING', action='turn on')
@when('look at THING', action='look')
@when('use THING', action='use')
@when('interact with THING', action='interact')
def interact(p, action, thing):
    if characters.find(thing): # if thing is person
        return talk(thing)
    cr = p.current_room
    msg = "I don't understand that command..." # default message
    if action == 'turn on' and (thing not in ['tv', 'computer', 'terminal'] or cr in [wy_injection_area,  bc_injection_area]):
        return msg
    if action == 'drink' and cr == cerner_booth:
        return take(p, thing)
    level = p.get_event_level()
    if cr == shared_office_area:
        if thing == 'furby':
            msg = "The furby stares deep into your soul."
    elif cr == zoe_madden_office:
        if thing in ["madden's desk", "madden desk", "maddens desk"]:
            msg = "It looks like it has been vacant for a long time. You silently shed a tear."
    elif cr == conference_room:
        if thing == 'tv' and (action == 'turn on' or action == 'interact'):
            msg = "You attempt to use the TV, but can't find the right input and eventually give up."
        elif action == 'erase board':
            msg = "You attempt to erase the stuff on the board, but it has been there too long and cannot be erased."
        elif action == 'write on board':
            msg = "You try to write on the board but the markers are all too dry."
        elif thing == 'whiteboard': 
            msg = "There are markers and erasers here. Perhaps you could try to write on it or erase the random scribbles."
    elif cr == demo_room:
        if action == 'join call':
            msg = "You find yourself on a call with Luke, Scott, James, and several customers."
            # if they can still make a sale here:
            if p.can_make_sale_here(cr):
                msg += (" At some point in the call, you have the opportunity to make a sale.\n"
                    "Do you want to try making the sale? (yes or no)")
                p.set_context('sale_prompt')
            else:
                msg += " After some time, the call ends. It was uneventful."
    elif cr == rosch_booth:
        if thing in ['computer', 'antiquated']:
            msg = ("You turn on the computer. You hear a low hum that gets louder and louder. It quickly turns into clunking as"
                " smoke begins to pour out of the side of the machine. You quickly turn off the computer and back away.")
    elif cr == xtract_booth:
        if thing in ['table', 'conference goodies', 'the table']:
            msg = "you see an abundance of Xtract Solutions branded beer cozies and honey stingers strewn across the table."
        elif thing == "poster":
            msg = "this is a nice poster."
    elif cr == bc_lobby and thing in ['microsoft surface', 'surface', 'microsoft surface' 'ms surface']:
        msg = "Nothing happens. You see the power cord hanging from the back..."
    elif cr == bc_injection_area:
        if thing == 'computer':
            msg = "You are scolded for poor HIPAA practices."
        elif thing in ['needle', 'injection needle', 'syringe']:
            msg = "You try to take the injection needle but the nurse karate chops it out of your hand."
    elif cr == bc_mixing_area:
        if thing in ['fridge', 'refrigerator']:
            msg = "You open the fridge and see that it is full of patient vials."
        elif thing in ['automated mixing assistant', 'ama']:
            msg = "Be careful, these are no longer supported... If you break it, you buy it!"
    elif cr == wy_lobby:
        if thing in ['microsoft surface login kiosk', 'microsoft surface', 'login kiosk', 'kiosk']:
            msg = "The screen says: 404 not found" if level < 6 else "The login kiosk is so popular! You notice that everyone has a smile on their face after using it."
    elif cr == wy_injection_area:
        if thing in ['summit', 'computer']:
            msg = "Summit isn't working." if level < 6 else "Summit is working great! Now HIPAA-dee hop off that computer!"
    elif cr == wy_server_room:
        if action == 'install' and level < 6:
            msg = "You notice Byers login... Suddenly everything begins working... Summit is up!"
            p.set_event_level(6)
        if thing in ['terminal', 'computer', 'the terminal']:
            msg = ("You note the absence of teamviewer... Perhaps if you *install teamviewer*, Byers could help..."
                "\nThe IT guy is currently peeking over your shoulder.") if level < 6 else "They don't want you using this now."
    return msg



@when('yes', context='sale_prompt', action='yes')
@when('no', context='sale_prompt', action='no')
def try_making_sale(p, action):
    p.set_context(None)
    level = p.get_event_level()
    if action == 'no':
        return " You have decided not to try selling to them right now."
    if level == 4:
        msg = "You successfully make the sale! Yipee!!! Perhaps you should go to the airport to check in on your new customer, Weyland-Yutani."
        p.set_event_level(5)
    elif level >= 5:
        msg = "Suddenly a large dinosaur comes and eats your perspective client. Oh darn... Well, you win some, you lose some."
        p.sale_rooms.pop(p.current_room)
    else:
        p.sale_rooms.pop(p.current_room)
        if p.sale_rooms:
            for room in p.sale_rooms.keys():
                msg = f"You lost this sale but you get one more try {p.sale_rooms[room]}."
                msg += "\n Perhaps next time you should try creating a relevant issue on GitHub first. Maybe if you ask around you'll get some ideas for things to add to Summit..."
        else:
            msg = (f"You lost the sale...\n"
                "Xtract has failed to meet its sales goals. It is unceremoniously dismantled and sold to its competitors..."
                " Out of nowhere, Luke is eaten by a dragon... All that remains of to prove that we were ever here are Xtract Solutions beer cozies.")
            p.set_context('game_over')
    return msg


@when('scream', action='scream')
@when('shout', action='shout')
@when('yell', action='yell')
def scream(p, action):
    msg = (f"You {action}: AAAAAAAAAAAAAGGHHHH!!!")
    return msg
