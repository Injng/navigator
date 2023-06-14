import os
import sys
from time import sleep
from initialize import *

# Clear the terminal
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# Function to print a dividwer
def divide():
    print("------------------------------")

# Function to detect illegal integer input
def detint(x, valid=[], limit=100):
    if valid != []:
        try:
            if int(x) not in valid:
                return -1
            else:
                return int(x)
        except:
            return -1
    try:
        if int(x) > limit:
            return -1
        else:
            return int(x)
    # If the choice is not an integer return -1 to signal error
    except:
        return -1


# Class to create a Sign object within a room
# name : a multi-line string that describes the sign
class Sign:
    def __init__(self, name):
        self.name = name
        self.holdable = False

    def print_object(self):
        print(self.name)

    def return_type(self):
        return "sign"

# Class to create a Weapon object within a room
# name : a descriptor of the weapon
class Weapon:
    def __init__(self, name):
        self.name = name
        self.holdable = True

    def print_object(self):
        print(self.name)

    def return_type(self):
        return "weapon"


# Class to create a room
# name : string, describes the name of the room
# position : tuple, uses coordinates to describe the position of the room on a map
# diagram : 2D list, shows adjacent rooms using a map
# classifier : integer, classifies room into entrance (1), corridor (2), check (3), platform (4), or street (5)
# objects : a list of objects, usually with their classes
# identifier : a unique integer that identifies the room
# connect : [connect, [diagram], [position]] ; used for connecting to other levels
# connect<connect> : integer, denotes whether the room connects to other structures, (0) none, (1) up, (-1) down, (2) both, (3) n/e/s/w
# diagram<connect> : if connect<connect> is not 0, this links to the diagram(s) for the connections; use "" for empty diagram for (3)
# position<connect> : if connect<connect> is not 0, this shows the position as tuple for the connections; use "" for empty position for (3)
class Room:
    def __init__(self, name, position, diagram, classifier, objects, identifier, connect=[0]):
        self.name = name
        self.position = position
        self.diagram = diagram
        self.classifier = classifier
        self.objects = objects
        self.identifier = identifier
        self.connect = connect

        # Remember adjacent rooms in order N, E, S, W, U, D
        self.n = diagram[position[0] - 1][position[1]]
        self.e = diagram[position[0]][position[1] + 1]
        self.s = diagram[position[0] + 1][position[1]]
        self.w = diagram[position[0]][position[1] - 1]
        # Connect to other structures
        if connect[0] != 0:
            other_position = connect[2]
        if connect[0] == 1:
            self.u = connect[1][0][other_position[0][0]][other_position[0][1]]
            self.d = False
        elif connect[0] == -1:
            self.u = False
            self.d = connect[1][0][other_position[0][0]][other_position[0][1]]
        elif connect[0] == 2:
            self.u = connect[1][0][other_position[0][0]][other_position[0][1]]
            self.d = connect[1][1][other_position[1][0]][other_position[1][1]]
        elif connect[0] == 3:
            if connect[1][0] != "":
                self.n = connect[1][0][other_position[0][0]][other_position[0][1]]
            if connect[1][1] != "":
                self.e = connect[1][1][other_position[1][0]][other_position[1][1]]
            if connect[1][2] != "":
                self.s = connect[1][2][other_position[2][0]][other_position[2][1]]
            if connect[1][3] != "":
                self.w = connect[1][3][other_position[3][0]][other_position[3][1]]
            self.u = False
            self.d = False
        else:
            self.u = False
            self.d = False
        self.adjacent = [self.n, self.e, self.s, self.w, self.u, self.d]

    # function to return adjacent rooms
    def return_adjacent(self):
        rooms = []
        for i in self.adjacent:
            if type(i) == bool:
                rooms.append("False")
            else:
                rooms.append(str(hex(i)[1:]))
        return rooms
    
    # function to set adjacent room types
    def set_adjacent(self, types):
        self.adjacent_types = types

    # function to initialize room to user
    def print_room(self):
        # Check to see if discovered, if not, don't print name
        if room_dict[self.identifier][0]:
            print(self.name)
        else:
            print("Unknown")
            room_dict[self.identifier][0] = True
        divide()
        # Show the types of adjacent rooms to the player
        for i in self.adjacent_types:
            print(f"To the {i[0]} there is a {i[1]}")
        # Initialize rooms
        if self.classifier == 1:
            return self.init_entrance()
        elif self.classifier == 2:
            return self.init_corridor()
        elif self.classifier == 3:
            return self.init_security()
        elif self.classifier == 4:
            return self.init_platform()
        elif self.classifier == 5:
            return self.init_street()

    # function to show objects in a room to user
    def show_objects(self):
        for i in self.objects:
            print(f"There is a {i.return_type()} here:")
            i.print_object()
            print(" ")

    # function to show choices to user
    def show_choices(self):
        # list to keep track of valid choices
        valid_choices = []
        
        if self.n != False:
            print("(1) Go north")
            valid_choices.append(1)
        if self.e != False:
            print("(2) Go east")
            valid_choices.append(2)
        if self.s != False:
            print("(3) Go south")
            valid_choices.append(3)
        if self.w != False:
            print("(4) Go west")
            valid_choices.append(4)
        if self.u != False:
            print("(5) Go up")
            valid_choices.append(5)
        if self.d != False:
            print("(6) Go down")
            valid_choices.append(6)
        print("(7) Look/Wait")
        valid_choices.append(7)

        # if this is a platform, give option to board
        index = 8
        vehicles = []
        if self.classifier == 4:
            station_id = room_dict[self.identifier][1][0]
            for i in station_dict[station_id][2]:
                if i[5]:
                    print(f"({index}) Board {i[1]} towards {i[3]}")
                    valid_choices.append(index)
                    # Build list of Train objects that are serving the platform
                    for j in train_dict[(i[0], i[2], i[4])]:
                        if j.return_location() == station_id:
                            vehicles.append(j)
                    index += 1

        # Allow user to pick up items
        for x in range(len(self.objects)):
            if self.objects[x].holdable == True:
                print(f"({index + x}) Acquire {self.objects[x].return_type()}:", end=" ")
                self.objects[x].print_object()
                valid_choices.append(index + x)
            else:
                pass

        while True:
            choice = detint(input("Your choice: "), valid=valid_choices)
            if choice == -1:
                print("Invalid choice")
            else:
                if self.classifier == 4:
                    return [choice, index, vehicles]
                else:
                    return [choice, 8, []]

    # function to return the next room location for the player to main
    def return_next(self, choice, index, boarding=[]):
        # Add items to inventory
        if choice >= index:
            inventory.append(self.objects[choice - 6])
            return str(hex(self.identifier)[1:])
        elif choice == 1:
            print(str(hex(self.n)[1:]))
            return str(hex(self.n)[1:])
        elif choice == 2:
            return str(hex(self.e)[1:])
        elif choice == 3:
            return str(hex(self.s)[1:])
        elif choice == 4:
            return str(hex(self.w)[1:])
        elif choice == 5:
            return str(hex(self.u)[1:])
        elif choice == 6:
            return str(hex(self.d)[1:])
        elif choice == 7:
            return str(hex(self.identifier)[1:])
        elif boarding != []:
            return boarding[choice - 8]
            
    # function to initialize entrance room
    def init_entrance(self):
        print("This is an entrance to a metro station.")
        print(" ")
        self.show_objects()
        choice = self.show_choices()
        return self.return_next(choice[0], choice[1])

    # function to initialize a corridor
    def init_corridor(self):
        print("This is a corridor.")
        print(" ")
        self.show_objects()
        choice = self.show_choices()
        return self.return_next(choice[0], choice[1])

    # function to initialize a street
    def init_street(self):
        print("You are on a street.")
        print(" ")
        self.show_objects()
        choice = self.show_choices()
        return self.return_next(choice[0], choice[1])

    # function to initialize security check
    def init_security(self):
        # Determine which directions the security check controls
        control = []
        index = 1
        for i in self.adjacent:
            if type(i) == bool:
                pass
            elif i % 2 == 0:
                pass
            else:
                control.append(index)
            index += 1

        print(f"In order to proceed to the controlled area, you must pass a security check.")
        print(" ")
        self.show_objects()
        choice = self.show_choices()

        # Add items to inventory
        if choice[0] > 7:
            return self.return_next(choice[0], choice[1])
            
        # Check if security check is needed, and if so, act accordingly
        if choice[0] in control:
            print("Conducting security check...")
            for i in inventory:
                if i.return_type() == "weapon":
                    print("(VIOLATION) The security officer tells you:")
                    print("北京地铁禁止携带武器上车")
                    return self.return_next(7, choice[1])
                else:
                    pass
        return self.return_next(choice[0], choice[1])

    # function to initialize platform
    def init_platform(self):
        lines = station_dict[room_dict[self.identifier][1][0]][2]
        print("This is a station platform. The following trains serve this platform:")
        for i in lines:
            print(f"{i[1]} towards {i[3]}")
        print(" ")
        self.show_objects()
        choice = self.show_choices()
        return self.return_next(choice[0], choice[1], choice[2])
        
