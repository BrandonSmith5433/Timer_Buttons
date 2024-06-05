from setup import PlayerButton, AcceptButton


player_button_list = [
    PlayerButton(
        color = "White",
        button_pin = 27,
        led_pin = 17,
    ),
    PlayerButton(
        color = "Green",
        button_pin = 23,
        led_pin = 24,
    ),
    PlayerButton(
        color = "Red",
        button_pin = 6,
        led_pin = 5,
    ),
    PlayerButton(
        color = "Yellow",
        button_pin = 21,
        led_pin = 20,
    ),
    PlayerButton(
        color = "Blue",
        button_pin = 19,
        led_pin = 26,
    )
]           

accept_button = AcceptButton(button_pin = 25)

## Stuff

#whiteButton = Button(27, bounce_time=.1, hold_time = 1)
#whiteLED = LED(17)

#greenButton = Button(23, bounce_time=.1, hold_time = 1)
#greenLED = LED(24)

#redButton = Button(6, bounce_time=.1, hold_time = 1)
#redLED = LED(5)

#yellowButton = Button(21, bounce_time=.1, hold_time = 1)
#yellowLED = LED(20)

#blueButton = Button(19, bounce_time=.1, hold_time = 1)
#blueLED = LED(26)