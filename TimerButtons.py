from time import sleep, time
import random
import SimonSays , WhackAMole, Sounds
import ButtonSetup
import ExportData

player_button_list = ButtonSetup.SetupPlayerButtons.button_list
auxillary_button_list = ButtonSetup.SetupAcceptButton.auxillary_button_list
active_player_button_list = []
turn_order_button_list = []
turn_in_progress = True
player_selection = False
records = {}

def gameTracker():
    game_state = "setup"
    while game_state != "complete":
        if game_state == "setup":
            game_state = gameSetup(game_state)
        if game_state == "determine_turn_order":
            game_state = determineTurnOrder(game_state)
        if game_state == "game_round":
            game_state = gameRound(game_state)
        if game_state == "game_end":
            pass
            
def gameSetup(game_state):
    '''This function will allow players to determine which buttons will be included in the current game
    the buttons will remain off and can be turned on by pressing.  This will add or remove the button objects
    to the active_player_button_list'''

    def gameSetupPressed(button):
        if button in active_player_button_list:
            active_player_button_list.remove(button)
            button.ledOff()
        else:
            active_player_button_list.append(button)
            button.ledOn()

    #What auxillary buttons will do, the first (main) will start the game, others will do other programs	
    def gameSetupAuxillaryPressed(button):
        if button == auxillary_button_list[0]:
            button.confirm_active_players = True
        #if button == auxillary_button_list[1]:
        #	SimonSays.simon_says_game()
        #if button == auxillary_button_list[2]:
        #	WhackAMole.whack_a_mole_game()

    #loop for waiting on confirmation
    while auxillary_button_list[0].confirm_active_players == False:
        for button in player_button_list:
            button.when_pressed = gameSetupPressed
        for button in auxillary_button_list:
            button.when_pressed = gameSetupAuxillaryPressed
        for button in active_player_button_list:
            button.ledToggle()
        sleep(.2)
        
        
    #Resets button state so that nothing will happen when pressed after this phase before next phase is active.
    for button in player_button_list:
        button.when_pressed = None
    
    #Returns game_state value to next phase
    return("determine_turn_order")

def determineTurnOrder(game_state):

    def determineTurnOrderPressed_Auxillary(button):
        if len(turn_order_button_list) == len(active_player_button_list):
            auxillary_button_list[0].player_selection = True

    def determineTurnOrderPressed(button):
        if button in turn_order_button_list:
            turn_order_button_list.remove(button)
            button.ledOff()
        else:
            turn_order_button_list.append(button)
            button.ledOn()

    for button in active_player_button_list:
        button.ledOff()
        
    while auxillary_button_list[0].player_selection == False:
        for button in active_player_button_list:
            button.when_pressed = determineTurnOrderPressed
        for button in auxillary_button_list:
            button.when_pressed = determineTurnOrderPressed_Auxillary

    #Resets button state so that nothing will happen when pressed
    for button in player_button_list:
        button.when_pressed = None
        button.ledOff()
    for button in auxillary_button_list:
        button.when_pressed = None
    
    return ("game_round")
    
def gameRound(game_state):

    if not records:
        for index, button in enumerate(active_player_button_list):
            player_name = input("Enter name for " +str(button.color)+ " player:")
            records[index] = {
                "Name" : player_name,
                "Color" : button.color,
                "First player?" : False,
                "Start time" : 0,
                "End time" : 0,
                "Turn time" : 0,
                "Pause time" : 0,
                "Pause count" : 0,
                "Unpause count" : 0,
                "Turn pause time" : 0,
                "Turn count" : 0,
                }
            
    def pause(pause_button):
        '''Allows any player to pause the game and any player to unpause the game.  The time should only count for the active player and will be subtracted from his total turn time
           as well as the person who paused and added to thier total pause time.  Also keeps track of amount of pauses'''
        resetButtons()
        print("test")
        pause_button.is_paused = True
        for button in active_player_button_list:
            button.held_down = True
            button.ledOff
            
        x=0
        while x < 5:
            pause_button.ledOn()
            sleep(.2)
            pause_button.ledOff()
            sleep(.2)
            x+=1
            
        pause_start_time = time()
        
        for button in active_player_button_list:
            button.when_released = unpause
            
        while pause_button.is_paused == True:
            pause_button.ledOff()
            sleep(.2)
            pause_button.ledOn()
            sleep(.2)
            for button in active_player_button_list:
                if button.active_player == True:
                    pass
                else:
                    button.ledOff()
            
        total_pause_time = records[active_player_button_list.index(pause_button)].get("Pause time") + (time() - pause_start_time)
        records[active_player_button_list.index(pause_button)].update({"Pause time" : total_pause_time})
        total_pause_count = records[active_player_button_list.index(pause_button)].get("Pause count") + 1
        records[active_player_button_list.index(pause_button)].update({"Pause count" : total_pause_count})


        for button in active_player_button_list:
            button.held_down = False
            #if button.active_player == True:
                #total_pause_time_turn = records[active_player_button_list.index(button)].get("Turn Pause time") + (time() - pause_start_time)
                #records[active_player_button_list.index(button)].update({"Turn Pause time" : total_pause_time_turn})
            if button.active_player == True:
                pause_turn = records[active_player_button_list.index(button)].get("Turn time") - (time() - pause_start_time)
                records[active_player_button_list.index(button)].update({"Turn time" : pause_turn})
            
    def unpause(unpause_button):
        resetButtons()
        total_unpause_count = records[active_player_button_list.index(unpause_button)].get("Unpause count") + 1
        records[active_player_button_list.index(unpause_button)].update({"Unpause count" : total_unpause_count})
        for button in active_player_button_list:
            button.is_paused = False
            button.when_held = pause
            sleep(.1)
            if button.active_player == True:
                button.ledOn()
                button.when_released = nextTurn

    def nextTurn(active_player):
        if active_player.held_down == True:
            active_player.held_down = False
        else:
            active_player.active_player = False

    def resetButtons():
        for button in active_player_button_list:
            button.when_pressed = None
            button.when_held = None
            button.when_released = None
    
    def playerTurn(active_player):

        active_player.active_player = True
        active_player.ledOn()

        player_turn_start_time = time()
        records[active_player_button_list.index(active_player)].update({"Start time" : player_turn_start_time})
        
        active_player.when_released = nextTurn
        for button in active_player_button_list:
            button.when_held = pause

        while active_player.active_player == True:
            sleep(.3)
            
            
        resetButtons()
        active_player.ledOff()
        player_turn_end_time = time()
        records[active_player_button_list.index(active_player)].update({"End time" : player_turn_end_time})
        total_turn_time = (player_turn_end_time - player_turn_start_time) + records[active_player_button_list.index(active_player)].get("Turn time")
        records[active_player_button_list.index(active_player)].update({"Turn time" : total_turn_time})
        ExportData.updateCell(records[(active_player_button_list.index(active_player))], (active_player_button_list.index(active_player)))

    active_player = turn_order_button_list[0]
    playerTurn(active_player)

    while auxillary_button_list[0].round_complete == False:
        if (turn_order_button_list.index(active_player) + 1) == len(turn_order_button_list):
            active_player = turn_order_button_list[0]
            playerTurn(active_player)
        else:
            active_player = turn_order_button_list[turn_order_button_list.index(active_player) + 1]
            playerTurn(active_player)

#SimonSays.simon_says_game()
#WhackAMole.whack_a_mole_game()
#gameTracker()
#sounds()
