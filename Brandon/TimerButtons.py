from time import sleep, time
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
				for button in active_list: # type: ignore
					button.ledOff()
					Setup.turn_order.clear()
		elif game_state == 3:
			Setup.game_state = 4
			gameEnd()
	
class Setup(Button):
	fuck_this_variable = 0
	game_state = 0 #0 = default ---> 1 = setup ---> 2 = turnorder ---> 3 = Game ----> 4 = Cleanup
	button_list, active_list, turn_order, time_list = []

	def __init__(self, color, button_pin, led_pin):
		super().__init__(button_pin, bounce_time = .1)
		self.is_live = True
		self.led = LED(led_pin)
		self.led.off()
		Setup.addToList(self)
		Setup.addToActive(self)
		self.color = color
		self.start_time = time()
		self.end_time = time()
		self.when_pressed = Setup.buttonPressed

	def buttonPressed(self):
		game_state = Setup.game_state
		if game_state == 1:
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
				Setup.fuck_this_variable = 1
		
	def addToActive(self):
		Setup.active_list.append(self)
		
	def addToList(self):
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
				button.led.on()
				sleep(.04)
				button.led.off()
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
	while Setup.fuck_this_variable == 0:
		sleep(.3)
	Setup.fuck_this_variable = 0
	button.end_time = time()
	time_difference = button.end_time - button.start_time
	print(time_difference)
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

accept_button = SetupAcceptButton(25)
white_button = Setup("White", 27, 17)
green_button = Setup("Green", 23, 24)
red_button = Setup("Red", 6, 5)
yellow_button = Setup("Yellow", 21, 20)
blue_button = Setup("Blue", 19, 26)
gameSetup()