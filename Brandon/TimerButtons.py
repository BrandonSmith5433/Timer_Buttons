from time import sleep, time
import csv
from gpiozero import Button , LED

##TODO
## I think all hold buttons will have to be worked differntly.  A buttons when_pressed fires instantly when it is pressed. If you were using all 3 (press,release,hold)
## press would always fire first, followed by hold, then release. 

## Hold for Pause as active player, hold for remove from round for inactive player
## extra button ends round -- extra button hold ends game
## end of round requires turn order to be chosen again
## Export multiple csv files
## extra button during turn selection selects a random first player(only first time, and other players will have to assign thier places (2nd,3rd...etc))

## probably work on changing names fo things so it's more readable
## Maybe move the button presses to another file

class SetupAcceptButton(Button):
	def __init__(self,button_pin):
		super().__init__(button_pin, bounce_time = .1)
		self.when_pressed = SetupAcceptButton.acceptButtonPressed
		self.when_held = SetupAcceptButton.acceptButtonHeld
		self.when_released = SetupAcceptButton.acceptButtonReleased
		self.accept_button_held = False
		
	def acceptButtonPressed(self):
		game_state = Setup.game_state
		if game_state == 1:
			Setup.game_state = 2
		elif game_state == 2:
			print(len(Setup.turn_order))
			print(len(Setup.active_list))
			if len(Setup.turn_order) == len(Setup.active_list):
				Setup.game_state = 3
				Setup.turn_order[0].is_live = True
			else:
				for button in active_list: # type: ignore
					button.ledOff()
					Setup.turn_order.clear()
		elif game_state == 3:
			Setup.game_state = 4
			gameEnd()
	
	def acceptButtonHeld(self):
		self.accept_button_held = True

	def acceptButtonReleased(self):
		if self.accept_button_held:
			self.accept_button_held = False
		else:
			pass #everything else on release --- probably all that button press shit

class Setup(Button):
	active_turn = 0
	enter_pause = False
	game_state = 0 #0 = default ---> 1 = setup ---> 2 = turnorder ---> 3 = Game ----> 4 = End of round ----> 5 = pause ---> 6 = cleanup
	button_list = []
	active_list = []
	turn_order = []
	time_list = []
	
	def __init__(self, color, button_pin, led_pin):
		super().__init__(button_pin, bounce_time = .1)
		self.is_live = True
		self.led = LED(led_pin)
		self.led.off()
		Setup.addToLists(self)
		self.color = color
		self.start_time = time()
		self.end_time = time()
		self.when_pressed = buttonPress
		self.when_held = buttonHold
		self.when_released = buttonRelease
		self.held = False

	def buttonPress(self):
		'''What is done when a colored button is pressed'''
		game_state = Setup.game_state
		match game_state:
			case 1: # Sets current players 
				if self in Setup.active_list:
					Setup.active_list.remove(self)
					self.ledOff()
				else:
					Setup.active_list.append(self)
					self.ledOn()

			case 2: # Determines turn order
				if self.is_live:
					Setup.turn_order.append(self)
					self.ledOn()
					self.is_live = False
				else:
					Setup.turn_order.remove(self)
					self.ledOff()
					self.is_live = True

	def buttonHold(self):
		'''What is done when a colored button is held'''
		game_state = Setup.game_state
		match game_state:
			case 3: #Active gameplay
				if self.is_live:
					self.held = True
					Setup.enter_pause = True

	def buttonRelease(self):
		'''What is done when a colored button is released'''
		game_state = Setup.game_state
		match game_state:
			case 3: #Active gameplay
				if self.is_live:
					if self.held == True & count == 1:
						self.held = False
						count = 0
					elif self.held == True:
						count = 1
					else:
						Setup.active_turn = 1

	def addToLists(self):
		Setup.active_list.append(self)
		Setup.button_list.append(self)
	
	def ledOn(self):
		self.led.on()
			
	def ledOff(self):
		self.led.off()
	
	def ledBlink(self, count):
		while count != 0:
			self.led.on()
			sleep(1)
			self.led.off()
			sleep(1)
			count = count - 1
		
	def cycleAll(count):
		while count !=0:
			for button in Setup.button_list:
				button.ledOn()
				sleep(.04)
				button.ledOff()
				sleep(.04)
			count = count - 1
	
	def cycleActive(count): #Players determined in first phase
		while count !=0:
			for button in Setup.active_list:
				button.led.on()
				sleep(.04)
				button.led.off()
				sleep(.04)
			count = count - 1
	
	def flashAll(count):
		while count !=0:
			for button in Setup.button_list:
				button.led.on()
			sleep(.2)
			for button in Setup.button_list:
				button.led.off()
			sleep(.2)
			count = count - 1

	def flashActive(count):
		while count !=0:
			for button in Setup.active_list:
				button.led.on()
			sleep(.2)
			for button in Setup.active_list:
				button.led.off()
			sleep(.2)
			count = count - 1
			
	def cycleTurn():
		for button in Setup.turn_order:
			button.ledBlink(Setup.turn_order.index(button))

def gameSetup():
	Setup.game_state = 1
	Setup.cycleAll(5)
	Setup.flashAll(5)
	for button in Setup.button_list:
		button.ledOn()
	while Setup.game_state == 1:
		sleep(.3)
	turnOrder()
	
def turnOrder():
	Setup.cycleActive(10)
	while Setup.game_state == 2:
		sleep(.3)
	gameInProgress()
	
def gameInProgress():
	Setup.cycleTurn()
	for button in Setup.turn_order:
		Setup.time_list.append(0)
	turn(Setup.turn_order[0])
	
def turn(button):
	button.is_live = True
	button.ledOn()
	button.start_time = time()
	while Setup.active_turn == 0:
		if Setup.enter_pause == True:
			pause_start = time()
			while Setup.enter_pause == True:
				sleep(.3)
			pause_end = time()
			pause_difference = pause_end - pause_start
		sleep(.3)
	Setup.active_turn = 0
	button.end_time = time()
	time_difference = button.end_time - button.start_time - pause_difference
	button.ledOff()
	button.is_live = False
	Setup.time_list[Setup.turn_order.index(button)] += time_difference
	if Setup.turn_order.index(button) == (len(Setup.turn_order) - 1):
		button = Setup.turn_order[0]
	else:
		button = Setup.turn_order[Setup.turn_order.index(button)+1]
	turn(button)

def gameEnd():
	with open('testcsv.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['player Color', 'Total Time'])
		for i in range(len(Setup.turn_order)):
			writer.writerow([Setup.turn_order[i].color, Setup.time_list[i]])
	exit()

#Buttons setup
#No need to fuck with, anything else can be changed in Setup class
accept_button = SetupAcceptButton(25)
white_button = Setup("White", 27, 17)
green_button = Setup("Green", 23, 24)
red_button = Setup("Red", 6, 5)
yellow_button = Setup("Yellow", 21, 20)
blue_button = Setup("Blue", 19, 26)
gameSetup()