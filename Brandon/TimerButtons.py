from time import sleep, time
import csv
import random
from gpiozero import Button , LED

##TODO
## I think all hold buttons will have to be worked differntly.  A buttons when_pressed fires instantly when it is pressed. If you were using all 3 (press,release,hold)
## press would always fire first, followed by hold, then release. 

## hold for remove from round for inactive player
## Export to db
## extra button during turn selection selects a random first player(only first time, and other players will have to assign thier places (2nd,3rd...etc))

class SetupAcceptButton(Button):
	def __init__(self,button_pin):
		super().__init__(button_pin, bounce_time = .1)
		self.when_pressed = SetupAcceptButton.press
		self.when_held = SetupAcceptButton.hold
		self.when_released = SetupAcceptButton.release
		self.held = False
		
	def press(self):
		game_state = Setup.game_state
		match game_state:
			case 1:
				Setup.game_state = 2
			case 2:
				if len(Setup.turn_order) == len(Setup.active_list):
					Setup.game_state = 3
					Setup.turn_order[0].is_live = True
				else:
					for button in Setup.active_list:
						button.ledOff()
						Setup.turn_order.clear()
						rando_boi = random.randint(0,len(Setup.active_list)-1)
						Setup.turn_order.append(Setup.active_list[rando_boi])
						Setup.turn_order[0].ledOn()
						print("rando firsty boi")

	def hold(self):
		game_state = Setup.game_state
		match game_state:
			case 3:  #if accept button is held during gameplay it will trigger game end
				self.held = True
				print("the game has ended")
				gameEnd()

	def release(self):
		game_state = Setup.game_state
		match game_state:
			case 3:  #If accept button is pushed during gameplay it will trigger end of round
				if not self.held:
					print("the round has ended")
					Setup.game_state = 5
				else:
					self.held = False

class Setup(Button):
	active_turn = 0
	enter_pause = False
	game_state = 0 #0 = default ---> 1 = setup ---> 2 = turnorder ---> 3 = Game ----> 4 = pause ----> 5 = end of round ---> 6 = cleanup
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
		self.when_pressed = Setup.buttonPress
		self.when_held = Setup.buttonHold
		self.when_released = Setup.buttonRelease
		self.held = False
		self.count = 0

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
					if self.held == True & self.count == 1:
						self.held = False
						self.count = 0
						Setup.enter_pause = False
					elif self.held == True:
						self.count = 1
					else:
						Setup.active_turn = 1

	def addToLists(self):
		Setup.active_list.append(self)
		Setup.button_list.append(self)
	
	def ledOn(self):
		self.led.on()
			
	def ledOff(self):
		self.led.off()
		
	def ledFastBlink(self, count):
		while count != 0:
			self.led.off()
			sleep(.1)
			self.led.on()
			sleep(.25)
			count = count - 1
			
	def ledBlink(self, count):
		while count != 0:
			self.led.off()
			sleep(.3)
			self.led.on()
			sleep(.7)
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
			button.ledFastBlink(Setup.turn_order.index(button)+1)
			button.ledOff()

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
	for button in Setup.active_list:
		button.ledOff()
	Setup.turn_order.clear
	Setup.game_state = 2
	while Setup.game_state == 2:
		sleep(.3)
	gameInProgress()
	
def gameInProgress():
	Setup.cycleTurn()
	for button in Setup.turn_order:
		Setup.time_list.append(0)
		button.ledOff
	playerTurn(Setup.turn_order[0])
	
def playerTurn(button):
	"""This is a full turn
	It will set the button to active turn, turn it's LED on and start a timer.
	It will then wait for a release (for next turn) or hold (for pause)
	It will calculate time and go to next person (removing time for duration paused as needed)"""
	difference_in_pause = 0
	button.is_live = True
	button.ledOn()
	timer_start = time()
	while Setup.active_turn == 0:
		if Setup.enter_pause == True:
			pause_timer_start = time()
			while Setup.enter_pause == True:
				if Setup.game_state == 5:
					turnOrder()
				sleep(.3)
			pause_timer_end = time()
			difference_in_pause = pause_timer_end - pause_timer_start
		if Setup.game_state == 5:
			turnOrder()
		sleep(.3)
	Setup.active_turn = 0
	timer_end = time()
	difference_in_time = timer_end - timer_start - difference_in_pause
	button.ledOff()
	button.is_live = False
	Setup.time_list[Setup.turn_order.index(button)] += difference_in_time
	if Setup.turn_order.index(button) == (len(Setup.turn_order) - 1):
		button = Setup.turn_order[0]
	else:
		button = Setup.turn_order[Setup.turn_order.index(button)+1]
	playerTurn(button)

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
