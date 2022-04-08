from mod_adventurelib import *
from rooms import *

# Configure bags: ------
Room.items = Bag()
Room.people = Bag()
inventory = Bag()

# Characters: ------
andrew = MaleCharacter('andrew')
byers = MaleCharacter('byers')

graham = MaleCharacter('graham')
james = MaleCharacter('james')
luke = MaleCharacter('luke')
martin = MaleCharacter('martin')
madden = FemaleCharacter('madden')
scott = MaleCharacter('scott')
steve = MaleCharacter('steve')
stephanie = FemaleCharacter('stephanie')
wei = FemaleCharacter('wei')
zoe = FemaleCharacter('zoe')

nurse = NonSpecificCharacter('nurse')
doctor = NonSpecificCharacter('doctor')
it_guy = MaleCharacter('it guy')
potential_client = NonSpecificCharacter('potential client')
patient = NonSpecificCharacter('patient')

characters = Bag({andrew, byers, graham, james, luke, martin, scott, steve, stephanie, madden, wei, zoe, nurse, doctor, it_guy, potential_client, patient})

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

# Initial character locations: ------

shared_office_area.people = Bag({andrew, graham, martin, wei})
luke_byers_cubicle_area.people = Bag({byers, luke})
zoe_madden_office.people = Bag({zoe})

wy_lobby.people = Bag({patient})
wy_back_office_area.people = Bag({madden, doctor, nurse})
wy_server_room.people = Bag({it_guy})
wy_injection_area.people = Bag({stephanie, nurse})

bc_lobby.people = Bag({patient})
bc_injection_area.people = Bag({nurse, patient})
bc_mixing_area.people = Bag({nurse})

xtract_booth.people = Bag({james, madden, scott, potential_client})
