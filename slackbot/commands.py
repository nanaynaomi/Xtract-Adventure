from mod_adventurelib import *
from rooms import *
from characters import *
from items import *
from help import *
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
    if p.current_room == fridge and e_key != 'close_fridge':
        return "You need to *close the fridge* before going anywhere."
    if room in p.current_room.connections: 
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
    if p.inventory.find('laptop'): 
        if p.current_room.is_laptop_room and e_key == 'close_laptop':
            return laptop_navigation(p, p.previous_room, e_key)
        elif p.current_room == fridge and room != fridge:
            return "You need to *close the fridge* before going anywhere."
        elif room and not p.current_room.is_laptop_room and e_key == 'open_laptop':
            p.previous_room = p.current_room
        if room and room in p.current_room.connections:
            msg = laptop_navigation(p, room, e_key)
        else:
            msg = "You can't access that from where you currently are."
    else:
        msg = "You need a laptop to do that."
        if p.get_event_level() < 2: # Player has not gotten the laptop from Byers yet.
            msg += " Byers should be able to give you a laptop."
    return msg


def laptop_navigation(p, room, e_key):
    if p.inventory.find('laptop'):
        if p.get_context() != None:
            p.set_context(None)
        msg = f"You {room_entry[e_key]}.\n"
        p.set_current_room(room)
        msg += '\n'+look(p)
    return msg


@when('open THING', action='open')
def open_thing(p, thing, action):
    if any(word in thing for word in ["fridge", "refrigerator", "mini-fridge", "mini fridge"]):
        return go_to(p, fridge, "open_fridge")
    elif any(word in thing for word in ["laptop", "computer"]):
        return laptop_access(p, laptop, "open_laptop")
    elif 'notifications' in thing:
        return slack_notifications(p)
    elif 'github' in thing:
        return laptop_access(p, github, 'open_github')
    elif 'slack' in thing:
        return laptop_access(p, slack, 'open_slack')
    return f"You cannot {action} {thing}"


@when('close THING', action='close')
def close_thing(p, thing, action):
    if any(word in thing for word in ["fridge", "refrigerator", "mini-fridge", "mini fridge"]):
        return go_to(p, shared_office_area, "close_fridge")
    elif any(word in thing for word in ["laptop", "computer"]):
        return laptop_access(p, None, "close_laptop")
    elif 'github' in thing:
        return laptop_access(p, laptop, 'close_github')
    elif 'slack' in thing:
        return laptop_access(p, laptop, 'close_slack')
    return f"You cannot {action} {thing}"


@when('where can i go')
def where_can_i_go(p):
    ''' Tells a player where they can go based on their current location/Room'''
    cr = p.current_room
    if cr == fridge:
        msg = "You need to *close the fridge* before going anywhere."
    else:
        ignore_laptop = False if p.inventory.find('laptop') else True
        msg = "Where you can go:"
        if cr == slack or cr == github:
            ignore_laptop = True
        if cr == car or cr == pdx_airport:
            rm_guide = car_pdx_room_guide
        else:
            rm_guide = room_guide
        for room in cr.connections:
            if (ignore_laptop and room == laptop) or (room == wy_lobby and p.get_event_level() < 5):
                msg += ""
            else:
                msg += f"\n{rm_guide[room]}"
        if cr == shared_office_area:
            msg += "\nWS - Workshop"
        elif cr.is_laptop_room:
            if cr == slack:
                msg += "\nClose Slack"
            elif cr == github:
                msg += "\nClose GitHub"
            msg += "\nClose laptop"
        msg += "\nIf you would like to see a map of where you currently are, say *'map'*."
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
        p.have_notifications = False
        return slack.notifications[level]
    return "Open Slack (in the game) to view notifications"

def get_slack_messages(p):
    random.seed()
    num = random.randint(0,len(slack.messages)-1)
    msg = f"{slack.messages[num]}"
    if p.have_notifications:
        msg += "\n:bell: You have notifications."
    return msg


# HELP: ----------------------------------------------------------------

@when('objective')
def objective(p):
    level = p.get_event_level()
    return f"Current Objective: {objectives[level]}\n(If you are stuck and would like a detailed hint about the current objective, say *'hint'*.)"

@when('hint')
def obj_hint(p):
    level = p.get_event_level()
    return f"Hint: {hints[level]}"

@when('help')
def help(p):
    msg = "Guide to some of the main commands: (NOT case sensitive)"
    if p.get_event_level() >= 2:
        msg += "\nopen laptop / close laptop - Access your laptop."
    for c in help_cmds:
        msg += (f"\n{c}")
    msg += ("\n (*Note:* there are many other commands besides these that you can try."
       " The game is designed to expect you to respond with whatever feels intuitive to you."
       " When in doubt, try typing something - and if it doesn't work, rephrase it and try again.)")
    return msg

