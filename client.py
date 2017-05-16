#!/usr/bin/env python3

import asyncio
import json
from random import random
from math import floor
from time import sleep
import subprocess
from multiprocessing import Process, Pipe
import websockets
from button import Button

constants = json.loads(open("constants.json").read())

BROWSER_CMD = constants['BROWSER_CMD']
PAIR_CMD = constants['PAIR_CMD']
TTS_CMD = constants['TTS_CMD']
WS_URL = constants['WS_URL']

#subprocess.call(PAIR_CMD)

def flash(pipe):
	b = Button(pipe)
	try:
		while(True):
			b.tick()
			sleep(0.01)
	except:
		b.stop()

class Client():
	def __init__(self):
		self.speaking = False
		#self.speak("introducing Fake News Bot")
		self.pipe = Pipe()
		self.loop = asyncio.get_event_loop()
		self.ws = self.loop.run_until_complete(websockets.connect(WS_URL))

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
		self.flasher = Process(target=flash, args=[self.pipe])
		self.flasher.start()
		self.loop.run_until_complete(asyncio.gather(
			self.receive(),
			self.handle_press()
		))
		self.loop.run_forever()

	@asyncio.coroutine
	def receive(self):
		read, write = self.pipe
		while(True):
			message = yield from self.ws.recv()
			write.send("speech:started")
			self.speaking = True
			try:
				data = json.loads(message)
				print("< {}".format(data['tweet']))
				yield from self.speak(data['tweet'])
			except:
				yield from self.speak("Data corrupted!")

			write.send("speech:ended")
			self.speaking = False
			yield from asyncio.sleep(0.1)

	@asyncio.coroutine
	def handle_press(self):
		read, write = self.pipe
		while(True):
			if read.poll():
				evt = read.recv()
				if evt == 'button:pressed' and not self.speaking:
					yield from self.ws.send(json.dumps({ 'evt': 'button:pressed'}))
			yield from asyncio.sleep(0.1)

#subprocess.Popen(BROWSER_CMD, shell=True)

c = Client()
c.run()



