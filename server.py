#!/bin/env python
# -*- coding: utf-8 -*-
import json
import time

import random
import datetime

import tornado.websocket
import tornado.web
import tornado.ioloop

import RPi.GPIO as GPIO
import dht11
import datetime

class SendWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print ('Session Opened. IP:' + self.request.remote_ip)
        self.ioloop = tornado.ioloop.IOLoop.instance()
        
        # initialize GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()

        # read data using pin no
        instance = dht11.DHT11(pin=4)
        
        self.send_websocket()

    def on_close(self):
        print("Session closed")

    def check_origin(self, origin):
        return True

    def send_websocket(self):
        self.ioloop.add_timeout(time.time() + 1, self.send_websocket)
        if self.ws_connection:
            result = instance.read()
            if result.is_valid():                
                message = json.dumps({
                    'time': str(datetime.datetime.now()),
                    'Temperature': str(result.temperature),
                    'Humidity': str(result.humidity),
                    })
                self.write_message(message)
                

app = tornado.web.Application([(r"/ws/display", SendWebSocket)])

if __name__ == "__main__":
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
