#!/usr/bin/env python3

import asyncio
import json
from random import random
from math import floor
from time import sleep
import subprocess
import os
import websockets

constants = json.loads(open("constants.json").read())

PULSEAUDIO_INIT = constants['PULSEAUDIO_INIT']
subprocess.call(PULSEAUDIO_INIT)
TTS_CMD = constants['TTS_CMD']
WS_URL = os.environ['BOT_SOCKET_URL']

class Client():
	def __init__(self):
		self.speaking = False
		#self.speak("introducing Fake News Bot")
		self.loop = asyncio.get_event_loop()

	@asyncio.coroutine
	def connect_ws(self):
		self.ws = yield from websockets.connect(WS_URL)

	@asyncio.coroutine
	def ensure_ws(self):
		if not self.ws.open:
			yield from self.connect_ws()
	
	@asyncio.coroutine
	def write_ws(self, obj):
		yield from self.ensure_ws()
		yield from self.ws.send(json.dumps(obj))

	@asyncio.coroutine
	def speak(self, text):
		if(random() < 0.5):
			gender = 'm'
		else:
			gender = 'f'
		num = floor(random() * 5)
		voice = "{}{}".format(gender, num)
		proc = subprocess.Popen([TTS_CMD, text, voice])
		while(proc.poll() == None):
			yield from asyncio.sleep(0.1)

	def run(self):
		self.loop.run_until_complete(self.connect_ws())
		self.loop.run_until_complete(self.receive())
		self.loop.run_forever()

	@asyncio.coroutine
	def receive(self):
		while(True):
			yield from self.ensure_ws()
			message = yield from self.ws.recv()
			if message:
				try:
					data = json.loads(message)
				except:
					continue
			if data and 'tweet' in data:
				yield from self.write_ws({ 'evt': 'speech:started' })
				print("< {}".format(data['tweet']))

				yield from self.speak(data['tweet'])

				yield from self.write_ws({ 'evt': 'speech:ended' })
				yield from asyncio.sleep(0.1)

c = Client()
c.run()
