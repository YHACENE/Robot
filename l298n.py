"""
Pilotage du composant l298n
"""
import RPi.GPIO as GPIO
from time import sleep


def init_gpio():
    print ("init")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)

def forward(tf):
    print("forward")
    init_gpio()
    GPIO.output(17, GPIO.LOW)
    GPIO.output(22, GPIO.HIGH)
    GPIO.output(23, GPIO.LOW)
    GPIO.output(24, GPIO.HIGH)
    sleep(tf)
    GPIO.cleanup()

def backward(tf):
    init_gpio()
    GPIO.output(17, GPIO.HIGH)
    GPIO.output(22, GPIO.LOW)
    GPIO.output(23, GPIO.HIGH)
    GPIO.output(24, GPIO.LOW)
    sleep(tf)
    GPIO.cleanup()

def left(tf):
    init_gpio()
    p = GPIO.PWM(24, 400)
    GPIO.output(17, GPIO.HIGH)
    GPIO.output(22, GPIO.LOW)
    GPIO.output(23, GPIO.LOW)
    GPIO.output(24, GPIO.LOW)
    sleep(tf)
    GPIO.cleanup()
    p.stop()

def right(tf):
    init_gpio()
    GPIO.output(17, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
    GPIO.output(23, GPIO.LOW)
    GPIO.output(24, GPIO.HIGH)
    sleep(tf)
    GPIO.cleanup()
#print("Forward")
#forward(4)
#print("Backward")
#backward(4)
