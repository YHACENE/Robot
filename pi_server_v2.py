#!/usr/bin/python
#coding:utf-8

from socket import *
from time import sleep
import threading
from l298n import *

HOST = ''
PORT = 12000
BUFSIZE = 1024
ADDR = (HOST, PORT)
ctr_cmds = {
        "forward" : forward,
        "backward" : backward,
        "left" : left,
        "right" : right
}
class MyServer(threading.Thread):
	def __init__(self, ip, port, clientsocket):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.clientsocket = clientsocket
		print("[+] Nouveau thread pour %s %s %s" % (self.ip, self.port,getThreadId(), ))

	def run(self):
		print("Connexion de %s %s" % (self.ip, self.port, ))
		cmd = ctr_cmds.get(self.clientsocket.recv(BUFSIZE), None)

		try:
			if cmd is not None:
				cmd(5)

		except KeyboardInterrupt as e:
			print("#ERROR: {}".format(e))

tcpsock = socket(AF_INET, SOCK_STREAM)
tcpsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpsock.bind(ADDR)

if __name__ == "__main__":
	while  True:
		tcpsock.listen(10)
		print( "En écoute...")
		(clientsocket, (ip, port)) = tcpsock.accept()
		newthread = MyServer(ip, port, clientsocket)
		newthread.start()
