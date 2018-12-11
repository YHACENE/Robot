#coding:utf-8

from socket import *
import cv2
from l298n import *

ctr_cmds = ['forward', 'backward', 'left', 'right', 'get_video']

HOST = ''
PORT = 12000
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
                forward(2)
            if cmd == ctr_cmds[1]:
                backward(2)
            if cmd == ctr_cmds[2]:
                left(2)
            if cmd == ctr_cmds[3]:
                right(2)
            if cmd == ctr_cmds[4]:
                print("Sending ...")

    except KeyboardInterrupt as e:
        print("#ERROR: {}".format(e))
tcp_cli_soc.close()
tcp_ser_soc.close()
