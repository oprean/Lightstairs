import machine
import neopixel
from ota import OTAUpdater
import time
import urandom
from constants import *

# Configurația benzii LED
pin = machine.Pin(0)  # Schimbă cu pinul tău de control
num_leds = 30 + 29 + 29 + 29 + 29 + 29 + 30 + 23   # Total LED-uri pe ambele trepte
np = neopixel.NeoPixel(pin, num_leds)
np.brightness(125)
firmware_url = "https://raw.githubusercontent.com/oprean/Lightstairs/master"

ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main.testing.py","main.py")
ota_updater.download_and_install_update_if_available()

# Definim intervalele pentru fiecare treaptă
treapta1 = list(range(0, 30))    # LED-urile 0-29
treapta2 = list(range(30, 59))   # LED-urile 30-58
treapta3 = list(range(59, 88))   # LED-urile 30-58
treapta4  = list(range(88, 117))   # LED-urile 30-58
treapta5  = list(range(117, 146))   # LED-urile 30-58
treapta6  = list(range(146, 175))   # LED-urile 30-58
treapta7  = list(range(175, 205))   # LED-urile 30-58
treapta8  = list(range(205, 228))   # LED-urile 30-58

def culoare_random():
    return (urandom.getrandbits(8), urandom.getrandbits(8), urandom.getrandbits(8))

def aprinde_treapta(treapta):
    # Oprim toate LED-urile
    for i in range(num_leds):
        np[i] = (0, 0, 0)

    # Aprindem treapta selectată cu o culoare random
    culoare = culoare_random()
    for i in treapta:
        np[i] = culoare

    np.write()

def aprinde_tot():
    # pornim toate LED-urile
    culoare = culoare_random()
    for i in range(num_leds):
        np[i] = culoare

    np.write()    

# Loop de test
while True:
    aprinde_treapta(treapta1)
    time.sleep(1)

    aprinde_tot()
    time.sleep(1)

    aprinde_treapta(treapta2)
    time.sleep(1)
    
    aprinde_tot()
    time.sleep(1)

    aprinde_treapta(treapta3)
    time.sleep(1)
    
    aprinde_tot()
    time.sleep(1)

    aprinde_treapta(treapta4)
    time.sleep(1)
    
    aprinde_tot()
    time.sleep(1)    

    aprinde_treapta(treapta5)
    time.sleep(1)
    
    aprinde_tot()
    time.sleep(1)

    aprinde_treapta(treapta6)
    time.sleep(1)        
    
    aprinde_tot()
    time.sleep(1)    

    aprinde_treapta(treapta7)
    time.sleep(1)

    aprinde_tot()
    time.sleep(1)    

    aprinde_treapta(treapta8)
    time.sleep(1)    