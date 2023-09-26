import uasyncio
import machine
from machine import Pin, ADC  
from time import sleep

class Multiplex:
    """
    Driver to use the multiplexor with 16 channels.
    http://multiwingspan.co.uk/pico.php?page=multiplex
    https://www.instructables.com/Tutorial-74HC4067-16-Channel-Analog-Multiplexer-De/
    """
    def __init__(self, s0_pin, s1_pin, s2_pin, s3_pin, z_pin):
        self.s_pins = [
            Pin(s0_pin, Pin.OUT),
            Pin(s1_pin, Pin.OUT),
            Pin(s2_pin, Pin.OUT),
            Pin(s3_pin, Pin.OUT)
        ]
        self.z_pin = ADC(z_pin)  

    def select_pin(self,p): 
        for i in range(4): 
            self.s_pins[i].value((p>>i)&1) 

    def read_pots(self): 
        pots = [] 
        for i in range(16): 
            self.select_pin(i, self.s_pins) 
            pots.append(self.z_pin.read_u16()//256) 
        return pots 
"""
from machine import Pin, ADC  
from time import sleep

select_pin_nums = [4,5,6] 
s_pins = [Pin(i, Pin.OUT) for i in select_pin_nums] 
z_pin = ADC(26)  

btn_a = Pin(27,Pin.IN,Pin.PULL_UP) 

def select_pin(p, pins): 
    for i in range(3): 
        pins[i].value((p>>i)&1) 

def read_pots(): 
    pots = [] 
    for i in range(8): 
        select_pin(i, s_pins) 
        pots.append(z_pin.read_u16()//256) 
    return pots 

# subroutine to handle button presses 
def btn_a_handler(pin): 
    data = read_pots() 
    print(data)
    
# attach IRQ to button pin 
btn_a.irq(trigger=Pin.IRQ_RISING, handler=btn_a_handler) 
"""