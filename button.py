#!/usr/bin/env python3

import os
import signal
import RPi.GPIO as GPIO
from time import sleep, time
from tweet import tweet
from tts import speak


PIN_LIGHT=17
PIN_SWITCH=27
FLASH_INTERVAL = 5

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
		self.time_pressed = time() - FLASH_INTERVAL
		self.button_pressed = False
		self.stopped = False
	
	def setup_gpio(self):
		GPIO.setmode(GPIO.BCM)
	
	def is_running(self):
		return not self.stopped

	def is_pressed(self):
		return not GPIO.input(PIN_SWITCH)

	def check_pressed(self):
		state = self.is_pressed()
		if state != self.button_pressed:
			self.button_pressed = state
			if state:
				self.send_tweet()
				self.time_pressed = time()
	def send_tweet(self):
		message = tweet()
		speak(message)
	
	def check_speed(self):
		if self.button_pressed:
			self.set_speed(self.SPEED_SOLID)
		elif time() - self.time_pressed < FLASH_INTERVAL:
			self.set_speed(self.SPEED_FAST)
		else:
			self.set_speed(self.SPEED_SLOW)

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
		self.check_pressed()
		self.check_speed()
		self.flash()
		self.light.ChangeDutyCycle(self.dc)

	def stop(self):
		self.stopped = True
		self.light.stop()
		GPIO.cleanup()

button = Button()

def cleanup(signum, frame):
	print('cleanup')
	button.stop()
signal.signal(signal.SIGINT, cleanup)

while button.is_running():
	button.tick()
	sleep(0.01)

	
