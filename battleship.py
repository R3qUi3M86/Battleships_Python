from copy import deepcopy
import random
import os
import time

player1 = "Player 1"
player2 = "Player 2"
AIPLAYER = "AI Player"
VSHUMAN = "vsHUMAN"
VSAI = "vsAI"

MAIN_MENU = "main_menu"
SETTINGS_MENU = "settings_menu"
SHIP_SHAPE_MENU = "ship_shape_menu"
BOARD_SIZE_MENU = "board_size_menu"
MAX_TURNS_MENU = "max_turns_menu"
OPONENT_MENU = "oponent_menu"
SHOTS_PER_TURN_MENU = "shots_per_turn_menu"

board_size = 5
dynamic_shooting = True
straight_ships_only = True
shots_per_player = 3
max_turns = 50
game_mode = VSAI

SHOOTING = "shooting"
PLACEMENT = "placement"
INVALID_INPUT = "invalid_input"
QUIT = "quit"
CANCEL = "cancel"
CANCEL_TUPLE = -1, -1

HIT = "hit"
MISS = "miss"
SUNK = "sunk"
REPEATING = "repeating"

SHIP_SIGN = "#"
MISS_SIGN = "."
WATER_SIGN = "~"
HIT_SIGN = "!"
SUNK_SIGN = "X"
CONCEALED = "concealed"
VISIBLE = "visible"

board1 = []
board2 = []
player1_ships = []
player2_ships = []
total_ship_size = 0
current_ship_size = 0
current_ship_coordinates = []
turn = 1

#OUTPUT LAYER:
#Wipes console from previous prints
def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

#Displays menu options
def display_main_menu():
    clear_console()
    print("\n   MAIN MENU")
    print("\n1. START GAME")
    print("2. SETTINGS")

#Displays game settings
def display_settings_menu():
    clear_console()
    print("\n   SETTINGS")
    print(f"\n1. Set game mode         (currently: {get_game_mode_description()})")
    print(f"2. Set ship shape rules  (currently: {get_ship_shape_rules_description()})")
    print(f"3. Set board size        (currently: {board_size})")
    print(f"4. Set turn limit        (currently: {max_turns})")
    print(f"5. Set shoots per player (currently: {get_shooting_mechanics_description()})")


#Displays oponent settings menu
def display_oponent_settings_menu():
    clear_console()
    print("\n   GAME MODE SETTINGS")
    print(f"\n1. Single player (default) {get_selected_option_sign(OPONENT_MENU, 1)}")
    print(f"2. Multiplayer {get_selected_option_sign(OPONENT_MENU, 2)}")

#Displays ship shape menu
def display_ship_shape_menu():
    clear_console()
    print("\n   SHIP SHAPE RULES SETTINGS")
    print(f"\n1. Straight ships only (default) {get_selected_option_sign(SHIP_SHAPE_MENU, 1)}")
    print(f"2. Any shape ships {get_selected_option_sign(SHIP_SHAPE_MENU, 2)}")

#Displays board size menu
def display_board_size_menu():
    clear_console()
    print("\n   BOARD SIZE SETTINGS")
    print(f"\nCurrent board size: {board_size}")
    print("Default: 5")

#Displays max turns menu
def display_max_turns_menu():
    clear_console()
    print("\n   TURN LIMIT SETTINGS")
    print(f"\nCurrent turn limit: {max_turns}")
    print("Default: 50")

#Displays shots per turn menu
def display_shots_per_turn_menu():
    clear_console()
    print("\n   SHOTS PER TURN SETTINGS")
    print(f"\nCurrent shots per turn: {get_shooting_mechanics_description()}")
    print("Default: dynamic")

def get_ship_shape_rules_description():
    return "straight ships only" if straight_ships_only == True else "any shape ships"

def get_game_mode_description():
    return "multiplayer" if game_mode == VSHUMAN else "single player"

def get_shooting_mechanics_description():
    return "dynamic" if dynamic_shooting == True else str(shots_per_player)

def get_selected_option_sign(menu_type, menu_option):
    if menu_type == OPONENT_MENU:
        if game_mode == VSAI and menu_option == 1:
            return "<- SELECTED"
        elif game_mode == VSHUMAN and menu_option == 2:
            return "<- SELECTED"
    elif menu_type == SHIP_SHAPE_MENU:
        if straight_ships_only == True and menu_option == 1:
            return "<- SELECTED"
        elif straight_ships_only == False and menu_option == 2:
            return "<- SELECTED"
    return ""

#Shows turns left counter on above dual game board
def display_turn_counter(turn):
    print(f"Turns left: {max_turns-turn+1}")

#Asks for any key press
def press_any_key_prompt():
    print("\n\n")
    os.system('pause') #might not work on Linux

#Signals players that the ship placement phase is now comencing
def ship_placement_phase_screen():
    clear_console()
    print("\n   SHIP PLACEMENT PHASE")
    press_any_key_prompt()

#Displays whish player takes turn it is
def display_which_player_takes_action(player):
    player = player1 if player == player1 else player2
    clear_console()
    print(f"\n{player} it is your turn now!")
    press_any_key_prompt()

