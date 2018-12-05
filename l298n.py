"""
Pilotage du composant l298n
"""
import RPi.GPIO as GPIO
from time import sleep

<<<<<<< HEAD
def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)

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
=======
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
>>>>>>> ea100d364bf5e5ea2db0b1c108f3e4d9cc229537
