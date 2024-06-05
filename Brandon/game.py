from setup import PlayerButton, AcceptButton
from gpio import player_button_list, accept_button

class GameSetup():
    def __init__(self,
                player_buttons : list[PlayerButton] = player_button_list,
                accept_button : AcceptButton = accept_button,
            ):
            super().__init__()
            self.inactive_buttons = set()
            self.active_buttons = set()
            self.player_buttons = player_buttons
            self.is_active = True

    def acceptButtonPressed(self):
        for button in self.inactive_buttons:
            button.disableButton()
            button.is_active = False

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