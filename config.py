from buttons import PlayerButton, AcceptButton, PlayerButtonBoard

# White button
WHITE_BTN_PIN = 27
WHITE_BTN_LED = 17

# Green button
GREEN_BTN_PIN = 23
GREEN_BTN_LED = 24

# Red button
RED_BTN_PIN = 6
RED_BTN_LED = 5

# Yellow button
YELLOW_BTN_PIN = 21
YELLOW_BTN_LED = 20

# Blue button
BLUE_BTN_PIN = 19
BLUE_BTN_LED = 26

# Accept button
ACCEPT_BTN_PIN = 25

BUTTON_LIST = [
    PlayerButton(
        color='white',
        button_pin=WHITE_BTN_PIN,
        led_pin=WHITE_BTN_LED,
    ),
    PlayerButton(
        color='green',
        button_pin=GREEN_BTN_PIN,
        led_pin=GREEN_BTN_LED,
    ),
    PlayerButton(
        color='red',
        button_pin=RED_BTN_PIN,
        led_pin=RED_BTN_LED,
    ),
    PlayerButton(
        color='yellow',
        button_pin=YELLOW_BTN_PIN,
        led_pin=YELLOW_BTN_LED,
    ),
    PlayerButton(
        color='blue',
        button_pin=BLUE_BTN_PIN,
        led_pin=BLUE_BTN_LED,
    ),
]

ACCEPT_BUTTON = AcceptButton(
    button_pin=ACCEPT_BTN_PIN,
)

PLAYER_BUTTON_BOARD = PlayerButtonBoard(buttons=BUTTON_LIST)