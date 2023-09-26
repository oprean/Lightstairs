import uasyncio
import machine
from machine import Pin
import time

LDR_READ_CNT = 10
LDR_READ_DELAY = 1

class LDR:
    """
    Driver to use the photoresitor GL55xy.
    There are more types, for the moment just generic implementation
    https://peppe8o.com/how-to-use-a-photoresistor-with-raspberry-pi-pico/
    https://www.donskytech.com/micropython-read-ldr-or-photoresistor/
    """
    def __init__(self, pin):
        self.ldr_pin = machine.ADC(Pin(pin))
        
    def get_raw_value(self):
        return self.ldr_pin.read_u16()
    
    def get_light_percentage(self):
        mesurements = 0
        for i in range(LDR_READ_CNT):
            raw_value = self.ldr_pin.read_u16()
            raw_value = round(raw_value/65535*100,2)
            uasyncio.sleep_ms(LDR_READ_DELAY)
            mesurements += raw_value
            
        light_percent = mesurements / LDR_READ_CNT
        return light_percent