#Displays single board for current player
def display_single_board(player):
    numbers_line = get_number_board_label()
    letters_line = get_letter_indices()
    board = get_player_board(player)
    print(f"\n{player}")
    print("  " + "  ".join(numbers_line))
    for index, value in enumerate(letters_line):
        print(value + " " + "  ".join(board[index])+" "+value)
    print("  " + "  ".join(numbers_line))

#Displays dual board -> one for current player and second representing enemy teritory
def display_both_boards(current_player, enemy_ships_visibility_mode):  
    enemy_board = get_enemy_player_board(current_player, enemy_ships_visibility_mode)
    numbers_line = get_number_board_label()
    letters_line = get_letter_indices()
    player_board = get_player_board(current_player)
    spaces = "         " if board_size < 10 else "        "

    print(get_boards_player_label(current_player))
    print("  " + " ".join(numbers_line) + spaces + " ".join(numbers_line))
    for index, value in enumerate(letters_line):
        print(value + " " + " ".join(player_board[index]) + " " + value + "     " + value + " " + " ".join(enemy_board[index]) + " " + value)
    print("  " + " ".join(numbers_line) + spaces + " ".join(numbers_line))

#Gets string array of number indices as board column labels
def get_number_board_label():
    return [str(i + 1) for i in range(board_size)]

#Gets string array of letter indices as board row labels
def get_letter_indices():
    return [chr(65 + i) for i in range(board_size)]

#Returns label for naming the boards
def get_boards_player_label(player):
    label = ""
    if player == player1:
        label += "\nPlayer 1 (You)"
    else:
        label += "\nPlayer 2 (You)"

    #adding certain amount of spaces
    for i in range(2*board_size - 6):
        label += " "

    if player == player1:
        label += "Player 2 (Enemy)"
    else:
        label += "Player 1 (Enemy)"

    return label

#Prints shot result based on its status
def display_shot_result(player, shot_status):
    if player == AIPLAYER:
        if shot_status == HIT:
            print("\nEnemy has hit our vessel!")
        elif shot_status == SUNK:
            print("\nEnemy has hit our vessel!\nOur ship is sinking!")
        elif shot_status == MISS:
            print("\nEnemy Missed...")
        else:
            print("\nEnemy repeats shot in the same spot - they are wasting ammo...")
    else:
        if shot_status == HIT:
            print("\nEnemy vessel hit!")
        elif shot_status == SUNK:
            print("\nEnemy vessel hit!\nEnemy ship is sinking!")
        elif shot_status == MISS:
            print("\nMiss...")
        else:
            print("\nWe already shot that spot - its a waste of ammo...")
    press_any_key_prompt()

#Displays message informing user that he provided invalid input and waits 3 seconds
def invalid_input_message():
    print("\nInvalid input!")
    time.sleep(1)

#Prints game results
def print_game_results():

    if player_has_won(player1) and player1 != AIPLAYER:
        dual_board_refresh(player1, VISIBLE)
        print("\n  Ships belonging to Player 2 sunk down into the abyss...\n               PLAYER 1 IS VICTORIOUS!!!")
    elif player_has_won(player2) and player2 != AIPLAYER:
        dual_board_refresh(player2, VISIBLE)
        print("\n  Ships belonging to Player 1 sunk down into the abyss...\n               PLAYER 2 IS VICTORIOUS!!!")
    elif player_has_won(player1) and player1 == AIPLAYER:
        dual_board_refresh(player2, VISIBLE)
        print("\n  Ships belonging to Player 2 sunk down into the abyss...\n               AI PLAYER IS VICTORIOUS!!!")
    elif player_has_won(player2) and player2 == AIPLAYER:
        dual_board_refresh(player1, VISIBLE)
        print("\n  Ships belonging to Player 1 sunk down into the abyss...\n               AI PLAYER IS VICTORIOUS!!!")
    else:
        clear_console()
        display_single_board(player1)
        display_single_board(player2)
        print("\n  Battle took too much time and storm came.\n               It's a tie...")

def single_board_refresh(player):
    clear_console()
    display_single_board(player)

def dual_board_refresh(current_player, enemy_ships_visibility_mode):
    clear_console()
    display_turn_counter(turn)
    display_both_boards(current_player, enemy_ships_visibility_mode)

#INPUT LAYER
#Gets valid user input while user is in main menu
def get_valid_menu_input(menu_type):
    while True:
        valid_menu_input = get_user_menu_input(menu_type)
        
        if valid_menu_input == QUIT:
            quit()
        elif valid_menu_input == "" and menu_type != MAIN_MENU:
            break
        elif menu_type == MAIN_MENU:
            if valid_menu_input in ["1","2"]:
                break
            else:
                invalid_input_message()
                display_main_menu()
        elif menu_type == SETTINGS_MENU:
            if valid_menu_input in [str(i) for i in range(1,6)]:
                break
            else:
                invalid_input_message()
                display_settings_menu()
        elif menu_type == OPONENT_MENU:
            if valid_menu_input in ["1","2"]:
                break
            else:
                invalid_input_message()
                display_oponent_settings_menu()
        elif menu_type == SHIP_SHAPE_MENU:
            if valid_menu_input in ["1","2"]:
                break
            else:
                invalid_input_message()
                display_ship_shape_menu()
        elif menu_type == BOARD_SIZE_MENU:
            if valid_menu_input in [str(i) for i in range(5,11)]:
                break
            else:
                invalid_input_message()
                display_board_size_menu()
        elif menu_type == MAX_TURNS_MENU:
            if valid_menu_input in [str(i) for i in range(5,51)]:
                break
            else:
                invalid_input_message()
                display_max_turns_menu()
        elif menu_type == SHOTS_PER_TURN_MENU:
            if valid_menu_input.lower() in ["1","2","3","4","5","d"]:
                break
            else:
                invalid_input_message()
                display_shots_per_turn_menu()

    return valid_menu_input

