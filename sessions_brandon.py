from config import BUTTON_LIST, PLAYER_BUTTON_BOARD
from buttons_brandon import PlayerButton
from typing import List

class ButtonPush(PlayerButton):
    #Initialize the class
    def __init__(
            self,
            buttons: List[PlayerButton] = BUTTON_LIST,
        ):
        super().__init__()
        self.buttons = buttons
        self.button_hold = False

    #Button Press
    def button_press(self, button: PlayerButton):
        '''Button Press'''
        self.button.when_released

    #Check for hold of button
    def check_for_hold(self):
        '''Need to check for hold before confirming release (or push)'''
        if self.button_hold == True:
            self.button_held()
            self.button_hold = False
        else
            self.button_press()

class SetupState():
    def __init__(self) -> None:
        pass

    #for x in buttons make them flash / cycle
    #button push turns off and on Player and adds to an active list
    #disable all inactive buttons at end
    #players must select colors in clockwise (or player) order
    #randomly assign first player

class PlayState():
    def __init__(self) -> None:
        pass

    #flash start player 10 times
    #active player should have light on and a timer counting
    #when active player pushes button, should turn off and move to next in turn order
    #hold for pause on any active button (led on or off)
    #extra button used to end play

class CleanupState():
    def __init__(self) -> None:
        pass
    
    #at this point probably save a csv for color & time played
    #loop through fastest to slowest, lights blink (1 for fastest, 2 for 2nd fastest, etc)
    #extra button turns off resets program
    
    
