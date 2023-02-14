import socket
import threading
from accounts import sqlDB
from accounts import accounts


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))

server.listen(5)


def handleConnection(c):
    loginOrRegister = c.recv(1024).decode()
    if loginOrRegister == "y":
        c.send("Email: ".encode())
        email = c.recv(1024).decode()
        print(f"email received - '{email}' at {accounts.Account._currentTime()}")
        c.send("Password: ".encode())
        password = c.recv(1024).decode()
        print(f"password received  - '{password}' at {accounts.Account._currentTime()}")
        if sqlDB.login(email, password):
            c.send("Login successful!".encode())
            print(c.recv(1024).decode())
        else:
            c.send("Login failed, please check credentials and try again!".encode())
    else:
        name = c.recv(1024).decode()
        age = c.recv(1024).decode()
        email = c.recv(1024).decode()
        password = c.recv(1024).decode()
        amount = c.recv(1024).decode()
        accounts.Account(name, age, email, password, amount)


while True:
    client, addr = server.accept()
    print(f"1 Connected to {addr} - {accounts.Account._currentTime()}")
    threading.Thread(target=handleConnection, args=(client,)).start()
