import os
import sys
from time import sleep
from classes import *
from initialize import *
from maps import *


# Run the train system
def trains():
    # Move existing trains
    for i in train_dict.values():
        for j in i:
            status = j.move_train()
            if status == 0:
                pass
            elif status == -1:
                i.remove(j)
            
    # Every five minutes initialize new train
    if time % 5 == 0:
        for i in train_list:
            train_dict[i[0]].append(Train(i[0][0], i[1], i[0][1], i[2], i[3], i[4]))

# Set adjacent types
def adjacent_types(room):
    room_list = []
    rooms = room.return_adjacent()
    for i in rooms:
        exec(f"room_list.append({i})")
    directions = ["north", "east", "south", "west", "above", "below"]  # For remembering correlation between direction and type
    types = ["entrance", "corridor", "checkpoint", "platform", "street"]  # For converting integer into type
    rooms = []  # Reuse rooms for storing the types
    for x in range(len(room_list)):
        if not room_list[x]:
            pass
        else:
            rooms.append((directions[x], types[room_list[x].classifier - 1]))
    room.set_adjacent(rooms)
    

# Main gameplay loop
# Keep track of the structure the player is in, rooms can be designated as structure connectors
# Each room returns object for next room

def main():
    # Initial start x4e24/20004 (dongchangan_street)
    # Goal end x2715/10005 or x2717/10007 (tiananmenxi_station)
    print("NAVIGATOR")
    sleep(1)
    print("by lnjng")
    sleep(1)
    print("Starting location: UNKNOWN")
    print("Ending location: 天安门西站")
    input("Press ENTER to continue")
    clear()
    goal = [10005, 10007]
    adjacent_types(x4e24)
    player = x4e24.print_room()
    while True:
        clear()
        room_list = []
        trains()
        global time
        time += 1
        if type(player) == Train:
            player = player.print_train()
        else:
            exec(f"room_list.append({player})")
            adjacent_types(room_list[0])
            # Check for win condition
            if room_list[0].identifier in goal:
                break
            # Print room to player
            player = room_list[0].print_room()
    # Win text
    print("天安门西站")
    divide()
    print(" ")
    sleep(3)
    print("CONGRATULATIONS! You've made it.")
    sleep(1)
    print(f"# of Turns: {time}")
    sleep(1)
    print("Thanks for playing.")
    sleep(1)
    print(" ")
    input("Press ENTER to exit")
    sys.exit()

# Start the game
def start():
    title_text = """
 ________   ________  ___      ___ ___  ________  ________  _________  ________  ________     
|\   ___  \|\   __  \|\  \    /  /|\  \|\   ____\|\   __  \|\___   ___\\   __  \|\   __  \    
\ \  \\ \  \ \  \|\  \ \  \  /  / | \  \ \  \___|\ \  \|\  \|___ \  \_\ \  \|\  \ \  \|\  \   
 \ \  \\ \  \ \   __  \ \  \/  / / \ \  \ \  \  __\ \   __  \   \ \  \ \ \  \\\  \ \   _  _\  
  \ \  \\ \  \ \  \ \  \ \    / /   \ \  \ \  \|\  \ \  \ \  \   \ \  \ \ \  \\\  \ \  \\  \| 
   \ \__\\ \__\ \__\ \__\ \__/ /     \ \__\ \_______\ \__\ \__\   \ \__\ \ \_______\ \__\\ _\ 
    \|__| \|__|\|__|\|__|\|__|/       \|__|\|_______|\|__|\|__|    \|__|  \|_______|\|__|\|__|
    """

    compass = """
                                        _                                       
                                        ]                                       
                                        ]f                                      
                                        ]Q                                      
                                        ]Qf                                     
                                        ]Q6                                     
                                        ]QQ/        .                           
                             ) a        ]QQf-     /'                            
                                ?6a/    ]QQQ'  _j"                              
                                  )4    ]QQQfajP                                
                        _aaaaaayQQQQ6/  ]QP'                                    
                  ????????????????????? )'                                      
                                      aj )?QQQQQQQQQQQQQ???????                 
                                 _a/aQQQ    4????' .                            
                               _j?  4QQQ    )Qa.                                
                              /?    ?QQQ       ?\/                              
                             '     ) QQQ          ?                             
                                     ]QQ                                        
                                      QQ                                        
                                      4Q                                        
                                      )Q                                        
                                       4                                        
                                       ]                                        
                                                                                
    """

    print(title_text)
    print(" ")
    print(compass)
    print(" ")
    print("(1) Start the game")
    print("(2) View rules")
    print(" ")
    
    while True:
        start_in = detint(input("Your choice: "), limit=2)
        if start_in != -1:
            print("Invalid choice")
            break
        else:
            pass

    if start_in == 1:
        clear()
        main()
    elif start_in == 2:
        clear()
        print(rules)
        print(" ")
        print(" ")
        print(" ")
        input("Press ENTER to continue")
        clear()
        start()
        
start()
