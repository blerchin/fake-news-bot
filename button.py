#!/usr/bin/env python3

import asyncio
import json
import signal
import RPi.GPIO as GPIO
from time import sleep
import websockets

constants = json.loads(open("constants.json").read())

WS_URL = constants['WS_URL']

PIN_LIGHT=17
PIN_SWITCH=27

class Button():
	SPEED_SOLID=0
	SPEED_SLOW=1
	SPEED_FAST=3

	def __init__(self):
		self.setup_gpio()
		GPIO.setup(PIN_SWITCH, GPIO.IN,  pull_up_down=GPIO.PUD_UP)
		GPIO.setup(PIN_LIGHT, GPIO.OUT)
		self.dc = 0
		self.light = GPIO.PWM(PIN_LIGHT, 50)
		self.light.start(self.dc)
		self.dir = 0
		self.speed = self.SPEED_SLOW
		self.button_pressed = False
		self.speaking = False
		self.loop = asyncio.get_event_loop()
		self.loop.run_until_complete(self.connect_ws())
		self.check_ws()
	
	def setup_gpio(self):
		GPIO.setmode(GPIO.BCM)

	@asyncio.coroutine
	def connect_ws(self):
		self.ws = yield from websockets.connect(WS_URL)

	@asyncio.coroutine
	def ensure_ws(self):
		if not self.ws.open:
			yield from self.connect_ws()

	def is_pressed(self):
		self.setup_gpio()
		return not GPIO.input(PIN_SWITCH)

	@asyncio.coroutine
	def check_pressed(self):
		yield from self.ensure_ws()
		state = self.is_pressed()
		if state != self.button_pressed:
			self.button_pressed = state
			if state and not self.speaking:
				self.set_speed(self.SPEED_SOLID)
				yield from self.ws.send(json.dumps({ 'evt': "button:pressed" }))
			else:
				yield from self.ws.send(json.dumps({ 'evt': "button:released" }))

	def check_ws(self):
		message = asyncio.async(self.receive_ws())
		message.add_done_callback(self.got_ws)
	
	@asyncio.coroutine	
	def receive_ws(self):
		yield from self.ensure_ws()
		message = yield from self.ws.recv()
		return message
	
	def got_ws(self, message):
		if message:
			try:
				data = json.loads(message.result())
			except:
				data = False
		if data and ('evt' in data) and (data['evt'] == 'speech:started'):
			self.set_speed(self.SPEED_FAST)
			self.speaking = True
		elif data and ('evt' in data) and (data['evt'] == 'speech:ended'):
			self.set_speed(self.SPEED_SLOW)
			self.speaking = False
		self.check_ws()

	def set_speed(self, speed):
		self.speed = speed

	def flash(self):
		if self.dir == 0:
			self.dir = 1
		elif self.dir == -1 and self.dc <= 0:
			self.dir = 1
		elif self.dir == 1 and self.dc >= 99:
			self.dir = -1
		self.dc += self.dir * self.speed
		self.dc = min(self.dc, 99)
		self.dc = max(self.dc, 0)

	def glow(self):
		self.dc = 99

	def tick(self):
		self.loop.run_until_complete(self.check_pressed())
		self.flash()
		self.light.ChangeDutyCycle(self.dc)

	def stop(self):
		self.light.stop()
		GPIO.cleanup()

button = Button()

def cleanup(signum, frame):
	print('cleanup')
	button.stop()
signal.signal(signal.SIGINT, cleanup)

while True:
	button.tick()
	sleep(0.01)

	
