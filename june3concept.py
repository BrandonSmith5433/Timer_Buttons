from gpiozero import Button, LED
from signal import pause
from time import wait




whiteButton = Button(27, bounce_time=.1, hold_time = 1)
whiteLED = LED(17)

greenButton = Button(23, bounce_time=.1, hold_time = 1)
greenLED = LED(24)

redButton = Button(6, bounce_time=.1, hold_time = 1)
redLED = LED(6)

yellowButton = Button(21, bounce_time=.1, hold_time = 1)
yellowLED = LED(20)

blueButton = Button(19, bounce_time=.1, hold_time = 1)
blueLED = LED(26)

ButtonList = [greenButton, redButton, yellowButton, blueButton]
LEDList = [greenLED, redLED, yellowLED, blueLED]


for x in LEDList:
    x.on
    wait(3)
    x.off
    

pause()