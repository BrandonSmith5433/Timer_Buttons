from gpiozero import Button, LED
from signal import pause
from time import sleep, time

whiteButton = Button(27, bounce_time=.1, hold_time = 1)
whiteLED = LED(17)

greenButton = Button(23, bounce_time=.1, hold_time = 1)
greenLED = LED(24)

redButton = Button(6, bounce_time=.1, hold_time = 1)
redLED = LED(5)

yellowButton = Button(21, bounce_time=.1, hold_time = 1)
yellowLED = LED(20)

blueButton = Button(19, bounce_time=.1, hold_time = 1)
blueLED = LED(26)

ButtonList = [greenButton, redButton, yellowButton, blueButton]
timeList = [0,0,0,0]
LEDList = [greenLED, redLED, yellowLED, blueLED]

start, = 0
end = 0
pauseStart = 0
pauseEnd = 0
y = 0
z = 0
held = 0

while y < 7:
    for x in LEDList:
        x.on()
        sleep(.2)
        x.off()
    y = y + 1     

def press_button(z, held):
    if held == 0:
        end = time()
        timeList[z] = timeList[z] + (end - start)
        timeList[z] = timeList[z] - (pauseEnd - pauseStart)
        reset_timers()
        LEDList[z].off()
        next_turn(z)
    else:
        held = 0

def held_button(z):
    held = 1
    pauseStart = time()
    ButtonList[z].wait_for_press()
    pauseEnd = time()

def next_turn(z):
    if z < 3:
        z = z + 1
        turn(z)
    else:
        z = 0
        turn(z)

def turn(z):
    while z != 4:
        LEDList[z].on()
        start = time()
        ButtonList[z].wait_for_press()
        ButtonList[z].when_held = held_button(z)
        ButtonList[z].when_released = press_button(z, held)
        
def reset_timers():
    start = 0
    end = 0
    pauseStart = 0
    pauseEnd = 0

def output():
    pass
