from setup import PlayerButton
from time import sleep, time
from signal import pause
from gpiozero import Button
class SetupAcceptButton(Button):
	def __init__(self,button_pin):
		super().__init__(button_pin, bounce_time = .1)
		
	def acceptButtonPressed():
		game_state = Setup.game_state
		if game_state == 1:
			turnOrder()
		elif game_state == 2:
			pass
		elif game_state == 3:
			pass
		elif game_state == 4:
			pass
	
class Setup(PlayerButton):
	
	game_state = 0 # 1 = setup, 2 = turnorder 3 = Game 4 = Cleanup
	button_list = []
	active_list = []
	turn_order = []
	time_list = []
	
	def __init__(self, color, button_pin, led_pin):
		super().__init__(color, button_pin,led_pin)
		self.is_disabled = False
		self.led.off()
		Setup.addToList(self)
		Setup.addToActive(self)
		self.color = color
		self.start_time = time()
		self.end_time = time()
		
	def buttonPressed(self):
		game_state = Setup.game_state
		if game_state == 1:
			pass
		elif game_state == 2:
			pass
		elif game_state == 3:
			pass
		elif game_state == 4:
			pass
	
			
	
	def addToActive(self):
		Setup.active_list.append(self)
		
	def addToList(self):
		Setup.button_list.append(self)
	
	def ledOn(self):
		if not self.is_disabled:
			self.led.on()
			
	def ledOff(self):
		if not self.is_disabled:
			self.led.off()
	
	def enableButton(self):
		if self.is_disabled == True:
			self.is_disabled = False
			
	def disableButton(self):
		if self.is_disabled == False:
			self.is_disabled = True
			
	def cycleAll(count):
		while count !=0:
			for button in Setup.button_list:
				button.led.on()
				sleep(.1)
				button.led.off()
				sleep(.1)
			count = count - 1
	
	def cycleActive(count):
		while count !=0:
			for button in Setup.active_list:
				button.led.on()
				sleep(.1)
				button.led.off()
				sleep(.1)
			count = count - 1
			
	def flashAll(count):
		while count !=0:
			for button in Setup.button_list:
				button.led.on()
			sleep(1)
			for button in Setup.button_list:
				button.led.off()
			sleep(1)
			count = count - 1
			
	def flashActive(count):
		while count !=0:
			for button in Setup.active_list:
				button.led.on()
			sleep(1)
			for button in Setup.active_list:
				button.led.off()
			sleep(1)
			count = count - 1
			
	def cycleTurn():
		pass
		#todo, flash first person 1 time then 2nd player 2 times, etc


#Create the button objects
accept_button = SetupAcceptButton(25)
white_button = Setup("White", 27, 17)
green_button = Setup("Green", 23, 24)
red_button = Setup("Green", 6, 5)
yellow_button = Setup("Green", 21, 20)
blue_button = Setup("Blue", 19, 26)
for button in Setup.active_list:
	button.when_pressed = Setup.buttonPressed
accept_button.when_pressed = SetupAcceptButton.acceptButtonPressed
print(accept_button)

#Setup.cycleAll(2)
#Setup.cycleActive(2)
#Setup.flashAll(3)
#Setup.flashActive(3)

def gameSetup():
	'''Setup the players in the game'''
	print("Starting setup")
	def setupPressed(button):
		if button in Setup.active_list:
			Setup.active_list.remove(button)
			button.ledOff()
		else:
			Setup.active_list.append(button)
			button.ledOn()
			print(Setup.active_list)
	Setup.cycleAll(2)
	for button in Setup.button_list:
		button.ledOn()
	accept_button.when_pressed = acceptSetupPressed
	pause()
	
	#TODO -- accept button to accept current players - will then move
	#to turnOrder function

def turnOrder():
	print("Starting Turn Order")
	def turnOrderPressed(button):
		if button.is_disabled == False:
			Setup.turn_order.append(button)
			button.ledOn()
			button.is_disabled = True
	for button in Setup.active_list:
		button.ledOff()
		button.when_pressed = turnOrderPressed
	def acceptTurnOrderPressed():
		print(started)
		if len(Setup.turnOrder) == len(Setup.active_list):
			gameInProgress()
		else:
			turnOrder()
	accept_button.when_pressed = acceptTurnOrderPressed
	Setup.cycleActive(10)
	pause()
	#TODO accept button when pressed to accept turn order and move into 
	#gameInProgress
	
def gameInProgress():
	global counter
	counter = 0
	print("Starting Game")
	def gameInProgressPressed(button):
		global counter
		sleep(.1)
		button.ledOff()
		button.end_time = time()
		Setup.time_list[counter] += (button.end_time - button.start_time)
		if (counter + 2) > len(Setup.turn_order):
			counter = 0
		else:
			counter += 1
		activeButton(Setup.turn_order[counter])
		
		
	def activeButton(button):
		button.is_disabled = False
		button.ledOn()
		button.start_time = time()
		print(button)
		button.wait_for_press()
		gameInProgressPressed(button)

		
	
	for button in Setup.turn_order:
		button.ledOff()
		button.is_disabled = True
		Setup.time_list.append(0)

		
	Setup.cycleTurn()
	activeButton(Setup.turn_order[counter])

		
	
	def gamePaused():
		pass
		
		
	pause()

def gameEnd():
	#output data
	pass

Setup.turn_order.append(green_button)
Setup.turn_order.append(blue_button)

gameSetup()
