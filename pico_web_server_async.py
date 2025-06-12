import network
import json
import time
import re

from machine import Pin
import uasyncio as asyncio
from constants import *

led = Pin(15, Pin.OUT)
onboard = Pin("LED", Pin.OUT, value=0)

wlan = network.WLAN(network.STA_IF)

def connect_to_network():
    wlan.active(True)
    #wlan.config(pm = 0xa11140) # Disable power-save mode
    wlan.connect(ssid, password)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])

def actionStatus():
	status = {}
	status['led'] = 1
	return status

def controller(route):
	match = re.search('/action/toggle/(\d+)/(\d+)', route)
	if (route.find('/status') > 0):
		actionStatus()
	elif (route.find('/action/toggle') > 0):
		actionStatus()		

async def serve_client(reader, writer):
	print("Client connected")
	request_line = await reader.readline()
	print("Request:", request_line)
	# We are not interested in HTTP request headers, skip them
	while await reader.readline() != b"\r\n":
		pass
	request = str(request_line)



	led_on = request.find('/light/on')
	led_off = request.find('/light/off')
	print( 'led on = ' + str(led_on))
	print( 'led off = ' + str(led_off))

	stateis = ""
	if led_on == 6:
		print("led on")
		led.value(1)
		stateis = "LED is ON"

	if led_off == 6:
		print("led off")
		led.value(0)
		stateis = "LED is OFF"

	status = {}
	status['led'] = stateis
	response = json.dumps(status)

	writer.write('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n')
	writer.write('Access-Control-Allow-Origin: *\r\n')
	writer.write('\r\n\r\n')
	writer.write(response)

	await writer.drain()
	await writer.wait_closed()
	print("Client disconnected")

async def main():
	print('Connecting to Network...')
	connect_to_network()

	print('Setting up webserver...')
	asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
	while True:
		onboard.on()
		print("heartbeat")
		await asyncio.sleep(0.25)
		onboard.off()
		await asyncio.sleep(5)

try:
	asyncio.run(main())
finally:
	asyncio.new_event_loop()
