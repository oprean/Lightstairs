#https://www.halvorsen.blog/documents/technology/iot/pico/pico_temperature_sensor_builtin.php
#https://core-electronics.com.au/guides/getting-started-with-servos-examples-with-raspberry-pi-pico/#example-1
from machine import ADC

class Temperature:
    def __init__(self):
        adcpin = 4
        self.sensor = ADC(adcpin)
        
    def ReadTemperature(self):
        adc_value = self.sensor.read_u16()
        volt = (3.3/65535)*adc_value
        temperature = 27 - (volt - 0.706)/0.001721
        return round(temperature, 1)