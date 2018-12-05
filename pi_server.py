#coding:utf-8

from socket import *
import cv2
import RPi.GPIO as gpio
from time import sleep
#from components.image_processing import *

ctr_cmds = ['forward', 'backward', 'left', 'right', 'get_video']

HOST = ''
PORT = 12000
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcp_ser_soc = socket(AF_INET, SOCK_STREAM)
tcp_ser_soc.bind(ADDR)
tcp_ser_soc.listen(5)

gpio.setwarnings(False)
gpio.setmode( gpio.BCM)
gpio.setup(14, gpio.OUT, initial= gpio.LOW)

def allum_gpio14():
    while True:
        gpio.output(14, gpio.HIGH)
        sleep(1)
        gpio.output(14, gpio.LOW)
        sleep(1)

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
                allum_gpio14()
                print("Forward")
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
