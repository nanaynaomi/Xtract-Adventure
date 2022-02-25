# LATER THIS WILL BE SPLIT UP INTO DIFFERENT FILES:
# from rooms import *
# from items import *
# from commands import *
# from start import *

from mod_adventurelib import *

# ROOMS ---------------------------------------------

# Rooms:
starting_room = Room("""You are in a dusty log cabin.""")
forest = Room("""You are in a forest. A river can be heard in the distance.""")
forest_edge = Room("""You are at the edge of a forest, overlooking a waterfall.""")

# Connections: (draw a map later)
starting_room.north = forest
forest.north = forest_edge

# Initialize current room:
current_room = starting_room


# ITEMS ---------------------------------------------

# Configure bags:
Room.items = Bag()
inventory = Bag()

# Items:
axe = Item('rusty axe', 'axe')

# Item locations:
forest.items = Bag({axe,})


# COMMANDS ------------------------------------------

@when('north', direction='north')
@when('south', direction='south')
@when('east', direction='east')
@when('west', direction='west')
def go(direction):
    global current_room
    room = current_room.exit(direction)
    if room:
        current_room = room
        msg = 'You go '+ direction +'.'
        msg += '\n' + look()
        if room == forest_edge:
            set_context('magical_area')
        else:
            set_context('default')
        return msg
    else:
        msg = 'You cannot go '+ direction + '.'
        return msg


@when('take ITEM')
def take(item):
    # HEY! There will be cases when there are items we don't want the user to pick up (such as characters) 
    # perhaps I can add a property to the item class that says whether or not it can be picked up.
    obj = current_room.items.take(item)
    if obj:
        inventory.add(obj)
        msg = ('You pick up the %s.' % obj)
    else:
        msg = ('There is no %s here.' % item)
    return msg


@when('drop THING')
def drop( thing):
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

@when('cast', context='magical_area', magic=None)
@when('cast MAGIC', context='magical_area')
def cast(magic):
    if magic == None:
        msg = "Which magic you would like to spell?"
    elif magic == 'soup':
        msg = "A large bowl of potato soup appears in front of you!"
    return msg

@when('scream', action='scream')
@when('shout', action='shout')
@when('yell', action='yell')
def scream(action):
    msg = (f"You {action}: AAAAAAAAAAAAAGGHHHH!!!")
    return msg

# THESE NEXT 3 COMMANDS NEED TO BE EDITED. For example, what if they try to use the axe on a waterfall?
@when('give ITEM to RECIPIENT')
def give(item, recipient):
    msg = (f"You give the {item} to the {recipient}.")
    msg += "\n Nothing happens."
    return msg

@when('use ITEM on TARGET')
def use(item, target):
    msg = (f"You attempt to use the {item} on the {target}.")
    msg += "\n Nothing happens."
    return msg

@when('hit TARGET with WEAPON')
def hit(target, weapon):
    msg = (f"You attempt to hit {target} with {weapon}.")
    msg += "\n Nothing happens."
    return msg


