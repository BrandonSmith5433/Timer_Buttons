from gpiozero import Button, LED
from time import sleep, time
from signal import pause
import csv

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

#Global Variables
held = 0
z = 0
start = float(0)
end = float(0)
pauseStart = float(0)
pauseEnd = float(0)


#Startup Sequence
y = 0
while y < 5:
    for x in LEDList:
        x.on()
        sleep(.2)
        x.off()
    y = y + 1

#Will turn on your light for your turn
#Starts a timer
def turn(z):
    global start
    LEDList[z].on()
    start = time()
    #holding the button will flash the lights and start a pause timer to be removed from the main timer
    ButtonList[z].when_held = held_button
    #just pressing the button will calculate the time and add it to your color, It will then reset timers
    ButtonList[z].when_released = release_button
    if z < 3:
        z = z + 1
        turn(z)
    else:
        z = 0
        turn(z)

def release_button():
    global held, z, pauseStart, pauseEnd, start, end
    if held == 0:
        end = time()
        timeList[z] = timeList[z] + (end - start)
        timeList[z] = timeList[z] - (pauseEnd - pauseStart)
        pauseStart = 0
        end = 0
        start = 0
        pauseEnd =0
        LEDList[z].off()
    else:
        held = 0

def held_button():
    global held, z, pauseStart, pauseEnd
    held = 1
    pauseStart = time()
    ButtonList[z].wait_for_press()
    pauseEnd = time()

def next_turn():
    global z
    if z < 3:
        z = z + 1
        turn()
    else:
        z = 0
        turn()

#writes data to CSV at end
def output():
    with open('output.csv', 'w', newline='') as csvfile: 
        writer = csv.writer(csvfile) 
        writer.writerow(['Player Color', 'Total Time'])
        for i in range(len(ButtonList)): 
            writer.writerow([ButtonList[i], timeList[i]])

#waits for white to be pressed     
ButtonList[4].when_pressed = output()
#the start of it all
turn()