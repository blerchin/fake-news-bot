#!/usr/bin/env python3

import asyncio
import json
from random import random
from math import floor
import subprocess
import websockets

constants = json.loads(open("constants.json").read())

BROWSER_CMD = constants['BROWSER_CMD']
PAIR_CMD = constants['PAIR_CMD']
TTS_CMD = constants['TTS_CMD']
WS_URL = constants['WS_URL']

#subprocess.call(PAIR_CMD)

def speak(text):
	if(random() < 0.5):
		gender = 'm'
	else:
		gender = 'f'
	num = floor(random() * 5)
	voice = "{}{}".format(gender, num)
	subprocess.call([TTS_CMD, text, voice])

#speak("introducing Fake News Bot")

@asyncio.coroutine
def send(ws):
	while(True):
		input("ready?")
		yield from asyncio.sleep(10)
		yield from ws.send(json.dumps({ 'evt': 'button:pressed'}))

asyncio.coroutine
def receive(ws):
	while(True):
		message = yield from ws.recv()
		try:
			data = json.loads(message)
			print("< {}".format(data['tweet']))
			speak(data['tweet'])
		except:
			speak("Data corrupted!")


subprocess.Popen(BROWSER_CMD, shell=True)

loop = asyncio.get_event_loop()
ws = loop.run_until_complete(websockets.connect(WS_URL))
loop.run_until_complete(asyncio.gather(
	send(ws),
	receive(ws)
))
loop.run_forever()

