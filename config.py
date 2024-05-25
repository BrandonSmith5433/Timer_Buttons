from buttons import PlayerButton, AcceptButton
from gpiozero import Device, LEDBoard
from gpiozero.pins.mock import MockFactory


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
ACCEPT_BTN_PIN = 0

LED_BOARD = LEDBoard(
    white=17,
    green=24,
    red=5,
    yellow=20,
    blue=26
)

BUTTON_MAP = {
    WHITE_BTN_PIN: PlayerButton(
        color='white',
        button_pin=WHITE_BTN_PIN,
        led_pin=WHITE_BTN_LED,
    ),
    GREEN_BTN_PIN: PlayerButton(
        color='green',
        button_pin=GREEN_BTN_PIN,
        led_pin=GREEN_BTN_LED,
    ),
    RED_BTN_PIN: PlayerButton(
        color='red',
        button_pin=RED_BTN_PIN,
        led_pin=RED_BTN_LED,
    ),
    YELLOW_BTN_PIN: PlayerButton(
        color='yellow',
        button_pin=YELLOW_BTN_PIN,
        led_pin=YELLOW_BTN_LED,
    ),
    BLUE_BTN_PIN: PlayerButton(
        color='blue',
        button_pin=BLUE_BTN_PIN,
        led_pin=BLUE_BTN_LED,
    ),
}

ACCEPT_BUTTON = AcceptButton(
    button_pin=ACCEPT_BTN_PIN,
)