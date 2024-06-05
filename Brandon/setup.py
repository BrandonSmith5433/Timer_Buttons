from gpiozero import Button, LED
from time import sleep, time

class PlayerButton(Button):
    def __init__(self, color: str, button_pin: int, led_pin: int):
        super().__init__(
            button_pin,
            hold_time=1,
            bounce_time = 0.1,
        )
        self.color = color
        self.led = LED(led_pin)
        self.is_disabled = False
        self.was_held = False
        self.is_active = True

    def disableButton(self):
        self.is_disabled = True

    def enableButton(self):
        self.is_disabled = False

    def ledOn(self):
        if self.is_disabled == False:
            self.led.on()

    def ledOff(self):
        self.led.off()

    def ledToggle(self):
        self.led.toggle()
    
    def ledCycle(self, count : int):
        for i in range(count):
            for button in PlayerButton:
                if not self.is_disabled:
                    self.ledOn()
                    sleep(.1)
                    self.ledOff()
                    sleep(.1)

class AcceptButton(Button):
    def __init__(self, button_pin: int):
        super().__init__(
            button_pin,
            hold_time = 1,
            bounce_time = .1
        )
