from mod_adventurelib import *
from rooms import *

# Configure bags: ----
Room.items = Bag()
Room.people = Bag()
inventory = Bag()

# Characters: ----
andrew = MaleCharacter('andrew')
byers = MaleCharacter('byers')

graham = MaleCharacter('graham')
james = MaleCharacter('james')
luke = MaleCharacter('luke')
martin = MaleCharacter('martin')
scott = MaleCharacter('scott')
steve = MaleCharacter('steve')
stephanie = FemaleCharacter('stephanie')
madden = FemaleCharacter('madden')
wei = FemaleCharacter('wei')
zoe = FemaleCharacter('zoe')

customer = MaleCharacter('the customer')
nurse = FemaleCharacter('the nurse')

characters = Bag({andrew, byers, graham, james, luke, martin, scott, steve, stephanie, madden, wei, zoe, customer, nurse, })

# Items: ----
axe = Item('rusty axe', 'axe')
mug = Item('mug') # mug of instant oatmeal in CR
ranch = Item('bottle of ranch', 'ranch') # from fridge - can feed to Luke
burrito = Item('half eaten breakfast burrito', 'breakfast burrito', 'burrito', 'half eaten burrito') # from fridge - gotta feed to Byers
# temp = Item('temp item')
# temp_two = Item('temp two item')

# Items from Byers:
chair = Item('chair')
laptop = Item('laptop') # "If when you take the laptop he could mention having created github and slack accounts for you as a bit of a clue..."
standing_desk = Item('standing desk', 'desk')
byers_items = Bag({chair, laptop, standing_desk})

# Item locations: ----
#forest.items = Bag({axe,})
conference_room.items = Bag({mug,})
fridge.items = Bag({ranch, burrito,})

# Initial character locations: ---
shared_office_area.people = Bag({andrew, graham, martin, wei})
luke_byers_cubicle_area.people = Bag({byers, luke})
zoe_madden_office.people = Bag({zoe})
# mixing_area.people = Bag({nurse})
# injection_area.people = Bag({nurse})
# If they are on a video call, temporarily move them to that room and then remove them again after the call...

# Items you might see but cannot take: ----
# Work on this later (non-essential)
