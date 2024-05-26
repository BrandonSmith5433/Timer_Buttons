from time import sleep

from typing import List

from config import BUTTON_LIST, ACCEPT_BUTTON, PLAYER_BUTTON_BOARD
from buttons import PlayerButton, AcceptButton, PlayerButtonBoard

class SessionState():
    '''Base class for session state'''

    def __init__(self, buttons: List[PlayerButton], accept_button: AcceptButton = ACCEPT_BUTTON):
        self.accept_button = accept_button
        self.is_active = True

    def _accept_button_pressed(self):
        '''Fuction when AcceptButton is pressed'''
        pass

    def _player_button_pressed(self):
        '''Function when PlayerButton is pressed'''
        pass

    def startup_pattern():
        '''LED pattern on startup'''
        pass

    def set_accept_button_pressed(self):
        '''Set accept button press function'''
        pass

    def set_player_button_pressed(self):
        '''Set player buttons press function'''
        pass

    def start(self):
        '''Runs session state pattern and sets button functions'''
        self.startup_pattern()

class SetupState(SessionState):
    '''Startup session state'''

    def __init__(
            self,
            buttons: List[PlayerButton] = BUTTON_LIST,
            button_board: PlayerButtonBoard = PLAYER_BUTTON_BOARD
        ):
        self.buttons = buttons
        self.active_buttons = set()

    def _accept_button_pressed(self):
        '''Function when AcceptButton is pressed'''
        self.is_active = False

    def _player_button_pressed(self, button: PlayerButton):
        '''Function when PlayerButton is pressed'''
        button.led_toggle()
        button.toggle_active()
        if button in self.active_buttons:
            self.active_buttons.remove(button)
        else:
            self.active_buttons.add(button)

    def _set_accept_button_pressed(self):
        '''Set accept button press function'''
        self.accept_button.when_pressed = self._accept_button_pressed

    def _set_player_button_pressed(self):
        '''Set player buttons press function'''
        for button in self.buttons:
            button.when_pressed = lambda: self._player_button_pressed(button)

    def startup_pattern(self):
        '''Starting LED pattern'''
        self.button_board.led_cycle(3)

    def start(self):
        '''Start session state'''
        self.startup_pattern()

class GameState(SessionState):
    '''Startup session state'''

    def startup_pattern():
        '''Starting LED pattern'''
        pass # TODO

    def set_accept_button_press(self):
        '''Set accept button press function'''
        pass # TODO

    def set_player_button_press(self):
        '''Set player buttons press function'''
        pass # TODO

    def start(self):
        '''Start session state'''
        self.startup_pattern()




    

class Session():
    '''Class for session'''

    def __init__(
            self,
            buttons: List[PlayerButton] = BUTTON_LIST,
            accept_button: AcceptButton =  ACCEPT_BUTTON,
            session_state: SessionState = SetupState(),
        ):
            self.buttons = buttons
            self.accept_button = accept_button
            self.session_state = session_state

    
    def start(self):
        '''Initialize session'''

        # Setup state
        self.session_state.start()

        while self.session_state.active:
            pass
        



        
