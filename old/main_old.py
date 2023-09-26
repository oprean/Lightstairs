import utime
import machine
import uasyncio
from lib.hcsr04 import HCSR04
from lib.neopixel import Neopixel  

LEDSTRIP_NUM_LEDS = 60
LEDSTRIP_PIN = 0

SENSOR_PIN_TRIGGER = 2
SENSOR_PIN_ECHO = 3
## in centimeter
SENSOR_DISTANCE = 50

PHOTO_PIN = 28
PHOTO_READ_CNT = 100
PHOTO_READ_DELAY = 100
## in percent
PHOTO_DUSK_VALUE = 60

BUTTON_PIN = 1

white = (255, 255, 255)
black = (0, 0, 0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

colors = [white,red,green,blue]

class StairsTester:
    
    def __init__(self):
        self.sensor = HCSR04(trigger_pin = SENSOR_PIN_TRIGGER, echo_pin = SENSOR_PIN_ECHO, echo_timeout_us = 10000)
        self.strip = Neopixel( num_leds = LEDSTRIP_NUM_LEDS, state_machine=0, pin = LEDSTRIP_PIN, mode = "RGB", delay = 0.0001)
        self.button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
        self.cid = 0
        self.pulse = 0
        self.inc = 1
        self.color = colors[self.cid]
        self.init()

    ## https://peppe8o.com/how-to-use-a-photoresistor-with-raspberry-pi-pico/
    def readLight(self):
        photoRes = machine.ADC(machine.Pin(PHOTO_PIN))
        mesurements = 0
        for i in range(PHOTO_READ_CNT):
            light = photoRes.read_u16()
            light = round(light/65535*100,2)
            utime.sleep_us(PHOTO_READ_DELAY)
            mesurements += light

        light = mesurements / PHOTO_READ_CNT
        return light

    def fadeIn(self, color):
        for i in range(255):
            print("bright: " + str(i))
            utime.sleep_us(3000)
            self.strip.brightness(i)
            self.strip.fill(color)
            self.strip.show()

    def fadeOut(self, color):
        for i in range(255,0,-1):
            print("bright: " + str(i))
            utime.sleep_us(3000)
            self.strip.brightness(i)
            self.strip.fill(color)
            self.strip.show()
        self.strip.fill(black)
        self.strip.show()

     def startFromTop(self):
       for i in range(STAIRS_CNT):
        for cs in range(-STAIRS_FADE*i, STAIRS_FADE):
            self.strip.fade_pixel_line(STAIRS[i][0],STAIRS[i][0],red,black,cs,STAIRS_FADE)
            self.strip.show()
            utime.sleep_us(3000)

    def lights(self, color):
        self.fadeIn(color)
        utime.sleep(2)
        self.fadeOut(color)
    
    def pulseLight(self):
        print(self.pulse)
        self.strip.brightness(self.pulse)
        self.strip.set_pixel_line(4,6, self.color)
        if (self.pulse > 255): self.inc = -10
        if (self.pulse < 0): self.inc = 10
        self.pulse += self.inc
        self.strip.show()

    def nextColor(self):
        print("new color: " + str(self.cid))    
        if (self.cid<len(colors)-1):
            self.cid += 1
        else:
            self.cid = 0
        return colors[self.cid]

    def init(self):
        self.strip.fill(white)
        self.strip.brightness(255)
        self.strip.show()
        utime.sleep(1)
        self.strip.fill(black)
        self.strip.brightness(0)
        self.strip.show()
        
    def run(self):
        while True:
            distance = self.sensor.distance_cm()
            light = self.readLight()
            print("Distance: " + str(distance) + " light :" + str(light))
            
            if (self.button.value() == 0):
                self.color = self.nextColor()
            
            if (light < PHOTO_DUSK_VALUE):           
                self.pulseLight()
                utime.sleep_us(90000)
                if (distance < SENSOR_DISTANCE):
                    self.pulse = 0
                    self.inc = 10
                    self.lights(self.color)
            else:
                self.pulse = 0
                self.inc = 10
                self.strip.fill(black)
                self.strip.brightness(0)
                self.strip.show()
                
## the test program start here!   
tester = StairsTester()
tester.run()

