import RPi.GPIO as GPIO
from time import sleep

global stop_event


def stop_motor():
	stop_event = True

def forward_pwm():
	stop_event = False
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)
	p = GPIO.PWM(24, 100)
	p.start(100.0)
	while stop_event is False:
		pass
	p.stop()
	GPIO.setup(24, GPIO.LOW)
ctr_cmds = {
	"forward" : forward_pwm,
   	"stop" : stop_motor,
}