#Prompts user for input while in menu
def get_user_menu_input(menu_type):
    if menu_type == MAIN_MENU:
        user_input = input("\nPlease provide number for above menu option or,\ntype quit to exit\n->>")
    elif menu_type == SETTINGS_MENU or menu_type == SHIP_SHAPE_MENU or menu_type == OPONENT_MENU:
        user_input = input("\nPlease provide number for above menu option or,\ntype quit to exit or,\npress ENTER to go up one menu level\n ->>")
    elif menu_type == BOARD_SIZE_MENU:
        user_input = input("\nPlease provide number from 5 to 10 or,\ntype quit to exit or,\npress ENTER to go up one menu level\n ->>")
    elif menu_type == MAX_TURNS_MENU:
        user_input = input("\nPlease provide number from 5 to 50 or,\ntype quit to exit or,\npress ENTER to go up one menu level\n ->>")
    elif menu_type == SHOTS_PER_TURN_MENU:
        user_input = input("\nType 'D' for dynamic shoots ammount\n(equal to size of largest ship affloat for current player) or,\nprovide number from 1 to 5 or,\ntype quit to exit or,\npress ENTER to go up one menu level\n ->>")
    return user_input

#ask user if he wants play again
def play_again():
    clear_console()
    user_input = ""
    while user_input.lower() != "n" and user_input.lower() != "y":
        user_input = input("Do you want to play again (Y/N) :")
    if user_input.lower() == "y":
        main_menu()
    else:
        quit()

#Gets valid input from user (checks format and assure that input is within board size)
def get_valid_user_input(player, MODE):
    while True:
        if MODE == PLACEMENT:
            single_board_refresh(player)
            print(f"\nNow placing ship size of: {total_ship_size}, parts remainig to place: {current_ship_size}")
        else:
            dual_board_refresh(player, CONCEALED)

        user_input = get_user_input(MODE)

        if user_input.lower() == QUIT:
            quit()
        elif user_input.lower() == CANCEL and MODE == PLACEMENT:
            return CANCEL_TUPLE
        elif is_valid_format(user_input):
            coordinates = convert_input_string_to_tuple(user_input)
            if coordinates_in_board_size(coordinates):
                return coordinates
            else:
                invalid_input_message()
        else:
            invalid_input_message()

#Checks if user_input is 2-signs or 3-signs long and first sign is letter and second and/or third sign is digit
def is_valid_format(user_input):
    if len(user_input) == 2 and user_input[0].isalpha() and user_input[1].isdigit():
        return True
    elif len(user_input) == 3 and user_input[0].isalpha() and user_input[1].isdigit() and user_input[2].isdigit():
        return True
    else:
        return False

#Gets user input string with prompt type chaning based on MODE
def get_user_input(MODE):
    if MODE == SHOOTING:
        user_input = input("\nTake your shot admiral!\n(example: C2) -> ")
    elif MODE == PLACEMENT:
        user_input = input("\nPlace your ship on water Admiral!\n(CANCEL - abort current ship placement)\n(example input: D2) -> ")
    return user_input

#Returns True if coordinates are within board dimensions
def coordinates_in_board_size(coordinates):
    if coordinates[0] < board_size and coordinates[1] < board_size:
        return True
    else:
        return False

#Converts user input string into int tuple
def convert_input_string_to_tuple(valid_user_input):
    row = 0
    col = 0
     
    if len(valid_user_input) == 2:
        col = int(valid_user_input[1]) -1

    else:
        col = int(valid_user_input[1]+valid_user_input[2]) -1

    for row_index in range(26):
        if chr(97+row_index) == valid_user_input[0].lower():
            row = row_index
            return row, col

#LOGIC LAYER:
#Gets board for parsed player variable
def get_player_board(player):
    if player == player1:
        return board1 
    else:
        return board2

#Gets board for enemy player with concealed or revealed ships based on mode
def get_enemy_player_board(player, enemy_ships_visibility_mode):
    enemy_board = []
    
    if player == player2:
        enemy_board = deepcopy(board1)
    else:
        enemy_board = deepcopy(board2)
    
    if enemy_ships_visibility_mode == CONCEALED:
        for row in range(board_size):
            for col in range(board_size):
                if enemy_board[row][col] == SHIP_SIGN:
                    enemy_board[row][col] = WATER_SIGN

    return enemy_board

