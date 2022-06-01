import unittest
from mod_adventurelib import *
from game import *

TEST_USER_ID = "BroccoliCheddarSoup"


class TestGame(unittest.TestCase):

    def test_game_initialization(self):
        """Test creating a player and starting the game"""
        p, res = self.create_player(TEST_USER_ID)
        self.check_response_text("You enter Xtract HQ. Luke has everyone gathered for an", res, 'start adventure')
        self.assertIsNotNone(p, "Player is None.")
        self.assertEqual(p.current_room, shared_office_area,
            f"Player starting room should be shared office area, instead, found: {p.current_room}")


    def create_multiple_users(self):
        """Make multiple users and return an array of the player objects"""
        players = []
        for u_id in ["abcdefghijklmnop", "qwertyuiop", "123456789qwertyuiop", TEST_USER_ID]:
            p, res = self.create_player(u_id)
            players.append(p)
        return players


    def test_multiple_users_creation(self):
        """Test to make sure multiple players can be created."""
        players = self.create_multiple_users()
        for p in players:
            u_id = p.get_user_id()
            self.assertIn(u_id, current_players, f"User with user id \"{u_id}\" not found in players.")


    def test_multiple_users_playing(self):
        """Test creating multiple users and running commands for them. Ensure that things don't get mixed up between them."""
        players = self.create_multiple_users()
        handle_command("zm", players[0])
        handle_command("open fridge", players[1])
        handle_command("take burrito", players[1])
        self.get_to_level(5, players[2])
        for cmd in ["dr", "join call", "yes"]:
            handle_command(cmd, players[3])
        self.check_room(players[0].current_room, zoe_madden_office, "zoe madden office")
        self.check_room(players[1].current_room, fridge, "fridge")
        self.check_room(players[3].current_room, demo_room, "demo room")
        self.assertTrue(burrito in players[1].inventory, "Player 2 inventory should contain burrito but it does not.")
        self.assertFalse(burrito in players[0].inventory, "Player 1 inventory contains breakfast burrito when player 2 took it.")
        self.check_level(5, players[2])
        self.check_level(0, players[0])
        self.check_sale_rooms(1, players[3])
        self.check_sale_rooms(2, players[1])


    def test_player_deletion(self):
        """Test deleting a player and then creating them again"""
        p, res = self.create_player(TEST_USER_ID)
        p2, res = self.create_player("qwertyuiop")
        self.get_to_level(4, p2)
        current_players.pop(p.get_user_id())
        del p
        self.assertNotIn(TEST_USER_ID, current_players, f"Player was not removed from current_players like they should have been.")
        with self.assertRaises(UnboundLocalError): # Make sure p object was deleted
            p.get_event_level()
        self.check_level(4, p2) # Make sure that deleting one player didn't mess with the other player.
        p, res = self.create_player(TEST_USER_ID) # create original player again
        self.check_level(0, p) # Make sure player is working fine


    def test_fridge_functionality(self):
        """Test to make sure fridge in XHQ works properly."""
        p, res = self.create_player(TEST_USER_ID)

        res = handle_command("open fridge", p)
        self.check_room(p.current_room, fridge, "fridge")
        for item in ["burrito", "ranch"]:
            self.assertIn(item, res, f"{item} not in fridge room description")
            self.assertTrue(item in p.get_room_items(p.current_room), f"{item} not in fridge room items")

        cmd = "close fridge"
        res = handle_command(cmd, p)
        self.check_room(p.current_room, shared_office_area, "shared office area")
        self.check_response_text("You close the fridge", res, cmd)


    def test_take_and_drop(self):
        """Test to make sure items can be taken, dropped, and picked up again."""
        p, res = self.create_player(TEST_USER_ID)

        handle_command("open fridge", p)
        for item in ["burrito", "ranch"]:
            res = handle_command(f"take {item}", p)
            self.assertIn("You pick up the", res, f"Unexpected response after picking up the {item}: {res}")
            self.assertTrue(item in p.inventory, f"Failed to take {item} - not in player inventory.")
            self.assertFalse(item in p.get_room_items(p.current_room), f"{item} still in fridge after taking it.")
        handle_command("close fridge", p)

        item = "burrito"
        res = handle_command(f"drop {item}", p)
        self.assertFalse(item in p.inventory, f"Failed to drop {item}. Still in player inventory. Response: {res}")
        self.assertTrue(item in p.get_room_items(p.current_room), f"Failed to drop {item}. NOT in room bag.")
        
        cmd = "dr"
        res = handle_command(cmd, p)
        self.assertNotIn(item, res, f"{item} is listed in room description of room it was NOT dropped in.")
        self.assertFalse(item in p.get_room_items(p.current_room), f"{item} in room bag of room it was NOT dropped in.")

        cmd = "take burrito"
        res = handle_command(cmd, p)
        self.assertFalse(item in p.inventory, f"{item} was able to be picked up from room it was NOT in.")
        self.assertNotIn("You pick up the", res, f"Told user item was picked up when it was actually NOT taken.")

        cmd = "soa"
        res = handle_command(cmd, p)
        self.assertIn(item, res, f"{item} was NOT listed in room description of room it was dropped in.")
        self.assertTrue(item in p.get_room_items(p.current_room), f"{item} NOT in room bag of room it was dropped in.")

        cmd = "take burrito"
        res = handle_command(cmd, p)
        self.assertIn("You pick up the", res, f"Unexpected response after picking up the {item}: {res}")
        self.assertTrue(item in p.inventory, f"Failed to take {item} - not in player inventory.")


    def test_help_commands(self):
        """Tests help, hint, objective, and tips commands."""
        p, res = self.create_player(TEST_USER_ID)
        cmd = "help"
        res = handle_command(cmd, p)
        self.check_response_text(help_cmds[0], res, cmd)
        self.check_response_text("Guide to some of the main commands", res, cmd)
        cmd = "objective"
        res = handle_command(cmd, p)
        self.check_response_text(objectives[0], res, cmd)
        cmd = "hint"
        res = handle_command(cmd, p)
        self.check_response_text(hints[0], res, cmd)
        cmd = "tips"
        res = handle_command(cmd, p)
        self.check_response_text(tips, res, cmd)

    def test_losing_game(self):
        """Makes sure that losing both sales causes user to enter 'game_over' context."""
        p, res = self.create_player(TEST_USER_ID)
        for cmd in ["dr", "join call", "yes", "soa", "car", "pdx", "ts", "xb", "talk to potential client", "yes"]:
            handle_command(cmd, p)
        self.assertEqual(p.get_context(), 'game_over', "Context should be 'game_over' but it is not.")


    def level_0_to_1(self, p):
        """Get player p from level 0 to level 1 by running several commands."""
        for cmd in ["open fridge", "take burrito", "close fridge", "lb", "feed burrito to byers"]:
            handle_command(cmd, p)

    def level_1_to_2(self, p):
        """Get player p from level 1 to level 2 by running several commands."""
        handle_command("ask for laptop", p)

    def level_2_to_3(self, p):
        """Get player p from level 2 to level 3 by running several commands."""
        for cmd in ["soa", "car", "bc", "bci", "talk to nurse"]:
            handle_command(cmd, p)

    def level_3_to_4(self, p):
        """Get player p from level 3 to level 4 by running several commands."""
        for cmd in ["open laptop", "open github", "create a new issue", "issue more information smaller space"]:
            handle_command(cmd, p)

    def level_4_to_5(self, p):
        """Get player p from level 4 to level 5 by running several commands."""
        for cmd in ["close laptop", "bcl", "car", "pdx", "ts", "xb", "talk to potential client", "yes"]:
            handle_command(cmd, p)

    def level_5_to_6(self, p):
        """Get player p from level 5 to level 6 by running several commands."""
        for cmd in ["mch", "pdx", "wy", "wyb", "wys", "interact with terminal", "install teamviewer"]:
            handle_command(cmd, p)

    def level_6_to_7(self, p):
        """Get player p from level 6 to level 7 by running several commands."""
        for cmd in ["wyb", "wyl", "pdx", "car", "xhq"]:
            handle_command(cmd, p)


    def get_to_level(self, level, p):
        """Quickly get to a specific level so a test can be done starting at that point in the game."""
        if p.get_event_level() > 0 or p.current_room != shared_office_area:
            raise Exception("Invalid use of get_to_level() function. Must start at level 0 in shared office area.")
        self.level_0_to_1(p)
        if level == 1:
            return
        self.level_1_to_2(p)
        if level == 2:
            return
        self.level_2_to_3(p)
        if level == 3:
            return
        self.level_3_to_4(p)
        if level == 4:
            return
        self.level_4_to_5(p)
        if level == 5:
            return
        self.level_5_to_6(p)
        if level == 6:
            return
        self.level_6_to_7(p)
        if level == 7:
            return


    def test_play_through(self):
        """Tests play through of game to ensure it can be played all the way to the end and player can win."""
        # Create player and initialize game start
        p, res = self.create_player(TEST_USER_ID)
        self.level_0_to_1(p)
        self.check_level(1, p)
        self.level_1_to_2(p)
        self.check_level(2, p)
        self.level_2_to_3(p)
        self.check_level(3, p)
        self.level_3_to_4(p)
        self.check_level(4, p)
        self.level_4_to_5(p)
        self.check_level(5, p)
        self.level_5_to_6(p)
        self.check_level(6, p)
        self.level_6_to_7(p)
        self.check_level(7, p)
        
        # self.check_room(p.current_room, luke_byers_cubicle_area, "luke byers cubicle area")

    def test_unrecognized_command(self):
        """Make sure that unrecognized commands are handled as expected."""
        p, res = self.create_player(TEST_USER_ID)
        cmd = "invalid meow"
        res = handle_command(cmd, p)
        self.assertIn("I don't understand ", res, f"Unrecognized command was not handled properly. Expected: \"I don't understand '{cmd}'\" But instead, got: \"{res}\"")
        

    def test_invalid_interactions(self):
        """Make sure that invalid interaction commands are handled as expected."""
        p, res = self.create_player(TEST_USER_ID)
        for thing in ["lights", "some cookie dough", "$@%&$*$#&(# %^&^%"]:
            cmd = f"interact with {thing}"
            res = handle_command(cmd, p)
            self.assertIn(f"You cannot interact with {thing}", res, f"Invalid interaction was not handled properly. Expected: \"You cannot interact with {thing}.\" But instead, got: \"{res}\"")


    def test_laptop(self):
        """Make sure that laptop functionality all works as expected."""
        p, res = self.create_player(TEST_USER_ID)
        self.get_to_level(2, p)
        self.assertTrue("laptop" in p.inventory, "Laptop is not in inventory after getting it from Byers.")
        room_before_laptop = p.current_room

        cmd = "open laptop"
        res = handle_command(cmd, p)
        self.check_response_text(room_entry.get("open_laptop"), res, cmd)
        self.check_room(p.current_room, laptop, "laptop")

        res = handle_command("github", p)
        self.check_room(p.current_room, github, "github")

        res = handle_command("open slack", p)
        self.check_room(p.current_room, slack, "slack")

        cmd = "close github"
        res = handle_command(cmd, p)
        self.check_room(p.current_room, slack, "slack") # because GitHub cannot be closed when it is not open.
        self.check_response_text("GitHub is not open right now", res, cmd)

        cmd = "check notifications"
        res = handle_command(cmd, p)
        self.check_response_text(slack.notifications[p.get_event_level()], res, cmd)

        res = handle_command("open github", p)
        self.check_room(p.current_room, github, "github")

        res = handle_command("create a new issue", p)
        self.assertEqual(p.get_context(), "creating_issue")

        res = handle_command("issue blah", p)
        self.assertNotEqual(p.get_event_level(), 4, f"Player was able to successfully create an issue with an INVALID issue name.")

        res = handle_command("check notifications", p)
        self.assertNotIn(slack.notifications[p.get_event_level()], res, "Notifications should not be able to be checked when not in Slack.")

        cmd = "where can i go"
        res = handle_command(cmd, p)
        self.check_response_text("close laptop", res.lower(), cmd)

        cmd = "close laptop"
        res = handle_command(cmd, p)
        self.check_room(p.current_room, room_before_laptop, "previous room before opening laptop")
        self.check_response_text(room_entry.get("close_laptop"), res, cmd)


    def check_room(self, curr_room, entered_room, room_title):
        """Check that current room is equal to entered room."""
        self.assertEqual(curr_room, entered_room, f"Failed to enter {room_title}. Current room description: {curr_room}")


    def check_response_text(self, text_to_find, res, cmd):
        """Check that the response message contains text_to_find in it."""
        self.assertIn(text_to_find, res, f"Command '{cmd}' returned an incorrect response. Could not find \"{text_to_find}\" in response. Response: \"{res}\"")

    def check_level(self, level, p):
        """Check that the player is at the expected level."""
        self.assertEqual(p.get_event_level(), level, f"Player should be at level {level} but instead is at level {p.get_event_level()}.")

    def check_sale_rooms(self, should_have, p):
        """Check that the number of sale rooms for a player is equal to the expected number (should_have)."""
        rooms_left = len(p.sale_rooms)
        self.assertEqual(rooms_left, should_have, f"User {p.get_user_id()} should have {should_have} sale rooms left but instead they have {rooms_left}.")

    def create_player(self, u_id):
        """Begins the game and creates a player"""
        player = current_players.get(u_id)
        if player: # If player ID already exists (it shouldn't...)
            current_players.pop(u_id)
            del player
        res = start_adventure(u_id)
        p = current_players.get(u_id)
        return p, res



if __name__ == '__main__':
    unittest.main()
