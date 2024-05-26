from time import sleep
from typing import List

from gpiozero import Button, LED

class PlayerButton(Button):
    '''Class for player button and LED'''

    def __init__(self, color: str, button_pin: int, led_pin: int):
        super().__init__(
            button_pin,
            hold_time=2,
            bounce_time = 0.1
        )
        self.color = color
        self.led = LED(led_pin)
        self.total_time = 0
        self.running = False
        self.is_disabled = False
        self.is_active_button = False
        self.is_player_turn = False

    def disabled_toggle(self):
        '''Toggles disabled state'''
        self.is_disabled = not self.is_disabled

    def active_button_toggle(self):
        '''Toggles active state'''
        self.is_active_button = not self.is_active_button

    def player_turn_toggle(self):
        '''Toggles player turn state'''
        if not self.is_disabled:
            self.is_player_turn = not self.is_player_turn
            while self.is_player_turn:
                sleep(1)
                self.total_time += 1

    def led_on(self):
        '''Turns button LED on'''
        if not self.is_disabled:
            self.led.on()

    def led_off(self):
        '''Turns button LED off'''
        if not self.is_disabled:
            self.led.off()

    def led_toggle(self):
        '''Toggles button LED state'''
        self.led.toggle()

    def led_flash(self, flashes: int, delay: float = 0.05):
        '''Flashes LED a number of times'''
        if not self.is_disabled:
            for i in range(flashes):
                self.led_on()
                sleep(delay)
                self.led_off()
                sleep(delay)

    def when_held2(self, func):
        '''
        Function to pass to when_held as lambda function
            example:
            button.when_held = lambda x: button.when_held2(button.led_toggle)
        '''
        self.running = True
        func()

    def when_released2(self, func):
        '''
        Function to pass to when_released as lambda function
            example:
            button.when_released = lambda x: button.when_released2(button.led_toggle)
        '''
        if not self.running:
            func()
        self.running = False


class AcceptButton(Button):
    '''Class for the accept button'''

    def __init__(self, button_pin: int):
        super().__init__(
            button_pin,
            hold_time=5,
        )

    def when_held2(self, func):
        '''
        Function to pass to when_held as lambda function
            example:
            button.when_held = lambda x: button.when_held2(button.led_toggle)
        '''
        self.running = True
        func()

    def when_released2(self, func):
        '''
        Function to pass to when_released as lambda function
            example:
            button.when_released = lambda x: button.when_released2(button.led_toggle)
        '''
        if not self.running:
            func()
        self.running = False

class PlayerButtonBoard():
    '''Class for group of PlayerButtons'''

    def __init__(self, buttons: List[PlayerButton]):
        self.buttons = buttons
        

    def led_cycle(self, num: int = 1, delay: float = 0.25):
        '''Cycles the LEDs on and off in order'''
        for _ in range(num):
            for button in self.buttons:
                button.led_on()
                sleep(delay)
                button.led_off()

    def led_flash(self, num: int = 1, delay: float = 0.25):
        '''Flashes the LEDS on and off'''
        for _ in range(num):
            for button in self.buttons:
                button.led_on()
            sleep(delay)
            for button in self.buttons:
                button.led_off()
            sleep(delay)
    
