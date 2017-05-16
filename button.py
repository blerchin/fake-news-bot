import RPi.GPIO as GPIO

PIN_LIGHT=17
PIN_SWITCH=27

class Button():
	MODE_SOLID=0
	MODE_SLOW=1
	MODE_FAST=2
	
	def __init__(self, pipe):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(PIN_SWITCH, GPIO.IN,  pull_up_down=GPIO.PUD_UP)
		GPIO.setup(PIN_LIGHT, GPIO.OUT)
		self.light = GPIO.PWM(PIN_LIGHT, 50)
		self.dc = 0
		self.dir = 0
		self.light.start(self.dc)
		self.speed = 2
		self.pipe = pipe
		self.button_pressed = False
	
	def is_pressed(self):
		return not GPIO.input(PIN_SWITCH)
	
	def check_pressed(self):
		read, write = self.pipe
		state = self.is_pressed()
		if state != self.button_pressed:
			self.button_pressed = state
			if state:
				write.send("button:pressed")	
			else:
				write.send("button:released")
			
	
	def set_mode(self, mode):
		if mode.value == self.MODE_SOLID:
			self.set_speed(0)
		elif mode.value == self.MODE_FAST:
			self.set_speed(1)
		else:
			self.set_speed(2)
	
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
		self.flash()
		self.light.ChangeDutyCycle(self.dc)
	
	def stop(self):
		self.light.stop()
		GPIO.cleanup()

