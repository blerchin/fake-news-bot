import RPi.GPIO as GPIO

PIN_LIGHT=17
PIN_SWITCH=27
FAST_FLASH_DURATION=5

class Button():
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(PIN_SWITCH, GPIO.IN,  pull_up_down=GPIO.PUD_UP)
		GPIO.setup(PIN_LIGHT, GPIO.OUT)
		self.light = GPIO.PWM(PIN_LIGHT, 50)
		self.dc = 0
		self.dir = 0
		self.light.start(self.dc)
		self.speed = 2
	
	def is_pressed(self):
		return not GPIO.input(PIN_SWITCH)
	
	def set_speed(self, speed):
		self.speed = speed

	def flash(self, speed = 1):
		if self.dir == 0:
			self.dir = 1
		elif self.dir == -1 and self.dc <= 0:
			self.dir = 1
		elif self.dir == 1 and self.dc >= 99:
			self.dir = -1
		self.dc += self.dir * speed
		self.dc = min(self.dc, 99)
		self.dc = max(self.dc, 0)

	def glow(self):
		self.dc = 99
	
	def tick(self):
		if self.is_pressed():
			self.glow()
		else:
			self.flash(self.speed)
		self.light.ChangeDutyCycle(self.dc)
	
	def stop(self):
		self.light.stop()
		GPIO.cleanup()
	