#Returns global variable with ships list for given player
def get_player_ships(player):
    if player == player1:
        return player1_ships
    else:
        return player2_ships

#Calculates number of shots for given player based on largest ship size for given player
def get_shots_ammount(player):
    ships = get_player_ships(player)
    largest_ship_size = 0

    for ship in ships:
        if len(ship) > largest_ship_size:
            largest_ship_size = len(ship)

    return largest_ship_size


#Determines shooting result, makes mark on board and prints result
def shooting_result(shot, player):
    enemy_player = swich_player(player)
    enemy_board = get_player_board(enemy_player)
    enemy_player_ships = get_player_ships(enemy_player)
    
    if enemy_board[shot[0]][shot[1]] == SHIP_SIGN:
        shot_status = HIT
        enemy_board[shot[0]][shot[1]] = HIT_SIGN
        
        if ship_has_sunk(enemy_player_ships, shot, enemy_player):
            shot_status = SUNK
    
    elif enemy_board[shot[0]][shot[1]] == WATER_SIGN:
        shot_status = MISS
        enemy_board[shot[0]][shot[1]] = MISS_SIGN
    else:
        shot_status = REPEATING
    
    if player == AIPLAYER:
        dual_board_refresh(enemy_player, CONCEALED)
        print(f"\nEnemy shot: {convert_tuple_to_board_coordinates([shot])}")
        display_shot_result(player, shot_status)
    else:
        dual_board_refresh(player, CONCEALED)
        display_shot_result(player, shot_status)


#Returns true or false if the enemy ship has been sunk or not
def ship_has_sunk(ships, shot, enemy_player):
    enemy_board = get_player_board(enemy_player)
    for ship in ships:
        if shot in ship:
            ship_modules_afloat = len(ship)
            for ship_module in ship:
                if ship_module_is_destroyed(ship_module, enemy_board):
                    ship_modules_afloat -= 1
                    if ship_modules_afloat == 0:
                        sink_destroyed_ship(enemy_board, ship, ships)
                        return True
    return False

#Returns true if checked ship module is already destroyed
def ship_module_is_destroyed(ship_module, enemy_board):
    if enemy_board[ship_module[0]][ship_module[1]] == HIT_SIGN:
        return True
    else:
        return False

#Removes ship from the game and marks X on board at its last position
def sink_destroyed_ship(board, ship, ships):
    for ship_module in ship:
        board[ship_module[0]][ship_module[1]] = SUNK_SIGN
    ships.remove(ship)

#Switches to other player
def swich_player(player):
    if player == player1:
        return player2
    else:
        return player1

#Places all ships for current player
def place_all_ships(player):
    ships_in_port = generate_ship_sizes_list()
    
    while len(ships_in_port) != 0:
        ship_size = ships_in_port[0]
        if player != AIPLAYER:
            current_ship_coordinates = get_current_ship_coordinates(player, ship_size)
        else:
            current_ship_coordinates = get_current_ship_coordinates_for_AI(player, ship_size)
        assign_ship_to_player(player, current_ship_coordinates)
        ships_in_port.pop(0)

#Allows user to place single ship on board and returns its modules coordinate as tuples list
def get_current_ship_coordinates(player, ship_size):
    global current_ship_size
    global total_ship_size
    global current_ship_coordinates

    current_ship_size = ship_size
    total_ship_size = ship_size
    board = get_player_board(player)
    backup_board = deepcopy(board)
    current_ship_coordinates = []

    while current_ship_size != 0:
        coordinates = get_valid_user_input(player, PLACEMENT)

        if coordinates == CANCEL_TUPLE:
            board = deepcopy(backup_board)
            revert_to_backup_board(player, board)
        elif legal_placement(player, board, coordinates) == False:
            press_any_key_prompt()
        else:
            put_ship_module_into_game(coordinates, board)

    return current_ship_coordinates

#AI BLOCK STARTS HERE
#Gets coordinates for AI player
def get_valid_AI_input(player, MODE):
    if MODE == PLACEMENT:
        coordinates = get_legal_AI_ship_module_coordinates(player)
    else:
        coordinates = get_AI_shot_coordinates(player)

    return coordinates

#AI shooting mechanics BLOCK BEGINS
#Gets shot coordinates for AI player:
def get_AI_shot_coordinates(player):
    enemy_board = get_enemy_player_board(player, CONCEALED)
    hit_sign_list = get_list_of_sign_coordinates(enemy_board, HIT_SIGN)
    sunk_sign_list = get_list_of_sign_coordinates(enemy_board, SUNK_SIGN)
    water_tiles = get_list_of_sign_coordinates(enemy_board, WATER_SIGN)

    squares_adjacent_to_sunken_sign = make_adjacent_coordinates_for_area(sunk_sign_list)
    water_tiles = remove_list_items_from_list(water_tiles, squares_adjacent_to_sunken_sign)
    
    if len(hit_sign_list) != 0:
        water_tiles = get_legal_coordinates_next_to_damaged_ship(water_tiles, hit_sign_list)
    else:
        enemy_player = swich_player(player)
        enemy_player_ships = get_player_ships(enemy_player)
        largest_ship_size = len(enemy_player_ships[0])
        water_tiles = get_water_hunting_tiles_for_specific_ship_size(enemy_player, enemy_board, water_tiles, largest_ship_size)
    
    return random.choice(water_tiles)

