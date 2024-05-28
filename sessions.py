import random

from typing import List
from enum import Enum

from config import BUTTON_LIST, ACCEPT_BUTTON, PLAYER_BUTTON_BOARD
from buttons import PlayerButton, AcceptButton, PlayerButtonBoard

# --------------------
# Player Choice Modes
# --------------------
"""
Choice modes control how the active player will be selected during the game

- Resume:           continue with the current active player
- Clockwise:        the next active player will be in clockwise order
- CounterClockwise: the next active player will be in counter clockwise order
- Random:           the next active player will be selected randomly and
                    proceed in clockwise order
- Selected:         the player order is selected by the players
"""

class SelectMode():
    '''Base class for select mode'''

    def __init__(self, accept_button: AcceptButton = ACCEPT_BUTTON):
        self.accept_button = accept_button
        self.is_active = False

    def _player_button_pressed(self):
        '''Function when PlayerButton is pressed'''
        pass

    def _mode_pattern():
        '''LED pattern on startup'''
        pass

    def _set_player_button_pressed(self):
        '''Set player buttons press function'''
        pass

    def start():
        '''Runs the mode pattern and sets button functions'''
        pass

class ResumeMode():
    '''Mode that continues with the current active player'''

    def __init__(self, buttons: List[PlayerButton], button_board: PlayerButtonBoard):
        super().__init__()
        self.buttons = buttons
        self.button_board = button_board

    def _player_button_pressed(self, button: PlayerButton):
        '''Function when PlayerButton is pressed'''
        pass # TODO

    def _mode_pattern(self):
        '''LED pattern on startup'''
        pass # TODO

    def _set_player_button_pressed(self):
        '''Set player buttons press function'''
        pass # TODO

    def start(self):
        '''Runs the mode pattern and sets button functions'''
        pass # TODO

class ClockwiseMode():
    '''Clockwise select mode'''

    def __init__(self, buttons: List[PlayerButton], button_board: PlayerButtonBoard):
        super().__init__()
        self.buttons = buttons
        self.button_board = button_board

    def _player_button_pressed(self):
        '''Function when PlayerButton is pressed'''
        pass # TODO

    def _mode_pattern(self):
        '''LED pattern on startup'''
        pass # TODO

    def _set_player_button_pressed(self):
        '''Set player buttons press function'''
        pass # TODO

    def start(self):
        '''Runs the mode pattern and sets button functions'''
        pass # TODO


# --------------------
# Session States
# --------------------
"""
Session states control how buttons behave at different stages of the program.

- Setup:    the stage when players select which buttons are in the game
- Game:     the stage when a single player is active and being timed
- Pause:    the stage when no player is active and the program is waiting
            for a new active player
"""
class SessionState():
    '''Base class for session state'''

    def __init__(self, accept_button: AcceptButton = ACCEPT_BUTTON):
        self.accept_button = accept_button
        self.is_active = True

    def _accept_button_pressed(self):
        '''Fuction when AcceptButton is pressed'''
        pass

    def _player_button_pressed(self):
        '''Function when PlayerButton is pressed'''
        pass

    def _startup_pattern():
        '''LED pattern on startup'''
        pass

    def _set_accept_button_pressed(self):
        '''Set accept button press function'''
        pass

    def _set_player_button_pressed(self):
        '''Set player buttons press function'''
        pass

    def start(self):
        '''Runs session state pattern and sets button functions'''
        self.startup_pattern()

class SetupState(SessionState):
    '''Setup session state'''

    def __init__(
            self,
            buttons: List[PlayerButton] = BUTTON_LIST,
            button_board: PlayerButtonBoard = PLAYER_BUTTON_BOARD,
        ):
        super().__init__()
        self.buttons = buttons
        self.button_board = button_board
        self.is_active = True
        self.active_buttons = set()

    def _accept_button_pressed(self):
        '''Function when AcceptButton is pressed'''
        inactive_buttons = list(set(self.buttons).difference(self.active_buttons))
        for button in inactive_buttons:
            button.active_button_toggle()
            button.disabled_toggle()
        self.is_active = False

    def _player_button_pressed(self, button: PlayerButton):
        '''Function when PlayerButton is pressed'''
        button.led_toggle()
        button.active_button_toggle()
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
            button.when_pressed = self._player_button_pressed

    def _startup_pattern(self):
        '''Starting LED pattern'''
        self.button_board.led_cycle(2)
        self.button_board.led_flash(3)

    def start(self):
        '''Runs session state pattern and sets button functions'''
        self._startup_pattern()
        self._set_player_button_pressed()
        self._set_accept_button_pressed()

class GameState(SessionState):
    '''Game session state'''

    def __init__(
            self,
            buttons: List[PlayerButton],
            button_board: PlayerButtonBoard
        ):
        super().__init__()
        self.buttons = buttons
        self.button_board = button_board


    def _startup_pattern(self):
        '''Starting LED pattern'''
        self.button_board.led_flash(num=3)

    def _set_accept_button_press(self):
        '''Set accept button press function'''
        pass # TODO

    def _set_player_button_press(self):
        '''Set player buttons press function'''
        pass # TODO

    def start(self):
        '''Runs session state pattern and sets button functions'''
        self._startup_pattern()

class PauseState():
    '''Pause session state'''

    def __init__(
        self,
        buttons: List[PlayerButton],
        button_board: PlayerButtonBoard,
        player_choice_mode: str = 'clockwise'
    ):
        super().__init__()
        self.buttons = buttons
        self.button_board = button_board
 
    def _startup_pattern(self):
        '''Starting LED pattern'''
        self.button_board.led_flash(num=3)

    def _set_accept_button_press(self):
        '''Set accept button press function'''
        pass # TODO

    def _set_player_button_press(self):
        '''Set player buttons press function'''
        pass # TODO

    def start(self):
        '''Runs session state pattern and sets button functions'''
        self._startup_pattern()
# --------------------
# Session
# --------------------
"""
A session is a single game. Session states are an attribute of a session.
"""
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

        while self.session_state.is_active:
            pass
        
        active_buttons = list(self.session_state.active_buttons)

        self.session_state = GameState(
            buttons = active_buttons,
            button_board = PlayerButtonBoard(active_buttons),
        )


    def reset(self):
        '''Reset session'''
        self.session_state = SetupState()
        for button in self.buttons:
            button.reset()

        
