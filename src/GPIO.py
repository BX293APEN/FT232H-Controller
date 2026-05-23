#!/usr/bin/env python3
import os

class FT232H:
    def __init__(self):
        self.dire = os.path.dirname(os.path.abspath(__file__)).replace(os.path.sep, '/')
        if os.environ.get("BLINKA_FT232H")      != "1":
            os.environ["BLINKA_FT232H"]         = "1"

        import board
        self.board                              = board
        if self.check_pin("C0"):
            import digitalio, busio
            self.digitalio                      = digitalio
            self.busio                          = busio
            self.OUT                            = self.digitalio.Direction.OUTPUT
            self.IN                             = self.digitalio.Direction.INPUT
    
    def check_pin(self, pinName):
        return pinName in dir(self.board)
    
    def Pin(self, pinName, mode = None):   # .value True/False : ON/OFF
        if self.check_pin(pinName):
            pin                                 = getattr(self.board, pinName)
            if mode is None:
                return pin
            else:
                gpio                            = self.digitalio.DigitalInOut(pin)
                gpio.direction                  = mode
                return gpio
        else:
            return None
        
    def I2C(self):
        if self.check_pin("SCL"):
            return self.busio.I2C(self.Pin("SCL"), self.Pin("SDA"))
        else:
            return None

if __name__ == "__main__":
    ft232h = FT232H()
    from time import sleep
    if ft232h.check_pin("C7"):
        led = ft232h.Pin("C7", ft232h.OUT)
        while True:
            led.value = (not led.value)
            sleep(1)