#Returns water tiles where largest ship can be fitted
def get_water_hunting_tiles_for_specific_ship_size(enemy_player, enemy_board, water_tiles, ship_size):
    primary_shot_coordinate_list = []
    secondary_shot_coordinate_list = []

    for coordinate in water_tiles:
        area = create_potential_ship_placement_area(enemy_player, enemy_board, [coordinate], ship_size-1)
        
        if ship_does_not_fit_in_area(coordinate, area, ship_size):
            pass
        elif straight_ships_only == True and ship_fits_horizontal_and_vertical(coordinate, area, ship_size):
            primary_shot_coordinate_list.append(coordinate)
        elif len(primary_shot_coordinate_list) == 0:
            secondary_shot_coordinate_list.append(coordinate)

    return primary_shot_coordinate_list if len(primary_shot_coordinate_list) != 0 else secondary_shot_coordinate_list
        
#Returns True if ship of given size will fit in given coordinates both horizontally and vertically
def ship_fits_horizontal_and_vertical(coordinate, area, ship_size):
    return True if ship_fits_horizontally(coordinate, area, ship_size) and ship_fits_vertically(coordinate, area, ship_size) else False

#Tries to sink already damaged ship
def get_legal_coordinates_next_to_damaged_ship(water_tiles, hit_sign_list):
    squares_adjacent_to_hit_sign = make_adjacent_coordinates_for_area(hit_sign_list)
    water_tiles = list_intersection(water_tiles, squares_adjacent_to_hit_sign)

    if len(hit_sign_list) >= 2 and straight_ships_only == True:
        water_tiles_copy = deepcopy(water_tiles)
        
        if ship_is_horizontal(hit_sign_list):
            
            for square in water_tiles_copy:
                if square[0] != hit_sign_list[0][0]:
                    water_tiles.remove(square)
        
        else:
            
            for square in water_tiles_copy:
                if square[1] != hit_sign_list[0][1]:
                    water_tiles.remove(square)
    
    return water_tiles
#AI shooting mechanics BLOCK ENDS

#AI ship placement mechanics BLOCK BEGINS
#Place single ship on board for AI player and returns its modules coordinate as tuples list
def get_current_ship_coordinates_for_AI(player, ship_size):
    global current_ship_size
    global total_ship_size
    global current_ship_coordinates

    current_ship_size = ship_size
    total_ship_size = ship_size
    board = get_player_board(player)
    current_ship_coordinates = []
    
    while current_ship_size != 0:
        coordinates = get_valid_AI_input(player, PLACEMENT)
        put_ship_module_into_game(coordinates, board)

    return current_ship_coordinates

#Gets legal ship module placement coordinates for AI player
def get_legal_AI_ship_module_coordinates(player):
    board = get_player_board(player)

    random_module_coordinates = []
    
    if current_ship_size == total_ship_size:
        valid_water_squares = get_valid_ship_placement_coordinates_list(player, board)
        random_module_coordinates = random.choice(valid_water_squares)
    
    else:
        adjacent_squares = make_valid_adjacent_placement_coordinates_for_area(player, board, current_ship_coordinates)
        
        if straight_ships_only == True:
            ship_area = create_potential_ship_placement_area(player, board, current_ship_coordinates, current_ship_size)
            ship_area = filter_non_straight_ship_shape_coordinates(ship_area, total_ship_size, current_ship_coordinates)
            intersescting_fields = list_intersection(ship_area, adjacent_squares)
            random_module_coordinates = random.choice(intersescting_fields)
        else:
            random_module_coordinates = random.choice(adjacent_squares)

    return random_module_coordinates

#Returns suitable water coordinate for current ship placement
def get_valid_ship_placement_coordinates_list(player, board):
    water_squares = get_list_of_sign_coordinates(board, WATER_SIGN)
    
    if len(get_player_ships(player)) == 0: #For optimizing first ship placement
        return water_squares

    legal_water_squares = deepcopy(water_squares)
    
    for coordinates in water_squares:
        if coordinate_adjacent_to_other_ship(coordinates, player, board):
            legal_water_squares.remove(coordinates)
    
    valid_water_squares = deepcopy(legal_water_squares)
    
    for coordinates in legal_water_squares:
        if ship_will_not_fit(player, board, coordinates, current_ship_size, total_ship_size):
            valid_water_squares.remove(coordinates)

    return valid_water_squares

#Checks if ship can be fitted in area adjacent to given coordinates
def ship_will_not_fit(player, board, coordinates, ship_size, total_ship_size):
    area = [coordinates]
    area = create_potential_ship_placement_area(player, board, area, ship_size-1)

    return True if ship_does_not_fit_in_area(coordinates, area, total_ship_size) else False