# Class to create a train
# line_num : unique string marking the line, with M for metro and B for bus
# line_des : string describing the line to the player
# direct : integer marking the direction of travel, (-1) clockwise/southbound/wetbound ; (1) counterclockwise/northbound/eastbound
# direct_des : string describing the direction to the player
# initial : unique integer station identifier to denote initial starting position
# route : list of station identifiers that denote the order in which the train reaches stations
class Train:
    def __init__(self, line_num, line_des, direct, direct_des, initial, route):
        self.line_num = line_num
        self.line_des = line_des
        self.direct = direct
        self.direct_des = direct_des
        self.initial = initial
        self.route = route[::direct]
        # Index for remembering which station the train is at
        self.index = 0
        self.length = len(route)
        # Show train at initial stop
        for i in station_dict[self.route[self.index]][2]:
            if i[0] == self.line_num and i[2] == self.direct:
                i[5] = True
            else:
                pass

    # Function that moves the train to the next station
    def move_train(self):
        # Remove train from station
        for i in station_dict[self.route[self.index]][2]:
            if i[0] == self.line_num and i[2] == self.direct:
                i[5] = False
                break
            else:
                pass
        self.index += 1
        # Check for end of track
        if self.index == self.length:
            return -1
        # Add train to station
        for i in station_dict[self.route[self.index]][2]:
            if i[0] == self.line_num and i[2] == self.direct:
                if self.index == self.length - 1:
                    pass
                else:
                    i[5] = True
                break
            else:
                pass
        self.station_num = station_dict[self.route[self.index]][3]
        self.station_name = station_dict[self.route[self.index]][0]
        return 0

    # Function that prints the train to the user
    def print_train(self):
        print(f"{self.line_des} towards {self.direct_des}   |   {self.station_name}")
        divide()
        print("(1) Disembark")
        choices = 1
        if self.index != self.length - 1:
            print("(2) Stay on")
            choices = 2
        print(" ")
        while True:
            train_in = detint(input("Your choice: "), limit=choices)
            if train_in != -1:
                break
            else:
                pass
        # If player decides to disembark, return the platform object
        # If player decides to stay on, do nothing
        if train_in == 1:
            return str(hex(self.station_num[0])[1:])
        elif train_in == 2:
            pass

    # Function that returns the location of the train
    def return_location(self):
        return self.route[self.index]
                            

