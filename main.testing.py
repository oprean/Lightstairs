import machine
import neopixel
from lib.ota import OTAUpdater
import time
import urandom

# Configurația benzii LED
pin = machine.Pin(0)  # Schimbă cu pinul tău de control
num_leds = 30 + 29     # Total LED-uri pe ambele trepte
np = neopixel.NeoPixel(pin, num_leds)

# Definim intervalele pentru fiecare treaptă
treapta1 = list(range(0, 30))    # LED-urile 0-29
treapta2 = list(range(30, 59))   # LED-urile 30-58

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

# Loop de test
while True:
    aprinde_treapta(treapta1)
    time.sleep(2)

    aprinde_treapta(treapta2)
    time.sleep(2)

