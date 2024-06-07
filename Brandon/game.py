from setup import PlayerButton, AcceptButton
from gpio import player_button_list, accept_button

class GameState():
    def __init__(
                self,
                buttons : list[PlayerButton] = player_button_list,
                accept_button : AcceptButton = accept_button,
                ):
        self.buttons = buttons
        self.accept_button = accept_button
        self.current_state = current_state

    def advanceGameState(self):
        if self.current_state ==  GameSetup:
            self.current_state = GameActive
        elif self.current_state == GameActive:
            self.current_State = GameCleanup
        self.start()

    def start(self)
        '''Starts next game state'''
        self.current_state(self.game_state)
        
        
class GameSetup(GameState):
    def __init__(self,
                player_buttons : list[PlayerButton],
                accept_button : AcceptButton,
            ):
            self.inactive_buttons = set()
            self.active_buttons = set()
            self.player_buttons = player_buttons
            self.is_active = True

    def acceptButtonPressed(self):
        for button in self.inactive_buttons:
            button.ledOff()
            button.disableButton()

    def buttonPressed(self, button : PlayerButton):
        button.ledToggle()
        if button in self.inactive_buttons:
            self.active_buttons.add(button)
            self.inactive_buttons.remove(button)
        else:
            self.active_buttons.remove(button)
            self.inactive_buttons.add(button)

    def activateButtons(self):
        for button in PlayerButton:
            button.when_pressed = self.buttonPressed
        accept_button.when_pressed = self.acceptButtonPressed

    def start(self):
        PlayerButton.ledCycle(5)
        for button in PlayerButton:
            self.ledOff()
            self.inactive_buttons.add(button)
        self.activateButtons()

class GameActive(GameState):
    pass

class GameCleanup(GameState):
    pass




