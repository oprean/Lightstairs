import utime
import machine
import uasyncio
from lib.hcsr04 import HCSR04
from lib.neopixel import Neopixel  
from lib.multiplex import Multiplex
from lib.ldr import LDR

LEDSTRIP_NUM_LEDS = 60
LEDSTRIP_PIN = 0

SENSOR_PIN_TRIGGER = 2
SENSOR_PIN_ECHO = 3
## in centimeter
SENSOR_DISTANCE = 50

LDR_PIN = 28

## in percent
PHOTO_DUSK_VALUE = 50

BUTTON_PIN = 1

PULSE_INC = 1

white = (255, 255, 255)
black = (0, 0, 0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

colors = [white,red,green,blue]

class StairsTester:
    
    def __init__(self):
        self.sensor = HCSR04(trigger_pin = SENSOR_PIN_TRIGGER, echo_pin = SENSOR_PIN_ECHO, echo_timeout_us = 10000)
        self.strip = Neopixel( num_leds = LEDSTRIP_NUM_LEDS, state_machine=0, pin = LEDSTRIP_PIN, mode = "GRB", delay = 0.0001)
        self.button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
        self.distance = 999
        self.ldr = LDR(LDR_PIN)
        self.light = 0
        self.cid = 0
        self.pulse = 0
        self.inc = PULSE_INC
        self.color = colors[self.cid]
        self.init_Visual()

    def fadeIn(self, color):
        for i in range(255):
            print("bright up: " + str(i))
            #uasyncio.sleep_ms(3000)
            self.strip.brightness(i)
            self.strip.fill(color)
            self.strip.show()

    def fadeOut(self, color):
        for i in range(255,0,-1):
            print("bright down: " + str(i))
            #uasyncio.sleep_ms(3000)
            self.strip.brightness(i)
            self.strip.fill(color)
            self.strip.show()
        self.strip.fill(black)
        self.strip.show()

    def lights(self, color):
        self.fadeIn(color)
        uasyncio.sleep(2)
        self.fadeOut(color)
    
    def pulseLight(self):
        self.strip.brightness(self.pulse)
        self.strip.set_pixel_line(4,6, self.color)
        if (self.pulse > 255): self.inc = -PULSE_INC
        if (self.pulse < 0): self.inc = PULSE_INC
        self.pulse += self.inc
        self.strip.show()

    def nextColor(self):
        print("new color: " + str(self.cid))    
        if (self.cid<len(colors)-1):
            self.cid += 1
        else:
            self.cid = 0
        return colors[self.cid]

    def init_Visual(self):
        col1 = black
        col2 = red
        self.strip.fill(black)
        self.strip.brightness(125)
        self.strip.show()
        print("init visual!")
        middle = int(LEDSTRIP_NUM_LEDS/2)
        
        for i in range(middle):
            self.strip.set_pixel_line_gradient(middle,middle-i,col1, col2)
            self.strip.set_pixel_line_gradient(middle+1, middle-1+i, col2, col1)
            self.strip.show()
            utime.sleep_ms(10)
        for i in range(middle):
            self.strip.set_pixel_line_gradient(i,middle,col1, col2)
            self.strip.set_pixel_line_gradient(middle+1, middle*2-i-1, col2, col1)
            self.strip.show()
            utime.sleep_ms(10)

        self.strip.fill(black)
        self.strip.brightness(0)
        self.strip.show()
       
    async def read_Button(self):
        while True:
            if (self.button.value() == 0):
                self.color = self.nextColor()
            await uasyncio.sleep_ms(200)

    async def read_Light(self):
        while True:
            self.light = self.ldr.get_light_percentage()
            print("Light :" + str(self.light))
            await uasyncio.sleep(1)

    async def read_Distance(self):
        while True:
            self.distance = self.sensor.distance_cm()
            print("Distance: " + str(self.distance))
            await uasyncio.sleep_ms(1000)

    async def run_Main(self):
        while True:
            print("Distance: " + str(self.distance) + " light :" + str(self.light))
            await uasyncio.sleep_ms(50)
            if (self.light < PHOTO_DUSK_VALUE):
                #await uasyncio.sleep(1)
                if (self.distance < SENSOR_DISTANCE):
                    self.pulse = 0
                    self.inc = PULSE_INC
                    self.lights(self.color)
                else:
                    self.pulseLight()
            else:
                self.pulse = 0
                self.inc = PULSE_INC
                self.strip.fill(black)
                self.strip.brightness(0)
                self.strip.show()


    def run(self):
        event_loop = uasyncio.get_event_loop()
        event_loop.create_task(self.read_Button())
        event_loop.create_task(self.read_Light())
        event_loop.create_task(self.read_Distance())
        event_loop.create_task(self.run_Main())
        event_loop.run_forever()                   
                
## the test program start here!   
tester = StairsTester()
tester.run()
