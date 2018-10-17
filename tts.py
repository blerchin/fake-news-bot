#!/usr/bin/env python3

import json
from random import random
from math import floor
from time import sleep
import subprocess

constants = json.loads(open("constants.json").read())

PULSEAUDIO_INIT = constants['PULSEAUDIO_INIT']
subprocess.call(PULSEAUDIO_INIT)
TTS_CMD = constants['TTS_CMD']

def speak(text):
	print("speaking " + text)
	if(random() < 0.5):
		gender = 'm'
	else:
		gender = 'f'
	num = floor(random() * 5)
	voice = "{}{}".format(gender, num)
	proc = subprocess.Popen([TTS_CMD, text, voice])
	while(proc.poll() == None):
		sleep(0.01)
