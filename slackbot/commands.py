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
@when('xhq', e_key='xhq', room=shared_office_area)  # car -> xhq
@when('bc', e_key='bc', room=bc_lobby) # car -> bc
@when('pdx', e_key='pdx', room=pdx_airport) # car -> pdx <- (wy or ts)
@when('wy', e_key='wy', room=wy_lobby) # pdx -> wy
@when('ts', e_key='ts', room=ts_main_area) # pdx -> ts

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
    if room in room_connections[current_room]:
        if current_room == car and room == pdx_airport:
            msg = "You drive to PDX airport.\n"
        else:
            msg = f"You {room_entry[e_key]}.\n"
        current_room = room
        msg += look()
    elif e_key == 'ws' and current_room == shared_office_area:
        msg = ("It\'s a dark, scary place. You are likely to be eaten by a grue.\n"
        "You turn back in fear and do not enter the room")
    else:
        msg = "You cannot access that from where you currently are."
    return msg


@when('open laptop', e_key='open_laptop', room=laptop) # if they don't have laptop in inventory they cant do this
@when('close laptop', e_key='close_laptop', room=previous_room) # room will need to go back to previous room... hmmm...
@when('open slack', e_key='open_slack', room=slack)
@when('close slack', e_key='close_slack', room=laptop)
@when('open github', e_key='open_github', room=github)
@when('close github', e_key='close_github', room=laptop)
def laptop(room, e_key):
    global current_room
    if room in room_connections[current_room]:
        if inventory.find('laptop'): # If player has the laptop
            msg = f"You {room_entry[e_key]}.\n"
            if e_key == 'open_laptop':
                global previous_room
                previous_room = current_room
            current_room = room
            msg += look()
        else:
            msg = "You need a laptop to do that."
    else:
        msg = "You can't access that from where you currently are."


@when('where can i go')
def where_can_i_go():
    ''' Tells a player where they can go based on their current location/Room'''
    if current_room == fridge:
        msg = "You must close fridge."
    else:
        msg = "Where you can go:"
        if current_room == car or current_room == pdx_airport:
            rm_guide = car_pdx_room_guide
        else:
            rm_guide = room_guide
        for room in room_connections[current_room]:
            msg += f"\n{rm_guide[room]}"
    return msg
   
# OTHER: ----------------------------------------------------------------

@when('take ITEM')
def take(item):
    if current_room.is_laptop_room:
        msg = "You cannot pick up items while using laptop."
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
    msg = str(current_room)
    if current_room.people and current_room.list_people:
        for person in current_room.people:
            msg += f"\n{person} is here."
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
        set_context('after1')
        msg = (f"You {action} Byers the half breakfast burrito.\n"
            "Byers: \"Thanks! I feel much better now. Do you need anything? An office chair, laptop, standing desk?\"")
    else:
        msg = (f"{recipient} does not want the {thing}.")
        inventory.add(food)
    return msg

# Ask Byers for chair, laptop, or chair
@when('ask byers for ITEM')
@when('take ITEM from byers')
@when('ask for ITEM from byers')
@when('get ITEM from byers')
def take_item_from_byers(item):
    if current_room.items.find(item):
        msg = take(item)
    elif current_room == luke_byers_cubicle_area:
        byers_obj = byers_items.take(item)
        if byers_obj:
            inventory.add(byers_obj)
            if byers_obj == chair:
                msg = ("Byers proceeds to ask: \"Should it be a rolling chair? What color do you want? Cloth or leather?\""
                    " The two of you discuss this important matter for a while until he eventually gives you a chair.")
            elif byers_obj == laptop:
                msg = "Byers gives you the laptop and informs you that he created GitHub and Slack accounts for you."
                set_context('after2')
            else:
                msg = (f"Byers gives you a {item}.")
        else:
            msg = (f"Byers does not have a {item}.")
    else:
        msg = "You can't do that."
    return msg