@when('tips')
def get_tips(p):
    return tips


# GENERAL: ----------------------------------------------------------------

@when('take ITEM')
@when('take the ITEM')
def take(p, item):
    cr = p.current_room
    if cr.is_laptop_room:
        return "You cannot pick up items while using laptop."
    elif cr == conference_room and item == 'mug':
        return "Hmm... instant oatmeal... Steve has been here. You leave the mug on the table."
    elif cr == luke_byers_cubicle_area and p.get_event_level() >= 1 and any(word in item for word in ['laptop', 'desk', 'chair']):
        return take_item_from_byers(p, item)
    obj = p.take_room_item(cr, item)
    if obj:
        p.inventory.add(obj)
        return f"You pick up the {obj}."
    else:
        if item == 'furby' and cr == shared_office_area:
            return "You cannot take the furby. It does not want to go with you."
        elif p.byers_items.find(item):
            return "You'll have to ask Byers for that..."
        elif cr == xtract_booth and item in ['honey stingers', 'honey stinger', 'beer cozies', 'beer cozy']:
            return "You should leave those for the customers... Maybe when the conference is over you can steal some..."
        elif cr == wy_injection_area and item in ['needle', 'injection needle', 'syringe']:
            return "You try to take the injection needle but the nurse karate chops it out of your hand."
        elif cr == cerner_booth and item in ['cocktail', 'champagne', 'shrimp cocktail', 'drink', 'shrimp']:
            return "You eat shrimp and drink champagne until you begin shamelessly flirting with the cute bartender."
        elif item in ["computer", "luke's computer", "old computer", "antique computer"]:
            return "You cannot take someone else's computer."
    return f"You cannot take {item}."

@when('drop the THING')
@when('drop THING')
def drop(p, thing):
    if p.current_room.is_laptop_room:
        return "You cannot drop items while using the laptop."
    obj = p.inventory.take(thing)
    if not obj:
        return ('You do not have a %s.' % thing)
    p.add_room_item(p.current_room, obj)
    return ('You drop the %s.' % obj)


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
    if p.inventory.is_empty():
        return "Your inventory is currently empty."
    msg = 'You have:'
    for thing in p.inventory:
        msg += '\n' + str(thing)
    return msg


@when('give RECIPIENT the THING', action='give')
@when('give THING to RECIPIENT', action='give')
@when('give the THING to RECIPIENT', action='give')
@when('feed THING to RECIPIENT', action='feed')
@when('feed the THING to RECIPIENT', action='feed')
@when('feed RECIPIENT the THING', action='feed')
def feed(p, recipient, thing, action):
    food = p.inventory.take(thing)
    character = characters.find(recipient)
    if not food:
        return f"You do not have a {thing}."
    elif not character:
        p.inventory.add(food)
        return f"You can only {action} things to humans."
    elif not p.current_room.people.find(recipient):
        p.inventory.add(food)
        return f"{recipient} is not here."
    elif recipient == 'luke' and food == ranch:
        return (f"You {action} Luke the ranch."
            " Luke mutes his call to thank you, opens 3 new tabs, and then returns to his call, pacing noticeably faster now.")
    elif recipient == 'byers' and food == burrito:
        p.set_event_level(1)
        return (f"You {action} Byers the {thing}.\n"
            "Byers: \"Thanks! I feel much better now. Do you need anything? An office chair, laptop, standing desk?\"")
    p.inventory.add(food) # put it back in your inventory
    return f"{recipient} does not want the {thing}."


# Ask Byers for chair, laptop, or desk
@when('ask ITEM')
@when('get ITEM')
@when('laptop', item='laptop')
@when('chair', item='chair')
@when('desk', item='desk')
def take_item_from_byers(p, item):
    if p.current_room == luke_byers_cubicle_area and p.get_event_level() >= 1:
        for object in ["laptop", "chair", "desk"]: 
            if object in item: # example: if the word "laptop" exists anywhere within ITEM
                item = object
        byers_obj = p.byers_items.take(item)
        if byers_obj:
            p.inventory.add(byers_obj)
            if byers_obj == chair:
                return ("Byers proceeds to ask: \"Should it be a rolling chair? What color do you want? Cloth or leather?\""
                    " The two of you discuss this important matter for a while until he eventually gives you a chair.")
            elif byers_obj == laptop_item:
                p.set_event_level(2)
                return "Byers gives you the laptop and informs you that he created GitHub and Slack accounts for you."
            else:
                return (f"Byers gives you a {item}.") 
        return (f"He does not have that.")
    if p.get_event_level() >= 2 and item == 'laptop' and not p.current_room.is_laptop_room and p.inventory.find('laptop'):
        return "To open your laptop, say: *'open laptop'*"
    return "You can't do that."