# Directory (dict) of rooms, whether the player has discovered them or not, and transit network info for platforms
# Identifier (key) : [Discovered, [Stations]]
# Identifier : integer corresponding to the unique room id
# Discovered : boolean marking whether a player has found the room
# [Stations] : a list of unique station identifiers that correlates the platform to the station, other rooms default to 0

room_dict = {
    10000: [False, [0]],
    10001: [False, [100]],
    10002: [False, [0]],
    10003: [False, [100]],
    10004: [False, [0]],
    10005: [False, [101]],
    10006: [False, [0]],
    10007: [False, [101]],
    10008: [False, [0]],
    10010: [False, [0]],
    10012: [False, [0]],
    10014: [False, [0]],
    10016: [False, [0]],
    10018: [False, [0]],
    10020: [False, [0]],
    20000: [False, [0]],
    20002: [False, [0]],
    20004: [False, [0]],
    20006: [False, [0]],
    20008: [False, [0]],
    20010: [False, [0]],
    20012: [False, [0]],
    20014: [False, [0]],
    20016: [False, [0]],
    30000: [False, [0]],
    30002: [False, [0]],
    30004: [False, [0]],
    30006: [False, [0]],
    30008: [False, [0]],
    30010: [False, [0]],
    30012: [False, [0]],
    30014: [False, [0]],
    30016: [False, [0]],
    30018: [False, [0]],
    30020: [False, [0]],
    30022: [False, [0]],
    30024: [False, [0]],
    30026: [False, [0]],
    30028: [False, [0]],
    30030: [False, [0]],
    30032: [False, [0]],
}


# Directory (dict) of stations, metadata concerning the stations, and transit network info for the stations
# Identifier (key) : [Name, [Lines served], [[Line #, Line Descriptor, Direction, Direction Descriptor, Variant, Availability]], [Platforms]]
# Name : a string that contains the name of the station
# [Lines served] : a list of Line #s denoting the lines that serve the station
# Line # : a unique string marking the line, with M for metro and B for bus
# Direction : an integer marking the direction of travel, (-1) counterclockwise/southbound/westbound ; (1) clockwise/northbound/eastbound
# Variant : an integer for variants, defaults to (0)
# Availability : a boolean denoting whether the train is present in the station, defaults to False
# [Platforms] : a list of unique room identifiers that correlate the station to platforms

station_dict = {
    100 : ["天安门东", ["M1"], [["M1", "北京地铁1号线", -1, "苹果园", 0, False], ["M1", "北京地铁1号线", 1, "四惠东", 0, False]], [10001, 10003]],
    101 : ["天安门西", ["M1"], [["M1", "北京地铁1号线", -1, "苹果园", 0, False], ["M1", "北京地铁1号线", 1, "四惠东", 0, False]], [10005, 10007]] 
}


# Directory (dict) of trains serving each route
# Key : [Trains]
# Identifier (key) : a tuple, [Line #, Direction, Variant]
# [Trains] : A list of Train objects denoting trains that are serving the route

train_dict = {
    ("M1", -1, 0): [],
    ("M1", 1, 0): []
}

# List of train routes
# [[[Line #, Direction, Variant], Line Descriptor, Direction Descriptor, Initial, Route]]
line_M1 = [101, 100]
train_list = [[("M1", -1, 0), "北京地铁1号线", "苹果园", 100, line_M1],
              [("M1", 1, 0), "北京地铁1号线", "四惠东", 101, line_M1]]
