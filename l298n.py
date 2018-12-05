"""
Pilotage du composant l298n
"""
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)

GPIO.output(7, True)
time.sleep(1)
GPIO.output(11, False)
GPIO.output(13, True)
time.sleep(1)
GPIO.output(13, False)
GPIO.output(15, True)
time.sleep(1)
GPIO.output(15, False)
GPIO.cleanup()
