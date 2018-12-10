"""
Pilotage du composant l298n
"""
import RPi.GPIO as GPIO
from time import sleep


def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)

def forward(tf):
    init_gpio()
    GPIO.output(17, False)
    GPIO.output(22, True)
    GPIO.output(23, False)
    GPIO.output(24, True)
    sleep(tf)
    GPIO.cleanup()

def backward(tf):
    init_gpio()
    GPIO.output(17, True)
    GPIO.output(22, False)
    GPIO.output(23, True)
    GPIO.output(24, False)
    sleep(tf)
    GPIO.cleanup()

print("Forward")
forward(4)
print("Backward")
backward(4)
