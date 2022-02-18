from mod_adventurelib import *


# ROOMS --------------------------------------------

# Rooms:
starting_room = Room("""You are in a dark room.""")
valley = Room("""You are in a beautiful valley.""")
magic_forest = Room("""You are in a enchanted forest where magic grows wildly.""")

# Connections:
starting_room.north = valley
valley.north = magic_forest

# Initialize current room:
current_room = starting_room


# ITEMS ---------------------------------------------

# Configure bags:
Room.items = Bag()
inventory = Bag()

# Items:
mallet = Item('rusty mallet', 'mallet')

# Item locations:
valley.items = Bag({mallet,})


# COMMANDS ------------------------------------------
# class Player:
# def __init__(self, channel):
#     self.channel = channel

#     self.current_room = 
#     self.inventory = Bag()
#     self.


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
        if room == magic_forest:
            set_context('magic_aura')
        else:
            set_context('default')
        return msg


@when('take ITEM')
def take(item):
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
    msg = 'You have:' # Note: add a check to see if this is empty and return a different message if so.
    for thing in inventory:
        msg += '\n' + str(thing)
    return msg

@when('cast', context='magic_aura', magic=None)
@when('cast MAGIC', context='magic_aura')
def cast(magic):
    if magic == None:
        msg = "Which magic you would like to spell?"
    elif magic == 'fireball':
        msg = "A flaming Fireball shoots form your hands!"
    return msg



# look()
# start()
