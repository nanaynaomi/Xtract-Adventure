from mod_adventurelib import *
from rooms import *

# Configure bag: ------
Room.people = Bag()

# Characters: ------
andrew = Character('andrew')
byers = Character('byers')
graham = Character('graham')
james = Character('james')
luke = Character('luke')
martin = Character('martin')
madden = Character('madden')
scott = Character('scott')
stephanie = Character('stephanie')
wei = Character('wei')
zoe = Character('zoe')

nurse = Character('nurse', 'the nurse', 'nurses', 'the nurses', 'a nurse')
doctor = Character('doctor', 'the doctor')
it_guy = Character('it guy', 'the it guy')
potential_client = Character('potential client', 'the potential client', 'a potential client', 'client', 'perspective client')
patient = Character('patient', 'patients', 'the patient', 'a patient')

characters = Bag({andrew, byers, graham, james, luke, martin, scott, stephanie, madden, wei, zoe, nurse, doctor, it_guy, potential_client, patient})


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


# Character messages: -------
all_levels = [lvl for lvl in range(8)]

andrew.set_msg(shared_office_area, all_levels, "Andrew: \"No\"")

byers.set_msg(luke_byers_cubicle_area, [0], "Byers mutters something about being too hungry to think...")
byers.set_msg(luke_byers_cubicle_area, [1,2,3,4, 6,7], "Byers is working on a security questionnaire.")
byers.set_msg(luke_byers_cubicle_area, [5], "Byers mentions that he cannot contact your customer's server.")

graham.set_msg(shared_office_area, all_levels, "Graham is on the phone with a customer who is furious that Summit isn't working."
    " He is politely asking them to try turning on their computer and they are insisting the software should do it for them.")

james.set_msg(xtract_booth, [0,1,2,3], "You hear James making his pitch... \"pain funnel... 3rd party story... pain funnel...\" then you hear James ask,"
    " \"So what's stopping you from signing today?\" to which the potential customer responds:"
    " \"Well... our reports absolutely must have red lines with transparent ink and I don't see where Summit supports that.\""
    " You think to yourself, that sounds like an absolutely horrible idea.")
james.set_msg(xtract_booth, [4,5,6,7], "You hear James making his pitch... \"pain funnel... 3rd party story... pain funnel...\"")

luke.set_msg(luke_byers_cubicle_area, [0,1,4,5,6], "Luke is busy talking on the phone.")
luke.set_msg(luke_byers_cubicle_area, [2,3], "Between calls, you ask Luke about what kind of Git issues you should create. He suggests that you talk to customers"
    " and see if anyone has ideas for things that they want Summit to have.")
luke.set_msg(luke_byers_cubicle_area, [7], "Luke: \"It's going to take more than a dragon to stop me from doing all the things!\"")

martin.set_msg(shared_office_area, all_levels, "Martin: \"Sigh... Skintest protocol or report template?\"")

madden.set_msg(xtract_booth, all_levels, "Scott is listening while Madden is waving her arms wildly and seems to be explaining an idea to Scott." 
    " She keeps pointing at a large visual aid she has created which has a 3 step plan on it. Phase 1 is \"collect all the allergy information\"." 
    " Phase 3 \"Profit\" but Phase 2 is only a large question mark.")
madden.set_msg(wy_back_office_area, all_levels, "Madden is busy right now.") # CHANGE LATER

scott.set_msg(xtract_booth, all_levels, "Scott is nodding thoughtfully and listening to Madden's plan.")

stephanie.set_msg(wy_injection_area, all_levels, "Stephanie is busy right now.") # CHANGE LATER

wei.set_msg(shared_office_area, [0,1], "Wei: \"You should talk to Byers if you need a computer.\"")
wei.set_msg(shared_office_area, [2,3,4,5,6,7], "She finds 3 new bugs in your code and assigns the issues back to you.")

zoe.set_msg(zoe_madden_office, [0,1,3,4], "She tells you that we need a new customer.") # POSSIBLY CHANGE LATER TO HINT BETTER
zoe.set_msg(zoe_madden_office, [2], "She suggests that you go talk to some customers and see what changes they would like to see in Summit.")
zoe.set_msg(zoe_madden_office, [5,6,7], "She is busy working on the security questionnaire for the new customer. She mentions something about being on question 3 of 2739.")

nurse.set_msg(wy_back_office_area, [5], "Nurse: \"We can't treat patients - can someone fix this?\"")
nurse.set_msg(wy_back_office_area, [6,7], "Nurse: \"Summit is super cool! My favorite feature is definitely the cat videos section.\"")
nurse.set_msg(wy_injection_area, [5], "Nurse: \"Why isn't it working? I was really looking forward to learning how to use Summit.\"")
nurse.set_msg(wy_injection_area, [6,7], "Nurse: \"I like my job much more now that we have Summit.\"")
nurse.set_msg(bc_injection_area, [0,1,2,3], "Nurse: \"I have a suggestion: Could you have Summit show more information in a smaller space?\"")
nurse.set_msg(bc_injection_area, [4,5,6,7], "Nurse: \"Gee I sure love giving people injections.\"")
nurse.set_msg(bc_mixing_area, [0,1,2,3], "Nurse: \"Hey, you should add cat videos to Summit. That would be really useful I think.\"")
nurse.set_msg(bc_mixing_area, [4,5,6,7], "Nurse: \"I like cookies.\"") # Change later? lol

doctor.set_msg(wy_back_office_area, [5], "The doctor is busy complaining")
doctor.set_msg(wy_back_office_area, [6,7], "The doctor is singing and dancing with joy")

it_guy.set_msg(wy_server_room, [5], "Is it working yet?! This is unacceptable... you need to fix this now!")
it_guy.set_msg(wy_server_room, [6,7], "He mutters something about his game of solitaire freezing and reboots the server.")

potential_client.set_msg(xtract_booth, all_levels, "You start chatting with the potential client.")

patient.set_msg(wy_lobby, [5], "Patient: \"What is taking so long? This is worse than the DMV!\"")
patient.set_msg(wy_lobby, [6,7], "Before you can say anything, the patient you were about to talk to gets called in for their appointment. Things are moving so efficiently around here, it's scary!!")
patient.set_msg(bc_lobby, all_levels, "Patient: \"Can you help me?! I put my finger on the screen and it wont read my fingerprint!\"")
patient.set_msg(bc_injection_area, all_levels, "Patient: \"1 down, 5000 injections to go!\"")