#Creates list of adjacent coordinates (within reach of current_ship_size) to ship_coordinates and appends_current_ship_coordinates to that list
def create_potential_ship_placement_area(player, board, ship_coordinates, ship_size):
    ship_area_coordinates = deepcopy(ship_coordinates)
    
    for _ in range(ship_size):
        adjacent_coordinates_list = make_valid_adjacent_placement_coordinates_for_area(player, board, ship_area_coordinates)
        for coord in adjacent_coordinates_list:
            if coord not in ship_area_coordinates:
                ship_area_coordinates.append(coord)

    return ship_area_coordinates

#Returns True if ship cannot be placed within given area
def ship_does_not_fit_in_area(coordinates, area, ship_size):
    if ship_size <= len(area):
        if straight_ships_only == True:
            
            if ship_fits_horizontally(coordinates, area, ship_size):
                return False
            elif ship_fits_vertically(coordinates, area, ship_size):
                return False
            return True
        
        else:
            return False
    return True

#Creates list of valid adjacent squares for given area (filters out non water tiles and tiles adjacent to other ships)
def make_valid_adjacent_placement_coordinates_for_area(player, board, area):
    area_adjacent_coordinates = make_adjacent_coordinates_for_area(area)

    valid_adjacent_coordinates = deepcopy(area_adjacent_coordinates)
    for coordinate in area_adjacent_coordinates:
        if board[coordinate[0]][coordinate[1]] != WATER_SIGN or coordinate_adjacent_to_other_ship(coordinate, player, board):
            valid_adjacent_coordinates.remove(coordinate)
    
    return valid_adjacent_coordinates

#Creates list of adjacent squares for given area
def make_adjacent_coordinates_for_area(area):
    area_adjacent_coordinates = []
    
    for coordinates in area:
        adjacent_coordinates = make_adjacency_list(coordinates)
        for square in adjacent_coordinates:
            if square in area_adjacent_coordinates:
                adjacent_coordinates.remove(square)
        
        for coordinates in adjacent_coordinates:
            area_adjacent_coordinates.append(coordinates)
    
    return area_adjacent_coordinates

#Removes coordinates which are not in line with given ship placement
def filter_non_straight_ship_shape_coordinates(area, ship_size, ship_coordinates):
    valid_squares = []
    
    if len(ship_coordinates) == 1:
        horizontal_area = []
        if ship_fits_horizontally(ship_coordinates[0], area, ship_size):
            for square in area:
                if square[0] == ship_coordinates[0][0]:
                    horizontal_area.append(square)
        vertical_area = []
        if ship_fits_vertically(ship_coordinates[0], area, ship_size):
            for square in area:
                if square[1] == ship_coordinates[0][1]:
                    vertical_area.append(square)
        
        valid_squares = horizontal_area
        for square in vertical_area:
            valid_squares.append(square)
    
    elif len(ship_coordinates) >= 2:
        if ship_is_horizontal(ship_coordinates):
            for square in area:
                if square[0] == ship_coordinates[0][0]:
                    valid_squares.append(square)
        else:
            for square in area:
                if square[1] == ship_coordinates[0][1]:
                    valid_squares.append(square)

    return valid_squares

#Places all ships for ai player and informs user when finished
def place_ships_for_AI_player(player):
    place_all_ships(player)
    clear_console()
    print("\nEnemy player fleet is now afloat!")
    press_any_key_prompt()
#AI ship placement mechanics BLOCK ENDS

#Returns True if ship is placed horizontally
def ship_is_horizontal(ship_coordinates):
    return True if ship_coordinates[0][0] == ship_coordinates[1][0] else False

#Returns true if ship does fit horizontally in given area
def ship_fits_horizontally(coordinates, area, ship_size):
    new_area = deepcopy(area)

    for square in area:
    
        if square[0] != coordinates[0]:
            new_area.remove(square)
    
    if ship_size <= len(new_area):
        return True
    else:
        return False

#Returns true if ship does fit vertically in given area
def ship_fits_vertically(coordinates, area, ship_size):
    new_area = deepcopy(area)

    for square in area:

        if square[1] != coordinates[1]:
            new_area.remove(square)

    if ship_size <= len(new_area):
        return True
    else:
        return False

#Returns list intersection
def list_intersection(list1, list2):
    list3 = [value for value in list1 if value in list2]
    return list3

#Removes from first list matching items from second list
def remove_list_items_from_list(target_list, subtracted_list):
    new_list = [item for item in target_list if item not in subtracted_list]
    return new_list

#Determines which player is human player and AI player
def determine_AI_player():
    global player1
    global player2
    player_number = random.choice([1, 2])
    
    if player_number == 1:
        player1 = AIPLAYER
        clear_console()
        print("\nAI player will play as Player 1 and will go first.")
        press_any_key_prompt()
    else:
        player2 = AIPLAYER
        clear_console()
        print("\nAI player will play as Player 2 and will go second.")
        press_any_key_prompt()
#AI BLOCK ENDS HERE

#Returns coordinates of given sign as list of tuples
def get_list_of_sign_coordinates(board, sign):
    sign_coordinates_list = []
    
    i = 0
    for row in board:
        j = 0
        for element in row:
            if element == sign:
                sign_coordinates_list.append((i,j))
            j += 1
        i += 1
    
    return sign_coordinates_list

