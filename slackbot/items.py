from mod_adventurelib import *
from rooms import *

# Configure bags: ------
Room.items = Bag()
inventory = Bag()

# Items: ------
mug = Item('mug') # mug of instant oatmeal in CR
ranch = Item('bottle of ranch', 'ranch') # from fridge - can feed to Luke
burrito = Item('half eaten breakfast burrito', 'breakfast burrito', 'burrito', 'half eaten burrito') # from fridge - gotta feed to Byers
vials = Item('patient vials', 'vials')

# Items from Byers:
chair = Item('chair')
laptop_item = Item('laptop') 
standing_desk = Item('standing desk', 'desk')
byers_items = Bag({chair, laptop_item, standing_desk})

# Item locations: ------
fridge.items = Bag({ranch, burrito,})
bc_mixing_area.items = Bag({vials})

shared_office_area.items = Bag({})
conference_room.items = Bag({})
demo_room.items = Bag({})
luke_byers_cubicle_area.items = Bag({})
zoe_madden_office.items = Bag({})

car.items = Bag({})
pdx_airport.items = Bag({})

wy_lobby.items = Bag({})
wy_back_office_area.items = Bag({})
wy_server_room.items = Bag({})
wy_injection_area.items = Bag({})

bc_lobby.items = Bag({})
bc_injection_area.items = Bag({})
bc_front_desk.items = Bag({})

ts_main_area.items = Bag({})
xtract_booth.items = Bag({})
rosch_booth.items = Bag({})
cerner_booth.items = Bag({})