# Refactor this later:
# Might make this one also be connected to "interact with ___"
@when('talk to PERSON')
def talk(person):
    character = characters.find(person)
    if person == 'furby':
        msg = ("The furby stares deep into your soul.")
    elif not character: # This case could be used for "interact with"
        msg = ("You can only talk to other humans.")
    elif not current_room.people.find(person):
        msg = (f"{person} cannot hear you.")
    else:
        if character == andrew:
            msg = "Andrew: \"No.\""
        elif character == byers:
            if get_context() == 'after0':
                msg = "Byers mutters something about being too hungry to think..."
            elif get_context() == 'after1':
                msg = "Byers: \"Thanks again for the burrito! Do you need anything?"
                for i in byers_items:
                    msg += (f" A {i}?")
        elif character == graham:
            msg = ("Graham is on the phone with a customer who is furious that Summit isn't working."
                " He is politely asking them to try turning on their computer and they are insisting the"
                " software should do it for them.")
        elif character == wei:
            if get_context() == 'after0' or get_context()=='after0':
                msg = "Wei: \"You should talk to Byers if you need a computer.\""
            else: 
                msg = "She finds 3 new bugs in your code and assigns the issues back to you."
        elif character == luke:
            msg = "Luke is busy talking on the phone."
        else:
            msg = (f"{character.subject_pronoun} is busy right now.")
    return msg


@when('use ITEM on TARGET')
def use(item, target):
    msg = (f"You attempt to use the {item} on the {target}.")
    msg += "\n Nothing happens."
    return msg

@when('hit TARGET with WEAPON')
def hit(target, weapon):
    # check if target is in list or dict of people. If so, they are like "ow why u do dat"
        # also would need to check if those people are in the room...
    msg = (f"You attempt to hit {target} with {weapon}.")
    msg += "\n Nothing happens."
    return msg

@when('scream', action='scream')
@when('shout', action='shout')
@when('yell', action='yell')
def scream(action):
    msg = (f"You {action}: AAAAAAAAAAAAAGGHHHH!!!")
    return msg


# COMMENTED OUT STUFF:

# THESE NEXT 3 COMMANDS NEED TO BE EDITED. For example, what if they try to use the axe on a waterfall?
# @when('give THING to RECIPIENT')
# def give(thing, recipient):
#     obj = inventory.take(thing)
#     character = characters.find(recipient)
#     if not obj:
#         msg = (f"You do not have a {thing}.")
#     elif not character:
#         msg = (f"You can only give things to people.")
#     elif not current_room.people.find(recipient):
#         msg = (f"{recipient} is not here.")
#     else:
#         msg = (f"You give the {obj} to the {recipient}.")
#     return msg


# @when('cast', context='magical_area', magic=None)
# @when('cast MAGIC', context='magical_area')
# def cast(magic):
#     if magic == None:
#         msg = "Which magic you would like to spell?"
#     elif magic == 'soup':
#         msg = "A large bowl of potato soup appears in front of you!"
#     return msg

# @when('north', direction='north')
# @when('south', direction='south')
# @when('east', direction='east')
# @when('west', direction='west')
# def go(direction):
#     global current_room
#     room = current_room.exit(direction)
#     if room:
#         current_room = room
#         msg = 'You go '+ direction +'.'
#         msg += '\n' + look()
#         if room == forest_edge:
#             set_context('magical_area')
#         else:
#             set_context('default')
#     else:
#         msg = 'You cannot go '+ direction + '.'
#     return msg

# @when('test')
# def test_something():
#     msg = temp.items.find('temp two item')
#     return msg


# if ((room.only_accessible_from_soa and current_room != shared_office_area) # room only accessible from soa and player not in soa
#         or (room == xhq_outside and (current_room != car and current_room != shared_office_area))): # can only access xhq_outside from soa or car
#         msg = 'You cannot access that from where you currently are.'
#     else:
#         current_room = room
#         msg = 'You '+ room_entry[e_key] +'.\n'
#         msg += look()
#     return msg

 # if current_room == shared_office_area:
    #     msg += (
    #         "LB - Luke and Byers cubicle area\n"
    #         "DR - Demo room\n"
    #         "CR - Conference room\n"
    #         "ZM - Zoe and Madden's office\n"
    #         "WS - Workshop\n"
    #         "Exit Xtract HQ - Go outside."
    #     )
    # # elif current_room == laptop or :
    # elif current_room == fridge: #or current_room == laptop:
    #     msg += f"Close {current_room} first."
    # elif current_room.only_accessible_from_soa:
    #     msg += "SOA - Shared office area"
    # else:
    #     msg += "UNKNOWN."
    # return msg