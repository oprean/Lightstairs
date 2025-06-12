# pub.py
import time
import ntptime
import machine
import ntptime
import network
from uping import ping
from umqtt.simple import MQTTClient
from constants import *

server="broker.emqx.io"
ClientID = f'raspberry-pub-{time.time_ns()}'
user = "emqx"
password = "public"
topic = "raspberry/mqtt"
msg = b'{"msg":"hello"}'

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


def connect():
    print('Connected to MQTT Broker "%s"' % (server))
    client = MQTTClient(ClientID, server, 1883, user, password)
    client.connect()
    return client

def reconnect():
    print('Failed to connect to MQTT broker, Reconnecting...' % (server))
    time.sleep(5)
    client.reconnect()

try:
    wificonnect()
    ntptime.settime()
    print(time.localtime())
    client = connect()
except OSError as e:
    reconnect()

while True:
  print('send message %s on topic %s' % (msg, topic))
  online_status = ping(host='google.com', quiet=True)
  #print(online_status)
  if (online_status[1]>0):
       print("online")
  else:
       print("offline")
       #machine.reset()
       wificonnect()
  
  client.publish(topic, msg, qos=0)
  time.sleep(1)
