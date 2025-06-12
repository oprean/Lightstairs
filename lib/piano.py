import uasyncio
import machine
from machine import Pin
from lib.multiplex import Multiplex
import time

LDR_READ_CNT = 10
LDR_READ_DELAY = 1

class Piano:
    """
    Piano stairs
    https://www.instructables.com/Piano-Stairs-with-Arduino-and-Raspberry-Pi/
    """
    def __init__(self, s0_pin, s1_pin, s2_pin, s3_pin, z_pin):
        self.multiplex = Multiplex(s0_pin, s1_pin, s2_pin, s3_pin, z_pin)
    
    def run(self):
        print("palying piano")


