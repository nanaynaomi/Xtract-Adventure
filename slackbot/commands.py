from mod_adventurelib import *
from rooms import *
from items import *


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
def go_to(room, e_key):
    global current_room
    if get_context() != None:
        set_context(None)
    if room in room_connections[current_room]:
        if current_room == car and room == pdx_airport:
            msg = "You drive to PDX airport.\n"
        else:
            msg = f"You {room_entry[e_key]}.\n"
        current_room = room
        if room == shared_office_area and get_event_level() == 6:
            msg += the_end()
        else:
            msg += look()
    elif e_key == 'ws' and current_room == shared_office_area:
        msg = ("It\'s a dark, scary place. You are likely to be eaten by a grue.\n"
        "You turn back in fear and do not enter the room")
    else:
        msg = "You cannot access that from where you currently are."
    return msg


def the_end():
    set_event_level(7)
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
def laptop_access(room, e_key):
    global previous_room
    if inventory.find('laptop'): # If player has the laptop
        if current_room == laptop and e_key == 'close_laptop':
            msg = laptop_navigation(previous_room, e_key)
        elif room and room in room_connections[current_room]:
            if e_key == 'open_laptop':
                previous_room = current_room
            msg = laptop_navigation(room, e_key)
        else:
            msg = "You can't access that from where you currently are."
    else:
        msg = "You need a laptop to do that."
    return msg


def laptop_navigation(room, e_key):
    global current_room
    if inventory.find('laptop'):
        if get_context() != None:
            set_context(None)
        msg = f"You {room_entry[e_key]}.\n"
        current_room = room
        msg += '\n'+look()
    return msg


@when('where can i go')
def where_can_i_go():
    ''' Tells a player where they can go based on their current location/Room'''
    if current_room == fridge:
        msg = "You must close fridge."
    else:
        ignore_laptop = False if inventory.find('laptop') else True
        msg = "Where you can go:"
        if current_room == car or current_room == pdx_airport:
            rm_guide = car_pdx_room_guide
        else:
            rm_guide = room_guide
        for room in room_connections[current_room]:
            if ignore_laptop and room == laptop:
                msg += ""
            else:
                msg += f"\n{rm_guide[room]}"
        if current_room == shared_office_area:
            msg += f"\nWS - Workshop"
        elif current_room == laptop:
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
def github_issue():
    if current_room == github:
        if get_event_level() >= 4:
            msg = "You already created a good issue. That's enough for today."
        else:
            set_context('creating_issue')
            msg = "You are now creating an issue. Please enter the title of your issue like so: 'issue YOUR TITLE'"
    else:
        msg = "You need to be on GitHub to do that."
    return msg


@when('issue TITLE', context='creating_issue')
def issue_title(title):
    key_words = ["cat videos", "cat video", "cats", "more information", "smaller space", "red lines", "transparent ink", "transparent red", "red"]
    if any(word in title for word in key_words):
        msg = "Issue created! - Success! \n ~ You have a new Slack notification. ~"
        set_event_level(4)
    else:
        msg = "Issue created! - Issue rejected by Andrew with comment: \"no\"."
    set_context(None)
    msg += '\n' + "You are in an Xtract Solutions GitHub Repository, on the \"Issues\" page."
    return msg

@when('check notifications')
@when('check slack notifications')
@when('notifications')
@when('notification')
@when('check slack')
def slack_notifications():
    if current_room == slack:
        if get_event_level() >= 4:
            msg = ("Notification: Your issue, [ISSUE HERE], has been completed and there is a new release of Summit."  
                "The customers will love this. This would have taken months before Addama...")
        else:
            msg = "Work out details of Slack later..."
    else:
        msg = "Open Slack (in the game) to view notifications"
    return msg


# GENERAL: ----------------------------------------------------------------


@when('take ITEM')
def take(item):
    if current_room.is_laptop_room:
        msg = "You cannot pick up items while using laptop."
    elif item == 'mug' and current_room == conference_room:
        msg = "Hmm... instant oatmeal... Steve has been here. You leave the mug on the table."
    else: 
        obj = current_room.items.take(item)
        if obj:
            inventory.add(obj)
            msg = f"You pick up the {obj}."
        else:
            if item == 'furby' and current_room == shared_office_area:
                msg = "You cannot take that."
            elif byers_items.find(item):
                msg = "You'll have to ask Byers for that..."
            else:
                msg = f"There is no {item} here."
    return msg


@when('drop THING')
def drop( thing):
    if current_room.is_laptop_room:
        msg = "You cannot drop items while using laptop."
    else:
        obj = inventory.take(thing)
        if not obj:
            msg = ('You do not have a %s.' % thing)
        else:
            current_room.items.add(obj)
            msg = ('You drop the %s.' % obj)
    return msg


