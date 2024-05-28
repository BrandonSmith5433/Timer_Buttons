from gpiozero import LED
from gpiozero import Button
from gpiozero import LEDBoard
from time import sleep
from signal import pause


# This code should be the start of the program, will cycle through lights at .3s intervals
# need to figure out an intro and outro to the loop
# allLED = LEDBoard(17,24,5,20,26)
# 
#for led in allLED:
#    led.on()
#    sleep(.3)
#    led.off()


whiteButton = Button(27)
whiteLED = LED(17)

greenButton = Button(23)
greenLED = LED(24)

redButton = Button(6)
redLED = LED(5)

yellowButton = Button(21)
yellowLED = LED(20)

blueButton = Button(19, bounce_time = .1)
blueLED = LED(26)

x = 0

while x < 2:

    x+=1

whiteLED.on()
whiteButton.wait_for_press()
whiteLED.off()

yellowLED.on()
yellowButton.wait_for_press()
yellowLED.off()

redLED.on()
redButton.wait_for_press()
redLED.off()

greenLED.on()
greenButton.wait_for_press()
greenLED.off()

blueLED.on()
blueButton.wait_for_press()
blueLED.off()


#heres a solution to all the problems I was having -- who knows if it's good but it works
#need to add bounce_time to the button. I just did blue here and .1 seems to work.

holdVar = 0

def held():
    global holdVar
    holdVar = 1
    #put code for light here

def release():
    global holdVar
    if holdVar == 0:
        pressed()
    holdVar = 0
    #code here

def pressed():
    blueLED.on()
    #code here

blueButton.when_held = held
blueButton.when_released = release

pause()