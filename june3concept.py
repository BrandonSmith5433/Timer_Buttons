from gpiozero import Button, LED
from signal import pause
from time import sleep, timer

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

while y < 7:
    for x in LEDList:
        x.on()
        sleep(.2)
        x.off()
    y = y + 1     

for x in LEDList:
    x.was_held = False

z = 0
active_player = ButtonList[z]

def press(z: int):
    if not ButtonList[z].was_held:
        timeList[z] = timeList[z] + (end - start)
        timeList[z] = timeList[z] - (pauseEnd - pauseStart)
        reset_timers()
        LEDList[z].off()
        next_turn(z)
    ButtonList[z].was_held = False

def held(z: int):
    ButtonList[z].was_held = True
    pauseStart = timer()
    ButtonList[z].wait_for_press()
    pauseEnd = timer()

def next_turn(z: int):
    if z < 3:
        z = z + 1
        turn(z)
    else:
        z = 0
        turn(z)

def turn(z: int):
    while z != 4:
        LEDList[z].on()
        start = timer()
        ButtonList[z].wait_for_press()
        ButtonList[z].when_held = held()
        ButtonList[z].when_released = press()
        
def reset_timers():
    start = 0
    end = 0
    pauseStart = 0
    pauseEnd = 0