@when('look')
def look():
    if current_room.after_event:
        if get_event_level() >= 6 and current_room.change_on_6:
            msg = str(current_room.after_event)
        elif get_event_level() >= 5 and not current_room.change_on_6:
            msg = str(current_room.after_event)
        else:
            msg = str(current_room)
    else:
        msg = str(current_room)
    if current_room.items:
        for i in current_room.items:
            msg += '\n' + ('A %s is here.' % i)
    return msg


@when('inventory')
def show_inventory():
    msg = 'You have:'
    for thing in inventory:
        msg += '\n' + str(thing)
    return msg


@when('give RECIPIENT the THING', action='give')
@when('give THING to RECIPIENT', action='give')
@when('feed THING to RECIPIENT', action='feed')
@when('feed RECIPIENT the THING', action='feed')
def feed(recipient, thing, action):
    food = inventory.take(thing)
    character = characters.find(recipient)
    if not food:
        msg = (f"You do not have a {thing}.")
    elif not character:
        msg = f"You can only {action} things to humans."
    elif not current_room.people.find(recipient):
        msg = (f"{recipient} is not here.")
    elif recipient == 'luke' and food == ranch:
        msg = (f"You {action} Luke the ranch."
            " Luke mutes his call to thank you, opens 3 new tabs, and then returns to his call, pacing noticeably faster now.")
    elif recipient == 'byers' and food == burrito:
        set_event_level(1)
        msg = (f"You {action} Byers the half breakfast burrito.\n"
            "Byers: \"Thanks! I feel much better now. Do you need anything? An office chair, laptop, standing desk?\"")
    else:
        msg = (f"{recipient} does not want the {thing}.")
        inventory.add(food)
    return msg


# Ask Byers for chair, laptop, or desk
@when('ask for ITEM')
@when('ask byers for ITEM')
@when('take ITEM from byers')
@when('ask for ITEM from byers')
@when('get ITEM from byers')
def take_item_from_byers(item):
    if current_room.items.find(item):
        msg = take(item)
    elif current_room == luke_byers_cubicle_area and get_event_level() >= 1:
        byers_obj = byers_items.take(item)
        if byers_obj:
            inventory.add(byers_obj)
            if byers_obj == chair:
                msg = ("Byers proceeds to ask: \"Should it be a rolling chair? What color do you want? Cloth or leather?\""
                    " The two of you discuss this important matter for a while until he eventually gives you a chair.")
            elif byers_obj == laptop_item:
                msg = "Byers gives you the laptop and informs you that he created GitHub and Slack accounts for you."
                set_event_level(2)
            else:
                msg = (f"Byers gives you a {item}.") 
        else:
            msg = (f"Byers does not have a {item}.")
    else:
        msg = "You can't do that."
    return msg


@when('talk to PERSON')
def talk(person):
    if person in ['perspective client','client']:
        person = 'potential client'
    character = characters.find(person)
    if not character:
        msg = ("You can only talk to other humans.")
    elif not current_room.people.find(person):
        msg = (f"{person} cannot hear you.")
    else:
        msg = (f"{character.subject_pronoun} is busy right now.") # default message just in case.
        level = get_event_level()
        if character == andrew:
            msg = "Andrew: \"No.\""
        elif character == byers:
            msg = ""
            if level == 0:
                msg = "Byers mutters something about being too hungry to think..."
            elif level == 5:
                msg = "Byers mentions that he cannot contact your customers server. "
            if (level >= 1) and byers_items:
                msg += "He asks if you need anything."
                for i in byers_items:
                    msg += (f" A {i}?")
        elif character == graham:
            msg = ("Graham is on the phone with a customer who is furious that Summit isn't working."
                " He is politely asking them to try turning on their computer and they are insisting the"
                " software should do it for them.")
        elif character == james and current_room == xtract_booth:
            msg = ("You hear James making his pitch... \"pain funnel... 3rd party story... pain funnel...\" then you hear James ask,"
                " \"So what's stopping you from signing today?\" to which the potential customer responds:"
                " \"Well... our reports absolutely must have red lines with transparent ink and I don't see where Summit supports that.\""
                " You think to yourself, that sounds like an absolutely horrible idea.") # put in italics later...?
            if level == 2:
                set_event_level(3)
        elif character == nurse:
            if current_room == bc_injection_area:
                msg = "Nurse: \"I have a suggestion: Could you have Summit show more information in a smaller space?\""
            elif current_room == bc_mixing_area:
                msg = "Nurse: \"Hey, you should add cat videos to Summit. That would be really useful I think.\""
            if level == 2:
                set_event_level(3)
        elif character == potential_client:
            msg = "You start chatting with the potential client."
            # if they can still make a sale here:
            if current_room.can_make_sale_here:
                msg += (" At some point, you have the opportunity to make a sale.\n"
                    "Do you want to try making the sale? (yes or no)")
                set_context('sale_prompt')
            else:
                msg += " After a few minutes of this, they randomly walk away without saying anything. You notice that their pockets are full of the free beer cozies..."
        elif character == wei:
            if level <= 1:
                msg = "Wei: \"You should talk to Byers if you need a computer.\""
            else: 
                msg = "She finds 3 new bugs in your code and assigns the issues back to you."
        elif character == luke:
            msg = "Luke is busy talking on the phone."
        elif character == zoe:
            if level >= 5:
                msg = "She is busy working on the security questionnaire for the new customer. She mentions something about being on question 3 of 2739."
            else:
                msg = "She tells you that we need a new customer."
    return msg


