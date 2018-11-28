#coding:utf-8

import socket

host, port = ('', 5566)

BUFSIZE = 1024

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((host, port))
print("Le serveur est démarré ...")

while True:
    socket.listen(5)
    conn, address = socket.accept()
    print("En écoute ...")
    print("Connected from: ", address)

    command = conn.recv(BUFSIZE)
    command = command.decode("utf8")
    print(command)
conn.close()
socket.close()
