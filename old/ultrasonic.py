import utime
from lib.hcsr04 import HCSR04
sensor = HCSR04(trigger_pin=3, echo_pin=2, echo_timeout_us=10000)
while True:
    distance = sensor.distance_cm()
    print(distance)
    utime.sleep_us(90000)