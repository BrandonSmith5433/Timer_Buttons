from setup import PlayerButton
from time import sleep, time
from signal import pause
from gpiozero import Button , LED

class SetupAcceptButton(Button):
	def __init__(self,button_pin):
		super().__init__(button_pin, bounce_time = .1)
		
	def acceptButtonPressed(self):
		game_state = Setup.game_state
		if game_state == 1:
			turnOrder()
		elif game_state == 2:
			if len(Setup.turnOrder) == len(Setup.active_list):
				self.is_active = True
				gameInProgress()
			else:
				turnOrder()
		elif game_state == 3:
			pass
		elif game_state == 4:
			pass
	
class Setup(Button):
	'''Class for setting up the buttons'''
	
	game_state = 0 #0 = default ---> 1 = setup ---> 2 = turnorder ---> 3 = Game ----> 4 = Cleanup
	button_list = []
	active_list = []
	turn_order = []
	time_list = []
	
	def __init__(self, color, button_pin, led_pin):
		super().__init__(button_pin, bounce_time = .1)
		self.is_active = False
		self.led = LED(led_pin)
		self.is_disabled = False
		self.led.off()
		Setup.addToList(self)
		Setup.addToActive(self)
		self.color = color
		self.start_time = time()
		self.end_time = time()

	def turnOrderPressed(button):
		if button.is_disabled == False:
			Setup.turn_order.append(button)
			button.ledOn()
			button.is_disabled = True


	def buttonPressed(self):
		game_state = Setup.game_state
		if game_state == 1:
			if button in Setup.active_list:
				Setup.active_list.remove(button)
				button.ledOff()
			else:
				Setup.active_list.append(button)
				button.ledOn()
				
		elif game_state == 2:
			if button.is_disabled == False:
				Setup.turn_order.append(button)
				button.ledOn()
				button.is_disabled = True
				
		elif game_state == 3:
			if button.is_active:
				moveToNextButton(self)
		
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
			sleep(.3)
			self.led.off()
			sleep(.3)
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
				sleep(.1)
				button.led.off()
				sleep(.1)
			count = count - 1
	
	def cycleActive(count):
		'''Cycles through each light to be used in the current game turning them on and off *count* times'''
		while count !=0:
			for button in Setup.active_list:
				button.led.on()
				sleep(.1)
				button.led.off()
				sleep(.1)
			count = count - 1
			
	def flashAll(count):
		'''Blinks all lights on and off'''
		while count !=0:
			for button in Setup.button_list:
				button.led.on()
			sleep(1)
			for button in Setup.button_list:
				button.led.off()
			sleep(1)
			count = count - 1
			
	def flashActive(count):
		'''Blinks all lights in current game on and off'''
		while count !=0:
			for button in Setup.active_list:
				button.led.on()
			sleep(1)
			for button in Setup.active_list:
				button.led.off()
			sleep(1)
			count = count - 1
			
	def cycleTurn(self):
		for button in Setup.turn_order:
			button.ledBlink(self, Setup.turn_order.index(button))


'''Create the button objects'''
accept_button = SetupAcceptButton(25)
white_button = Setup("White", 27, 17)
green_button = Setup("Green", 23, 24)
red_button = Setup("Green", 6, 5)
yellow_button = Setup("Green", 21, 20)
blue_button = Setup("Blue", 19, 26)

'''Setup what to do when a button is pressed'''
for button in Setup.active_list:
	button.when_pressed = Setup.buttonPressed
accept_button.when_pressed = SetupAcceptButton.acceptButtonPressed

def gameSetup():
	'''Setup the players in the game'''
	print("Starting setup")
	
	Setup.game_state = 1
	Setup.cycleAll(2)
	Setup.flashAll(2)
	for button in Setup.button_list:
		button.ledOn()
	pause()

def turnOrder():
	'''Determine Turn Order'''
	print("Starting Turn Order")
	Setup.game_state = 2
	for button in Setup.active_list:
		button.ledOff()
	Setup.cycleActive(10)
	pause()
	
def gameInProgress():
	'''Game in progress'''
	Setup.game_state = 3
	Setup.cycleTurn()
	print("Starting Game")

	'''Make the time_list'''
	length = 0
	while length < len(Setup.turn_order):
		Setup.time_list.append(time())

	for button in Setup.turn_order:
		if button.is_active:
			turn(button)

def turn(button):
	button.start_time = time()
	pause
	button.end_time = time()
	button.is_active = False
	Setup.time_list[Setup.turn_order.index(button)] += (button.end_time - button.start_time)
	if Setup.turn_order.index(button) == (len(Setup.turn_order) - 1):
		button = Setup.turn_order[0]
	else:
		button = Setup.turn_order[Setup.turn_order.index(button)+1]
	button.is_active = True
	turn(button)

def gameEnd():
	#output data
	pass

gameSetup()