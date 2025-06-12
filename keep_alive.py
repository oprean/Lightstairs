# pub.py
import time
import ntptime
import machine
import ntptime
import network
from uping import ping
from machine import Pin
from constants import *
onboard = Pin("LED", Pin.OUT, value=0)

def wificonnect():
	ssid = SSID
	password = PASSWORD
	wlan = network.WLAN(network.STA_IF)
	wlan.active(True)
	wlan.connect(ssid, password)
	while wlan.isconnected() == False:
		print('Waiting for connection...')
		time.sleep(1)
	print('Connected on {ip}'.format(ip = wlan.ifconfig()[0]))

try:
    wificonnect()
    ntptime.settime()
    print(time.localtime())
except OSError as e:
    print(e) 

while True:
  result = ping(host='google.com', quiet=True)
  #print(online_status)
  if (result[1]>0):
       print("online")
       onboard.on()
       time.sleep(0.25)
       onboard.off()
       time.sleep(1)

  else:
       print("offline")
       #machine.reset()
       wificonnect()
  time.sleep(1)
