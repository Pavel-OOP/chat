import socket
import threading
from accounts import sqlDB
import hashlib

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))

server.listen(5)


def handleConnection(c):
    c.send("Email: ".encode())
    email = c.recv(1024).decode()
    c.send("Password: ".encode())
    password = c.recv(1024).decode()
    if sqlDB.login(email, password):
        c.send("Login successful!".encode())
    else:
        c.send("Login failed, please check credentials and try again!".encode())


while True:
    client, addr = server.accept()
    print(f"Connected to {addr}")
    threading.Thread(target=handleConnection, args=(client,)).start()
