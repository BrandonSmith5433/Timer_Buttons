from time import sleep, time
from signal import pause
import csv
from gpiozero import Button , LED

class SetupAcceptButton(Button):
	def __init__(self,button_pin):
		super().__init__(button_pin, bounce_time = .1)
		self.when_pressed = SetupAcceptButton.acceptButtonPressed

	def acceptButtonPressed(self):
		print(self)
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
				for button in active_list:
					button.ledOff()
					Setup.turn_order.clear()
		elif game_state == 3:
			Setup.game_state = 4
			gameEnd()
		elif game_state == 4:
			pass
	
class Setup(Button):
	'''Class for setting up the buttons'''
	fuck_this_variable = 0
	game_state = 0 #0 = default ---> 1 = setup ---> 2 = turnorder ---> 3 = Game ----> 4 = Cleanup
	button_list = []
	active_list = []
	turn_order = []
	time_list = []
	
	def __init__(self, color, button_pin, led_pin):
		super().__init__(button_pin, bounce_time = .1)
		self.is_live = False
		self.led = LED(led_pin)
		self.is_disabled = False
		self.led.off()
		Setup.addToList(self)
		Setup.addToActive(self)
		self.color = color
		self.start_time = time()
		self.end_time = time()
		self.when_pressed = Setup.buttonPressed

	def buttonPressed(self):
		game_state = Setup.game_state
		print(self)
		if game_state == 1:
			if self in Setup.active_list:
				Setup.active_list.remove(self)
				self.ledOff()
			else:
				Setup.active_list.append(self)
				self.ledOn()
				
		elif game_state == 2:
			print(self)
			Setup.turn_order.append(self)
			self.ledOn()
				
		elif game_state == 3:
			if self.is_live:
				print(" im live")
				self.end_time = time()
				Setup.fuck_this_variable = 1
		
	def addToActive(self):
		'''Adds button to list of active buttons for a game'''
		Setup.active_list.append(self)
		
	def addToList(self):
		'''Adds button to list of player buttons'''
		Setup.button_list.append(self)
	
	def ledOn(self):
		'''Turns LED on'''
		if not self.is_disabled:
			self.led.on()
			
	def ledOff(self):
		'''Turns LED off'''
		if not self.is_disabled:
			self.led.off()
	
	def ledBlink(self, count):
		'''Blinks LED'''
		while count != 0:
			self.led.on()
			sleep(.15)
			self.led.off()
			sleep(.15)
			count = count - 1
		
	def enableButton(self):
		'''Enables button'''
		if self.is_disabled == True:
			self.is_disabled = False
			
	def disableButton(self):
		'''Disables button'''
		if self.is_disabled == False:
			self.is_disabled = True
		
	def cycleAll(count):
		'''Cycles through each light turning them on and off *count* times'''
		while count !=0:
			for button in Setup.button_list:
				button.led.on()
				sleep(.04)
				button.led.off()
				sleep(.04)
			count = count - 1
	
	def cycleActive(count):
		'''Cycles through each light to be used in the current game turning them on and off *count* times'''
		while count !=0:
			for button in Setup.active_list:
				button.led.on()
				sleep(.04)
				button.led.off()
				sleep(.04)
			count = count - 1
			
	def flashAll(count):
		'''Blinks all lights on and off'''
		while count !=0:
			for button in Setup.button_list:
				button.led.on()
			sleep(.2)
			for button in Setup.button_list:
				button.led.off()
			sleep(.2)
			count = count - 1
			
	def flashActive(count):
		'''Blinks all lights in current game on and off'''
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


'''Create the button objects'''
accept_button = SetupAcceptButton(25)
white_button = Setup("White", 27, 17)
green_button = Setup("Green", 23, 24)
red_button = Setup("Red", 6, 5)
yellow_button = Setup("Yellow", 21, 20)
blue_button = Setup("Blue", 19, 26)

def gameSetup():
	'''Setup the players in the game'''
	print("Starting setup")
	Setup.game_state = 1
	Setup.cycleAll(2)
	Setup.flashAll(2)
	for button in Setup.button_list:
		button.ledOn()
	while Setup.game_state == 1:
		sleep(.3)
	turnOrder()
	
def turnOrder():
	'''Determine Turn Order'''
	print("Starting Turn Order")
	Setup.cycleActive(10)
	while Setup.game_state == 2:
		sleep(.3)
	gameInProgress()
	
def gameInProgress():
	'''Game in progress'''
	Setup.cycleTurn()
	print("Starting Game")

	'''Make the time_list'''
	length = 0
	while length < len(Setup.turn_order):
		Setup.time_list.append(0)
		length += 1
	print("test1")
	turn(Setup.turn_order[0])
	gameEnd()
	
def turn(button):
	print("test2")
	button.start_time = time()
	print(button.start_time)
	while Setup.fuck_this_variable == 0:
		sleep(.3)
	Setup.fuck_this_variable = 0
	button.end_time = time()
	print(button.end_time)
	time_difference = button.end_time - button.start_time
	print(time_difference)
	button.ledOff()
	button.is_live = False
	Setup.time_list[Setup.turn_order.index(button)] += time_difference
	if Setup.turn_order.index(button) == (len(Setup.turn_order) - 1):
		button = Setup.turn_order[0]
	else:
		button = Setup.turn_order[Setup.turn_order.index(button)+1]
	button.is_live = True
	button.ledOn()
	turn(button)

def gameEnd():
	print("here")
	if Setup.game_state == 4:
		with open('testcsv.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(['player Color', 'Total Time'])
			for i in range(len(Setup.turn_order)):
				writer.writerow([Setup.turn_order[i].color, Setup.time_list[i]])
	exit()
	

gameSetup()
