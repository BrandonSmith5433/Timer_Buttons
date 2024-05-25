from gpiozero import Button, LED, LEDBoard
from time import sleep

from typing import List

from config import LED_BOARD, BUTTON_MAP, ACCEPT_BUTTON
from buttons import PlayerButton, AcceptButton

class SessionState():
    '''Base class for session state'''

    def startup_pattern():
        pass

    def on_button_press(button):
        pass

    def on_button_hold(button):
        pass

    def start(self):
        self.startup_pattern()

class SetupState(SessionState):
    '''Startup session state'''

    def startup_pattern():
        '''Starting LED pattern'''
        for i in range(3):
            for led in LED_BOARD:
                delay = 1 / (2 ** i)
                led.on()
                sleep(delay)
                led.off()
        for i in range(3):
            LED_BOARD.on()
            sleep(1)
            LED_BOARD.off()

    def on_button_pressed(button):
        '''When a button is pressed'''
        pass # TODO

    def on_button_hold(button):
        '''When a button is held'''
        pass # TODO

    def start(self):
        '''Start session state'''
        self.startup_pattern()

class GameState(SessionState):
    '''Startup session state'''

    def startup_pattern():
        '''Starting LED pattern'''
        pass # TODO

    def on_button_pressed(button):
        '''When a button is pressed'''
        pass # TODO

    def on_button_hold(button):
        '''When a button is held'''
        pass # TODO

    def start(self):
        '''Start session state'''
        self.startup_pattern()




    

class Session():
    '''Class for game session'''

    def __init__(self):
        self.buttons = BUTTON_MAP.copy()
        self.session_buttons = []
        self.session_state = SetupState()

    
    def start(self):
        '''Initialize session'''

        self.session_state.start()

        if isinstance(self.session_state, SetupState):
            for button in self.buttons.values():
                button.when_held
        else isinstance(self.session_state, GameState):
            pass # TODO
