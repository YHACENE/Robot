"""
Pilotage du composant l298n
"""
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(20, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)

GPIO.output(20, GPIO.HIGH)
sleep(5)
GPIO.output(20, GPIO.LOW)
sleep(5)
GPIO.output(26, GPIO.HIGH)
sleep(5)
GPIO.output(26, GPIO.LOW)
GPIO.cleanup()