# INTERACTIONS
@when('install THING', action='install')
@when('join the call', action='join call', thing='')
@when('join call', action='join call', thing='')
@when('erase whiteboard', action='erase board', thing='')
@when('write on whiteboard', action='write on board', thing='')
@when('turn on THING', action='turn on')
@when('look at THING', action='look')
@when('use THING', action='use')
@when('interact with THING', action='interact')
def interact(action, thing):
    if characters.find(thing): # if thing is person
        return talk(thing)
    else:
        msg = 'You cannot do that. Try phrasing it differently...' # default message for now...
        if current_room == shared_office_area:
            if thing == 'furby':
                msg = "The furby stares deep into your soul."
        elif current_room == zoe_madden_office:
            if thing in ["madden's desk", "madden desk", "maddens desk"]:
                msg = "It looks like it has been vacant for a long time. You silently shed a tear."
        elif current_room == conference_room:
            if thing == 'tv' and (action == 'turn on' or action == 'interact'):
                msg = "You attempt to use the TV, but can't find the right input and eventually give up."
            elif action == 'erase board':
                msg = "You attempt to erase the stuff on the board, but it has been there too long and cannot be erased."
            elif action == 'write on board':
                msg = "You try to write on the board but the markers are all too dry."
            elif thing == 'whiteboard':
                msg = "There are markers and erasers here. Perhaps you could try to write on it or erase the random scribbles."
        elif current_room == demo_room:
            if action == 'join call':
                msg = "You find yourself on a call with Luke, Scott, James, and several customers."
                # if they can still make a sale here:
                if current_room.can_make_sale_here:
                    msg += (" At some point in the call, you have the opportunity to make a sale.\n"
                        "Do you want to try making the sale? (yes or no)")
                    set_context('sale_prompt')
                else:
                    msg += " After some time, the call ends. It was uneventful."
        elif current_room == xtract_booth:
            if thing in ['table', 'conference goodies', 'the table']:
                msg = "you see an abundance of Xtract Solutions branded beer cozies and honey stingers strewn across the table."
            elif thing == "poster":
                msg = "this is a nice poster."
        elif current_room == wy_server_room:
            if action == 'install' and thing in ['teamviewer', 'teamviewer on computer', 'teamviewer on terminal']:
                msg = "You notice Byers login... Suddenly everything begins working... Summit is up!"
                set_event_level(6)
            if thing in ['terminal', 'computer', 'the terminal']:
                msg = "You note the absence of teamviewer... Perhaps if you installed it, Byers could help..."
    return msg


@when('yes', context='sale_prompt', action='yes')
@when('no', context='sale_prompt', action='no')
def try_making_sale(action):
    set_context(None)
    level = get_event_level()
    if action == 'no':
        return " You have decided not to try selling to them right now."
    if level == 4:
        msg = "You successfully make the sale! Yipee!!! Perhaps you should go to the airport to check in on your new customer, Weyland-Yutani."
        set_event_level(5)
        room_connections[pdx_airport].append(wy_lobby)
    elif level >= 5:
        msg = "Suddenly a large dinosaur comes and eats your perspective client. Oh darn... Well, you win some, you lose some."
        current_room.can_make_sale_here = False
        sale_rooms.pop(current_room)
    else:
        current_room.can_make_sale_here = False
        sale_rooms.pop(current_room)
        if sale_rooms:
            for room in sale_rooms.keys():
                msg = f"You lost this sale but you get one more try {sale_rooms[room]}."
        else:
            msg = (f"You lost the sale...\n"
                "Xtract has failed to meet its sales goals. It is unceremoniously dismantled and sold to its competitors..."
                " Out of nowhere, Luke is eaten by a dragon... All that remains of to prove that we were ever here are Xtract Solutions beer cozies.")
            set_context('game_over')
    return msg


@when('scream', action='scream')
@when('shout', action='shout')
@when('yell', action='yell')
def scream(action):
    msg = (f"You {action}: AAAAAAAAAAAAAGGHHHH!!!")
    return msg