#Returns game state to state before current ship placement
def revert_to_backup_board(player, board):
    global current_ship_size
    global current_ship_coordinates
    global board1
    global board2

    if player == player1:
        board1 = board
    else:
        board2 = board
    current_ship_size = total_ship_size
    current_ship_coordinates = []

#Puts new ship module into the battlefield
def put_ship_module_into_game(coordinates, board):
    global current_ship_coordinates
    global current_ship_size

    current_ship_coordinates.append(coordinates)
    current_ship_size -= 1
    board[coordinates[0]][coordinates[1]] = SHIP_SIGN

#Checks if placement is legal in current board and displays appropriate message if not legal
def legal_placement(player, board, coordinates):
    if board[coordinates[0]][coordinates[1]] == SHIP_SIGN:
        print("\nThat spot is already taken by your ship!")
    elif ship_not_adjacent_to_itself(coordinates, current_ship_coordinates):
        print(f"\nThis ship is {total_ship_size} squares long. Place next part next to already existing part of this ship!\nParts belonging to this ship: {convert_tuple_to_board_coordinates(current_ship_coordinates)}")
    elif coordinate_adjacent_to_other_ship(coordinates, player, board): 
        print(f"\nThats to close to our existing vessel!")
    elif straight_ships_only == True and ship_not_straight(coordinates):
        print(f"\nYou need to place your ship in straight line!")
    else:
        return True
    return False

#Ship placing phase for current player
def place_ships_on_board(player):
    place_all_ships(player)
    single_board_refresh(player)
    print("\nWhole fleet is now afloat Admiral!")
    press_any_key_prompt()

#Assings ships position to global parameter
def assign_ship_to_player(player, current_ship_coordinates):
    global player1_ships
    global player2_ships


    if player == player1:
        player1_ships.append(current_ship_coordinates)
    else:
        player2_ships.append(current_ship_coordinates)
    current_ship_coordinates = []

#Returns True or if coordinates are not adjacent to currently placed ship
def ship_not_adjacent_to_itself(coordinates, current_ship_coordinates):
    if len(current_ship_coordinates) != 0:
        adjacent_coordinate_list = make_adjacency_list(coordinates)
        
        for coord in adjacent_coordinate_list:
            if coord in current_ship_coordinates:
                return False
        return True

    else:
        return False

#Returns True or if coordinates is adjacent to other already existing ship
def coordinate_adjacent_to_other_ship(coordinate, player, board):
    adjacent_coordinate_list = make_adjacency_list(coordinate)
    for coord in adjacent_coordinate_list:
        if board[coord[0]][coord[1]] == SHIP_SIGN and coord not in current_ship_coordinates:
            return True
    return False

#Returns True if coordinates are not in straight line with current ship coordinates
def ship_not_straight(coordinates):
    if len(current_ship_coordinates) >= 2:
        if ship_is_horizontal(current_ship_coordinates):
            if coordinates[0] != current_ship_coordinates[0][0]:
                return True
        else:
            if coordinates[1] != current_ship_coordinates[0][1]:
                return True
    return False

#Makes list of adjacent squares as int tuple to parsed coordinate (int tuple)
def make_adjacency_list(coordinates):
    adjacency_list = []
    adjacency_list.append((coordinates[0]-1, coordinates[1]))
    adjacency_list.append((coordinates[0]+1, coordinates[1]))
    adjacency_list.append((coordinates[0], coordinates[1]-1))
    adjacency_list.append((coordinates[0], coordinates[1]+1))
    
    valid_adjacency_list = deepcopy(adjacency_list)
    
    for adjacent_square in adjacency_list:
        if adjacent_square[0] < 0 or adjacent_square[0] >= board_size or adjacent_square[1] < 0 or adjacent_square[1] >= board_size:
            valid_adjacency_list.remove(adjacent_square)
    
    return valid_adjacency_list

#Converts list of int tuples into list of strings expressed as game coordinates (for example [A1, B4])
def convert_tuple_to_board_coordinates(coordinates):
    field_list = []
    letter_indices = get_letter_indices()

    for coordinate in coordinates:
        field_list_element = letter_indices[coordinate[0]] + str(coordinate[1]+1)
        field_list.append(field_list_element)

    return field_list

#returns ships for current board size
def generate_ship_sizes_list():
    if board_size == 5:
        return [2,2,2,1,1]
    elif board_size == 6:
        return [3,2,2,1,1,1]
    elif board_size == 7:
        return [3,3,2,2,1,1,1]
    elif board_size == 8:
        return [3,3,2,2,2,1,1,1]
    elif board_size == 9:
        return [4,3,2,2,2,1,1,1,1]
    else:
        return [4,3,3,2,2,2,1,1,1,1]

#Prepares game according to current game settings
def prepare_game():
    global board1
    global board2

    board1 = initialize_game_board()
    board2 = initialize_game_board()

    ship_placement_phase_screen()
    
    if game_mode == VSAI:
        determine_AI_player()

        if player1 == AIPLAYER:
            place_ships_for_AI_player(player1)
            display_which_player_takes_action(player2)
            place_ships_on_board(player2)
        else:
            display_which_player_takes_action(player1)
            place_ships_on_board(player1)
            place_ships_for_AI_player(player2)

    else:
        display_which_player_takes_action(player1)
        place_ships_on_board(player1)

        display_which_player_takes_action(player2)
        place_ships_on_board(player2)

