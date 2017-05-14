#!/usr/bin/env python3

import asyncio
import json
import websockets

config = json.loads(open("config.json").read())

@asyncio.coroutine
def open():
	ws = yield from websockets.connect(config['WS_URL'])
	while True:
		name = input("ready?")
		yield from ws.send(json.dumps({ 'evt': 'button:pressed'}))
		message = yield from ws.recv()
		data = json.loads(message)
		print("< {}".format(data['tweet']))
	


asyncio.get_event_loop().run_until_complete(open())
asyncio.get_event_loop().run_forever()