@when('talk to a PERSON') # ex: "talk to a patient"
@when('talk to PERSON')
@when('speak to PERSON')
def talk(p, person):
    character = characters.find(person)
    if p.current_room == cerner_booth and any(word in person for word in ['waiter', 'people', 'tuxedo', 'person', 'ballgown']):
        return "They are occupied at the moment..."
    if not character:
        return "Character name not recognized."
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
            msg += (f" At some point, you have the opportunity to make a sale. {p.hint_dont_sell()}"
                "\nDo you want to try making the sale? (yes or no)")
            p.set_context('sale_prompt')
        else:
            msg += " After a few minutes of this, they randomly walk away without saying anything. You notice that their pockets are full of the free beer cozies..."
    return msg


# INTERACTIONS WITH THINGS IN ROOM
@when('install teamviewer', action='install', thing='teamviewer')
@when('install teamviewer on computer', action='install', thing='teamviewer')
@when('install teamviewer on terminal', action='install', thing='teamviewer')
@when('join the call', action='join', thing='call')
@when('join call', action='join', thing='call')
@when('erase THING', action='erase')
@when('write on THING', action='write on')
@when('drink THING', action='drink')
@when('turn on THING', action='turn on')
@when('look at the THING', action='look at')
@when('look at THING', action='look at')
@when('use the THING', action='use')
@when('use THING', action='use')
@when('interact with the THING', action='interact with')
@when('interact with THING', action='interact with')
def interact(p, action, thing):
    if characters.find(thing) and action not in ['drink', 'turn on', 'use']: # if thing is person
        return talk(p, thing)
    cr = p.current_room
    msg = f"You cannot {action} {thing}." # default message
    if action == 'turn on' and (not any(word in thing for word in ['tv', 'computer', 'terminal', 'laptop']) or cr in [wy_injection_area,  bc_injection_area]):
        return "You can't turn that on."
    elif action == 'drink':
        return take(p, thing) if cr == cerner_booth else msg
    elif action in ['erase', 'write on'] and not any(word in thing for word in ['board', 'whiteboard', 'scribbles']):
        return msg
    elif thing == "laptop" and action in ['use', 'interact with', 'turn on']:
        return laptop_access(p, laptop, 'open_laptop')
    level = p.get_event_level()

    if cr == shared_office_area:
        if thing == "furby":
            return "The furby stares deep into your soul."
        elif thing == "bookshelf":
            return "There are many random items on this shelf. Let's leave them be."
        elif thing in ["desk", "desks"]:
            return "Probably should just leave the desks alone..."
        elif thing == "front door":
            return "The front door leads out to the parking lot, where your car is." if action == "look at" else go_to(p, car, 'car')
        elif thing in ["kitchen", "kitchen area", "small kitchen area"]:
            if p.get_room_items(fridge).find("burrito"): # If burrito in fridge:
                return "Perhaps you should *open the fridge* and see if there's something in there that Byers might want."
            return "Just a standard little kitchen area. Not much to do here."
        elif thing in ["fridge", "mini fridge", "mini-fridge", "refrigerator"]:
            return go_to(p, fridge, "open_fridge")

    elif cr == conference_room:
        if thing == 'tv':
            if action in ['turn on', 'use', 'interact with']:
                return "You attempt to use the TV, but can't find the right input and eventually give up."
            return "The TV is off."
        elif action == 'erase' or (action != 'look at' and thing == 'eraser'):
            return "You attempt to erase the stuff on the board, but it has been there too long and cannot be erased."
        elif action == 'write on' or (action != 'look at' and thing == 'marker'):
            return "You try to write on the board but the markers are all too dry."
        elif 'board' in thing: 
            return "There are markers and erasers here. Perhaps you could try to write on it or erase the random scribbles."
        elif thing in ['random scribbles', 'scribbles', 'writing', 'random gibberish', 'gibberish'] and action != 'use':
            return "You examine the writing on the board, and conclude that it is just nonsensical gibberish."
        elif thing in ['mechanical contraptions', 'contraptions', 'mechanical contraption', 'contraption', 'vials', 'miscellaneous vials']:
            return "Probably best to leave that stuff alone."
        elif thing == 'table':
            return "It's just a big table. Not much to do with it."

    elif cr == demo_room:
        if action == 'join' or thing == 'computer':
            msg = "You find yourself on a call with Luke, Scott, James, and several customers."
            # if they can still make a sale here:
            if p.can_make_sale_here(cr):
                msg += (f" At some point in the call, you have the opportunity to make a sale. {p.hint_dont_sell()}"
                    "\nDo you want to try making the sale? (yes or no)")
                p.set_context('sale_prompt')
            else:
                msg += " After some time, the call ends. It was uneventful."
    
    elif cr == zoe_madden_office:
        if thing == 'desk':
            return "There is more than one desk in the room."
        if "madden" in thing and "desk" in thing:
            return "Madden's desk looks like it has been vacant for a long time. You silently shed a tear."
        elif 'board' in thing:
            if action == 'look at':
                return "The board is full of information."
            return "This board looks carefully written - probably not a good idea to mess with it."
        elif ('zoë' in thing or 'zoe' in thing) and 'desk' in thing:
            return "Her desk is very organized."

    elif cr == wy_lobby:
        if thing in ['microsoft surface login kiosk', 'microsoft surface', 'login kiosk', 'kiosk']:
            return "The screen says: 404 not found" if level < 6 else "The login kiosk is so popular! You notice that everyone has a smile on their face after using it."
    
    elif cr == wy_server_room:
        if action == 'install' and level < 6:
            p.set_event_level(6)
            return "You notice Byers login... Suddenly everything begins working... Summit is up!"
        if thing in ['terminal', 'computer']:
            return ("You note the absence of teamviewer... Perhaps if you *install teamviewer*, Byers could help..."
                "\nThe IT guy is currently peeking over your shoulder.") if level < 6 else "They don't want you using this now."

    elif cr == wy_injection_area:
        if thing in ['summit', 'computer']:
            return "Summit isn't working." if level < 6 else "Summit is working great! Now HIPAA-dee hop off that computer!"

    elif cr == bc_lobby:
        if 'surface' in thing or 'microsoft' in thing:
            return "Nothing happens. You see the power cord hanging from the back..."
        elif 'chair' in thing in ["chair", "chairs"]:
            return "Nothing much you can do with these chairs."
        elif thing == "front desk" and action == "look at":
            return "You look at the front desk. Nothing happens. Wow. That was exciting..."

    elif cr == bc_injection_area:
        if thing == 'computer':
            return "You are scolded for poor HIPAA practices."
        elif thing in ['needle', 'injection needle', 'syringe']:
            return "You try to take the injection needle but the nurse karate chops it out of your hand."

    elif cr == bc_mixing_area:
        if thing in ['fridge', 'refrigerator']:
            return "You open the fridge and see that it is full of patient vials."
        elif thing in ['vials', 'patient vials']:
            return "You probably shouldn't mess with those..."
        elif thing in ['automated mixing assistant', 'ama', 'mixing assistant']:
            return "Be careful, these are no longer supported... If you break it, you buy it!"

    elif cr == ts_main_area:
        if action == 'look at' and thing in ["rows of booths", "booths"]:
            return "There are many booths."

    elif cr == xtract_booth:
        if thing in ['table', 'conference goodies', 'goodies']:
            return "you see an abundance of Xtract Solutions branded beer cozies and honey stingers strewn across the table."
        elif thing == "poster":
            return "this is a nice poster."
    
    elif cr == rosch_booth:
        if thing in ['computer', 'antiquated']:
            return ("You turn on the computer. You hear a low hum that gets louder and louder. It quickly turns into clunking as"
                " smoke begins to pour out of the side of the machine. You quickly turn off the computer and back away.")

    elif cr == cerner_booth:
        if action == 'look at':
            return "So fancy!"
        elif thing in ["banquet table", "table", "free champagne", "champagne", "cocktails", "cocktail", "drink"]:
            return "You eat shrimp and drink champagne until you begin shamelessly flirting with the cute bartender."

    elif "computer" in thing: # Default for any other computer we come across if someone looks at it.
        if action == "interact with":
            return "Yep, that's a computer. It's got like a screen and everything."
        elif action in ["use", "interact with"]:
            msg = "You cannot use that computer."
            if p.inventory.find("laptop"):
                msg += " The only computer you can use in this room is your own laptop."

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
                msg += "\n*Hint:* Perhaps next time you should try creating a relevant issue on GitHub first. Maybe if you ask around you'll get some ideas for things to add to Summit..."
        else:
            msg = (f"You lost the sale...\n"
                "Xtract has failed to meet its sales goals. It is unceremoniously dismantled and sold to its competitors..."
                " Out of nowhere, Luke is eaten by a dragon... All that remains of to prove that we were ever here are Xtract Solutions beer cozies.")
            p.set_context('game_over')
    return msg

# RANDOM FUN COMMANDS: --------------------------------------------------

@when('scream', action='scream')
@when('shout', action='shout')
@when('yell', action='yell')
def scream(p, action):
    return f"You {action}: AAAAAAAAAAAAAGGHHHH!!!"

@when('cry')
def cry(p):
    return "You sob quietly for a few minutes."

@when('laugh')
def laugh(p):
    return "MUAHAHAHAHAHAHAHA"