#Main game loop
def start_game():
    global turn
    global shots_per_player

    prepare_game()
    current_player = player1

    clear_console()
    print("\n   GAME BEGINS!")
    time.sleep(2)

    while turn <= max_turns and player_has_won(player1) == False and player_has_won(player2) == False:
        if game_mode == VSHUMAN:
            display_which_player_takes_action(current_player)

        if dynamic_shooting == True:
            shots_per_player = get_shots_ammount(current_player)

        if current_player == AIPLAYER:
                dual_board_refresh(swich_player(current_player), CONCEALED)
                print("\nIncomming fire from enemy ships!")
                press_any_key_prompt()

        for _ in range(shots_per_player):
            if current_player != AIPLAYER:
                shot = get_valid_user_input(current_player, SHOOTING)
                shooting_result(shot, current_player)
            else:
                shot = get_valid_AI_input(current_player, SHOOTING)
                shooting_result(shot, current_player)
            if player_has_won(player1) == True or player_has_won(player2) == True:
                break
        if current_player == player2:
                turn += 1
            
        current_player = swich_player(current_player)

#Initializes game board as board_size x board_size matrix and fills it with water signs
def initialize_game_board():
    return [[WATER_SIGN]*board_size for _ in range(board_size)]

#Returns true if given player has won the game
def player_has_won(player):
    if player == player2 and len(player1_ships) == 0:
        return True
    elif player == player1 and len(player2_ships) == 0:
        return True
    else:
        return False

def end_game():
    print_game_results()
    reset_game_state()
    press_any_key_prompt()

#Resets global variables
def reset_game_state():
    global board1
    global board2
    global player1
    global player2
    global player1_ships
    global player2_ships
    global current_ship_coordinates
    global turn

    board1 = []
    board2 = []
    player1_ships = []
    player2_ships = []
    current_ship_coordinates = []
    turn = 1
    player1 = "Player 1"
    player2 = "Player 2"

def play():
    start_game()
    end_game()
    play_again()

#Displays main menu and prompts for user input
def main_menu():
    display_main_menu()
    user_input = get_valid_menu_input(MAIN_MENU)
    if user_input == "1":
        play()
    else:
        game_settings()

#Displays game settings
def game_settings():
    display_settings_menu()
    user_input = get_valid_menu_input(SETTINGS_MENU)
    if user_input == "1":
        oponent_settings()
    elif user_input == "2":
        ship_shape_settings()
    elif user_input == "3":
        board_size_settings()
    elif user_input == "4":
        max_turns_settings()
    elif user_input == "5":
        shot_ammount_settings()
    else:
        main_menu()

#Gives user option to pick if he wants to play vs human or vs AI oponent
def oponent_settings():
    global game_mode

    display_oponent_settings_menu()
    user_input = get_valid_menu_input(OPONENT_MENU)
    if user_input == "1":
        game_mode = VSAI
    elif user_input == "2":
        game_mode = VSHUMAN
    game_settings()

#Gives user options to set ship shape rule -> only straight ships or any shape
def ship_shape_settings():
    global straight_ships_only

    display_ship_shape_menu()
    user_input = get_valid_menu_input(SHIP_SHAPE_MENU)
    if user_input == "1":
        straight_ships_only = True
    elif user_input == "2":
        straight_ships_only = False
    game_settings()

#Gives user option to set board size in range 5-10
def board_size_settings():
    global board_size

    display_board_size_menu()
    user_input = get_valid_menu_input(BOARD_SIZE_MENU)
    if user_input in [str(i) for i in range(5,11)]:
        board_size = int(user_input)
    game_settings()

#Gives user option to set ammount of maximum turns
def max_turns_settings():
    global max_turns

    display_max_turns_menu()
    user_input = get_valid_menu_input(MAX_TURNS_MENU)
    if user_input in [str(i) for i in range(5,51)]:
        max_turns = int(user_input)
    game_settings()

#Gives user option to set ammount of shots per player turn from 1-5 or dynamic
def shot_ammount_settings():
    global shots_per_player
    global dynamic_shooting

    display_shots_per_turn_menu()
    user_input = get_valid_menu_input(SHOTS_PER_TURN_MENU)
    if user_input.lower() == "d":
        dynamic_shooting = True
    elif user_input in [str(i) for i in (range(1,6))]:
        dynamic_shooting = False
        shots_per_player = int(user_input)
    game_settings()

#Display splash screen graphic (maybe read graphic from file?)
def splash_screen():
    with open('splash_graphic.txt') as graphic:
        for i in range(44):
            clear_console()
            for _ in range(14):
                print(graphic.readline().replace("\n",""))
            if i == 0:
                time.sleep(1)
            else:
                time.sleep(0.15)

def quit():
    print("\nBye, Bye...")
    time.sleep(1)
    clear_console()
    exit()

def main():
    splash_screen()
    press_any_key_prompt()
    main_menu()

main()