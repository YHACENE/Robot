#coding:utf-8

from socket import *
import cv2
import RPi.GPIO as GPIO
from components.image_processing import *
from time import sleep

ctr_cmds = ['forward', 'backward', 'left', 'right', 'get_video']


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)

def allume():
    while True:
        GPIO.output(14, GPIO.HIGH)
        sleep(1)
        GPIO.output(14, GPIO.LOW)
        sleep(1)



HOST = ''
PORT = 5566
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcp_ser_soc = socket(AF_INET, SOCK_STREAM)
tcp_ser_soc.bind(ADDR)
tcp_ser_soc.listen(5)

while True:
    print("Waiting for connection ...")
    tcp_cli_soc, addr = tcp_ser_soc.accept()
    print("Connected from: {}".format(addr))
    try:
        while True:
            cmd = ''
            cmd = tcp_cli_soc.recv(BUFSIZE)
            cmd = cmd.decode("utf8")

            if not cmd:
                break;
            if cmd == ctr_cmds[0]:
                print("Forward")
                allume()
            if cmd == ctr_cmds[1]:
                print("Backward")
            if cmd == ctr_cmds[2]:
                print("Left")
            if cmd == ctr_cmds[3]:
                print("Right")
            if cmd == ctr_cmds[4]:
                print("Sending ...")

    except KeyboardInterrupt as e:
        print("#ERROR: {}".format(e))
tcp_cli_soc.close()
tcp_ser_soc.close()
