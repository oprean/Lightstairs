import utime
import machine
import uasyncio
from lib.hcsr04 import HCSR04
from lib.neopixel import Neopixel
from lib.multiplex import Multiplex
from lib.ldr import LDR

RUNNING_MODE_SLEEPING = 1
RUNNING_MODE_WATCHFUL = 2
RUNNING_MODE_PIANO = 3
RUNNING_MODE_AI = 4

LEDSTRIP_NUM_LEDS = 60
LEDSTRIP_PIN = 0

SENSOR_PIN_TRIGGER = 2
SENSOR_PIN_ECHO = 3

## in centimeter
SENSOR_DISTANCE = 50
TOP_SENSOR_DISTANCE = 50
BOTTOM_SENSOR_DISTANCE = 50

LDR_PIN = 28

## in percent
PHOTO_DUSK_VALUE = 50

BUTTON_PIN = 1

PULSE_INC = 1

"""
STAIRS_CNT = 17
STAIRS_FADE = 17
STAIRS = [
    [0, 29],     #17 (top staier)
    [30, 60],    #16
    [61, 91],    #15
    [92, 122],   #14
    [123, 153],  #13
    [154, 184],  #12
    [185, 215],  #11 
    [216, 243],  #10 (higher deck)
    [244, 274],  # window
    [275, 302],  #09 (lower deck)
    [303, 330],  #08
]
"""

STAIRS_CNT = 6
STAIRS_FADE_STEPS = 255
STAIRS_FADE_SPEED = 200
STAIRS = [
    [0, 10],     #17 (top staier)
    [10, 20],    #16
    [20, 30],    #15
    [30, 40],  	 #14
    [40, 50], 	 #13
    [50, 60], 	 #13
]


white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 165, 0)
yellow = (255, 150, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
indigo = (75, 0, 130)
violet = (138, 43, 226)

colors = [white, red, orange, yellow, green, blue, indigo, violet]

class StairsPainter:
    def __init__(self):
      self.strip = Neopixel( num_leds = LEDSTRIP_NUM_LEDS, state_machine=0, pin = LEDSTRIP_PIN, mode = "GRB", delay = 0.0001)
      self.sensor = HCSR04(trigger_pin = SENSOR_PIN_TRIGGER, echo_pin = SENSOR_PIN_ECHO, echo_timeout_us = 10000)
      self.button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
      self.ldr = LDR(LDR_PIN)
      self.distance = 999
      self.light = 0
      self.cid = 0
      self.pulse = 0
      self.inc = PULSE_INC
      self.color = colors[self.cid]
      self.strip.brightness(100)
      self.init_Visual()
      
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
        
    def nextColor(self):
        print("new color: " + str(self.cid))    
        if (self.cid<len(colors)-1):
            self.cid += 1
        else:
            self.cid = 0
        return colors[self.cid]
    
    def fadeAll(self, color, inc):
        steps = 255
        if (inc == 1):
            color1 = black
            color2 = color
        else:
            color1 = color
            color2 = black
            
        for i in range(steps):
            self.strip.fade_pixel_line(0, LEDSTRIP_NUM_LEDS, color1, color2, i, steps)
            self.strip.show()
            utime.sleep_ms(1)
            
        if (inc == -1):
            self.strip.fill(black)
            self.strip.show()
    
    def lights_OLD(self):
        self.fadeAll(self.color,1)
        uasyncio.sleep(2)
        self.fadeAll(self.color,-1)
        
    def lights(self, direction = "down"):
       self.strip.clear()
       self.strip.show()
       if (direction == "down"):
           range_stairs = range(STAIRS_CNT)
       else:
           range_stairs = range(STAIRS_CNT-1,-1,-1)
           
       for i in range_stairs:
        #print("stair " + str(i) + "[" + str(STAIRS[i][0]) + " : " + str(STAIRS[i][1]) + "]")
        for cs in range(STAIRS_FADE_STEPS):
            self.strip.fade_pixel_line(STAIRS[i][0], STAIRS[i][1], black, self.color, cs, STAIRS_FADE_STEPS)
            utime.sleep_us(STAIRS_FADE_SPEED)
            self.strip.show()
        utime.sleep_us(STAIRS_FADE_SPEED)
        
       #utime.sleep_us(3000)
       
       for i in range_stairs:
        #print("stair " + str(i) + "[" + str(STAIRS[i][0]) + " : " + str(STAIRS[i][1]) + "]")
        for cs in range(STAIRS_FADE_STEPS):
            self.strip.fade_pixel_line(STAIRS[i][0], STAIRS[i][1], self.color, black, cs, STAIRS_FADE_STEPS)
            utime.sleep_us(STAIRS_FADE_SPEED)
            self.strip.show()
        self.strip.set_pixel_line(STAIRS[i][0], STAIRS[i][1], black,0)
        self.strip.show()
        utime.sleep_us(STAIRS_FADE_SPEED)
    
       self.strip.clear()
       self.strip.show()
       
    def pulseLight_OLD(self):
        self.strip.brightness(self.pulse)
        self.strip.set_pixel_line(4,6, self.color)
        if (self.pulse > 255): self.inc = -PULSE_INC
        if (self.pulse < 0): self.inc = PULSE_INC
        self.pulse += self.inc
        self.strip.show()
        
    def pulseLight_V1(self):
        self.strip.clear()
        max_range = 7
        m = 18
        if (self.pulse >= LEDSTRIP_NUM_LEDS-max_range):
            self.inc = -PULSE_INC
            self.pulse = LEDSTRIP_NUM_LEDS-max_range
            self.color = self.nextColor()
        if (self.pulse <= max_range):
            self.inc = PULSE_INC
            self.pulse = max_range
            self.color = self.nextColor()
        
        for i in range(1,max_range):
            color = (int(self.color[0]/i*m), int(self.color[1]/i*m), int(self.color[2]/i*m))
            self.strip.set_pixel(self.pulse-i+1, color)
            self.strip.set_pixel(self.pulse+i-1, color)
            #self.strip.fade_pixel(self.pulse-i, black, self.color, i, max_range)
            #self.strip.fade_pixel(self.pulse+i-1, self.color, black, i, max_range)
            
        self.pulse += self.inc
        self.strip.show()
        
    def pulseLight(self):
        self.strip.clear()
        max_range = 7
        m = 18
        if (self.pulse >= LEDSTRIP_NUM_LEDS-max_range):
            self.inc = -PULSE_INC
            self.pulse = LEDSTRIP_NUM_LEDS-max_range
            self.color = self.nextColor()
        if (self.pulse <= max_range):
            self.inc = PULSE_INC
            self.pulse = max_range
            self.color = self.nextColor()
        
        for i in range(1,max_range):
            color = (int(self.color[0]/i*m), int(self.color[1]/i*m), int(self.color[2]/i*m))
            self.strip.set_pixel(self.pulse-i+1, color)
            self.strip.set_pixel(self.pulse+i-1, color)
            #self.strip.fade_pixel(self.pulse-i, black, self.color, i, max_range)
            #self.strip.fade_pixel(self.pulse+i-1, self.color, black, i, max_range)
            
        self.pulse += self.inc
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
            await uasyncio.sleep_ms(50)
            if (self.light < PHOTO_DUSK_VALUE or True):
                if (self.distance < SENSOR_DISTANCE):
                    self.pulse = 0
                    self.inc = PULSE_INC
                    self.lights()
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
        
stairs = StairsPainter()   
stairs.run()