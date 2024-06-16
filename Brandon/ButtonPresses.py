import TimerButtons
import random

def press():
	'''Function for the accept button'''
	game_state = TimerButtons.Setup.game_state  # Needs to get the state of the game
	if game_state == 1: # If in setup
		TimerButtons.Setup.game_state = 2 # Move to setting up turn order
	elif game_state == 2: # If in setting up turn order
		def setupTurnOrder():
			'''Will make sure turn order is set up properly'''
			if len(TimerButtons.Setup.turn_order) == len(TimerButtons.Setup.active_list): # Makes sure all players have an order in turn order
				TimerButtons.Setup.game_state = 3	# Moves to game in progress
				TimerButtons.Setup.turn_order[0].is_live = True # Sets the first player button to be active (timer doesn't start until game is going (~3secs)


			'''elif len(TimerButtons.Setup.turn_order) == 0:	#if no buttons are pressed will set a random person to first
				rando = random.randint(0,TimerButtons.Setup.turn_order)
				TimerButtons.Setup.turn_order.append(TimerButtons.Setup.active_list[rando])
				TimerButtons.Setup.turn_order[0].ledOn()'''
			
			
			else:
				for button in TimerButtons.Setup.active_list: # type: ignore
					button.ledOff()
				TimerButtons.Setup.turn_order.clear()
				setupTurnOrder()

	elif TimerButtons.Setup.game_state == 3:
		TimerButtons.Setup.game_state = 4
		TimerButtons.gameEnd()
def hold():
	'''What happens when a button is held for longer than (hold_time)'''
	pass
def release():
	'''What happens when a button is released'''
	game_state = TimerButtons.Setup.game_state
	current_player_list = TimerButtons.Setup.active_list

	#Determine what button was pushed
	
	#player buttons code
	if True:
		match game_state:
			case 1:
				if self in Setup.active_list: #Setup buttons in play
					Setup.active_list.remove(self)
					self.ledOff()
				else:
					Setup.active_list.append(self)
					self.ledOn()
		elif game_state == 2: #Turn Order
			if self.is_live:
				Setup.turn_order.append(self)
				self.ledOn()
				self.is_live = False
		elif game_state == 3:
			if self.is_live:
				self.end_time = time()
				Setup.fuck_this_variable = 1'''
	#other buttons code

	pass
