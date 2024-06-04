'''from time import sleep, time
from signal import pause
import csv
import Brandon.setup as setup 

#class PlayerButton():
    def __init__(self)
        
#timeList = [float(0),float(0),float(0),float(0),float(0),]


#Global Variables
setup_state = 0 # 0 will start a setup, 1 will go straight to turn
held = 0 # variable needed so that when_held and when_released aren't both activated
z = 0 # list iterator
start = float(0) # Timer start when player is active.
end = float(0) # Timer ends when player is inactive
pauseStart = float(0) #Timer starts when paused
pauseEnd = float(0) #Timer ends when unpaused


#Startup Sequence - flashes through LED's in order y times
y = 5
while y > 0:
    for x in LEDList:
        x.on()
        sleep(.2)
        x.off()
    y = y - 1

def turn():
    global z
    global start
    LEDList[z].on()
    start = time()
    #holding the button will flash the lights and start a pause timer to be removed from the main timer
    ButtonList[z].when_held = held_button
    #just pressing the button will calculate the time and add it to your color, It will then reset timers
    ButtonList[z].when_released = release_button

def next_turn():
    if z < 3:
        z = z + 1
        turn()
    else:
        z = 0
        turn()

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
        next_turn()
    else:
        held = 0

def held_button():
    global held, z, pauseStart, pauseEnd
    held = 1
    pauseStart = time()
    sleep(2)
    ButtonList[z].wait_for_press()
    sleep(2)
    held = 1 #needed a 2nd time due to release activiating on first and 2nd push
    pauseEnd = time()

#writes data to CSV at end
def output():
    with open('output.csv', 'w', newline='') as csvfile: 
        writer = csv.writer(csvfile) 
        writer.writerow(['Player Color', 'Total Time'])
        for i in range(len(ButtonList)): 
            writer.writerow([ButtonList[i], timeList[i]])

#waits for white to be pressed     
whiteButton.when_pressed = output()
#the start of it all
turn()
pause()'''