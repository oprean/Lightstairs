#https://bytesnbits.co.uk/web-control-panel-web-server/
#https://timeapi.io/api/Time/current/zone?timeZone=Europe/Bucharest
#https://dev.to/opshack/why-is-my-browser-sending-an-options-http-request-instead-of-post-5621
import network
import json
import time
import machine
import re
from lib.webserver.request_parser import RequestParser
from lib.webserver.response_builder import ResponseBuilder
from lib.config import Config
from machine import Pin
import uasyncio as asyncio

from lib.onboard import Temperature 

onboard = Pin("LED", Pin.OUT, value=0)

HEARTBEAT = 1
MAX_WAIT = 10

class Controller():
    def __init__(self):
        self.config = Config()
        print('init controller')
        self.routes = [
            ['GET', '/status', 'status', 0],
            ['GET', '/action/pin/(\d+)/(\d+)', 'setpin', 2],
            ['GET', '/temperature', 'temperature', 0],
            ['POST', '/config', 'updateconfig', 0],
        ]

    def process(self, request):
        self.request = request
        response = ResponseBuilder()
        data = {}
        is_match = False
        print(json.dumps(request.__dict__))
        for route in self.routes:
            match = re.search(route[1], request.url)
            if match and request.method == 'OPTIONS':
                response.build_preflight()
                return response

            if match:
                is_match = True
                actionMethod = 'action_'+route[2]
                action = getattr(self,actionMethod)
                params = []
                for i in range(1, route[3]+1):
                    params.append(match.group(i))
                data = action(params)
                response.set_body_from_dict(data)
                break

        if (is_match == False):
            response.set_status(404)
            response.set_body('action not found')

        return response
    
    # actions
    def action_status(self, params):
        return self.config.data

    def action_updateconfig(self, params):
        self.config.update(self.request.content[0])
        return {'status':'config updated'}
    
    def action_temperature(self, params):
        temp = Temperature()
        temp = temp.ReadTemperature()
        return {'onboard_temperature':temp}
    
    def action_setpin(self, params):
        pin_number = int(params[0])
        pin_value = int(params[1])
        pin = Pin(pin_number, Pin.OUT)
        pin.value(pin_value)
        return {'pin':pin_number, 'value': pin_value}

class WebServer:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
    
    def connect_to_network(self):
        #https://github.com/orgs/micropython/discussions/12260
        ap = network.WLAN(network.AP_IF); ap.active(False)    # Disable AP!
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if wlan.isconnected():
            wlan.disconnect()
            print ('started in the connected state, but now disconnected')
        else:
            print ('started in the disconnected state')
        # if I ever need the mac address
        #mac = ubinascii.hexlify(wlan.config('mac'),':').decode()
        wlan.connect(self.ssid, self.password)
        cwait = MAX_WAIT
        while (cwait > 0):
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            cwait -= 1
            print('waiting for connection...')
            time.sleep(1)

        if wlan.status() != 3:
            raise RuntimeError('network connection failed')
        else:
            print('connected')
            status = wlan.ifconfig()
            print('ip = ' + status[0])

    async def serve_client(self, reader, writer):
        print("Client connected")
        request_raw = await reader.read(2048)
        request = RequestParser(request_raw)
        ctrl = Controller()
        response = ctrl.process(request)
        response.build_response()
        writer.write(response.response)
        await writer.drain()
        await writer.wait_closed()
        print("Client disconnected")

    async def main(self):
        print('Connecting to Network...')
        self.connect_to_network()

        print('Setting up webserver...')
        #https://stackoverflow.com/questions/50678184/how-to-pass-additional-parameters-to-handle-client-coroutine
        asyncio.create_task(asyncio.start_server(self.serve_client, "0.0.0.0", 80))
        while True:
            if (HEARTBEAT == 1):
                onboard.on()
                print("heartbeat")
            await asyncio.sleep(0.25)
            if (HEARTBEAT == 1):
                onboard.off()
            await asyncio.sleep(5)

    def start(self):
        try:
            asyncio.run(self.main())
        finally:
            asyncio.new_event_loop()
