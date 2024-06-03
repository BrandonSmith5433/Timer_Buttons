from config import BUTTON_LIST, PLAYER_BUTTON_BOARD
from gpiozero import Button, ButtonBoard

class PlayerButton(Button):

    '''Class for player button and LED'''
    #Initialize the class
    def __init__(self, color: str, button_pin: int, led_pin: int):
        super().__init__(
            button_pin,
            hold_time=1,
            bounce_time = 0.1
        )
        self.color = color
        self.led = LED(led_pin)
        self.total_time = 0
        self.running = False
        self.is_disabled = False
        self.is_active_button = False
        self.is_player_turn = False
        self.turn_start_time = None

    #Disable player
    def disable_player(self):
        '''Disables player color and button'''
        if self.is_disabled == False:
            self.is_disabled = True

    #Enable player
    def enable_player(self):
        '''Enables a player color and button'''
        if self.is_disabled == True:
            self.is_disabled = False



