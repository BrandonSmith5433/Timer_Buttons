from time import sleep
from functools import wraps

from gpiozero import Button, LED



class PlayerButton():
    '''Class for player button and LED'''

    def __init__(self, color: str, button_pin: int, led_pin: int):
        super().__init__(
            button_pin=button_pin,
            hold_time=2,
        )
        self.color = color
        self.led = LED(led_pin)
        self.total_time = 0
        self.is_player_turn = False

    def led_on(self):
        '''Turns button LED on'''
        self.led.on()

    def led_off(self):
        '''Turns button LED off'''
        self.led.off()

    def led_flash(self, flashes: int, delay: float = 0.05):
        '''Flashes LED a number of times'''
        for i in range(flashes):
            self.led_on()
            sleep(delay)
            self.led_off()
            sleep(delay)
    
    def toggle_player_turn(self):
        self.is_player_turn = not self.is_player_turn
        while self.is_player_turn:
            sleep(1)
            self.total_time += 1



class AcceptButton(Button):
    '''Class for the accept button'''

    def __init__(self, button_pin: int):
        super().__init__(button_pin)