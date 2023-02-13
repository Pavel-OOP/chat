import socket
from accounts import accounts

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

input1 = input("Do you have an account? y/n: ")
client.send(input1.encode())

if input1 == "y":
    email = client.recv(1024).decode()
    print(f"recv '{email}' at {accounts.Account._currentTime()}")
    client.send(input(email).encode())
    password = client.recv(1024).decode()
    print(f"recv '{password}' at {accounts.Account._currentTime()}")
    client.send(input(password).encode())
    print(client.recv(1024).decode())
    client.close()
else:
    client.send(input("Name: ").encode())
    client.send(input("Age: ").encode())
    client.send(input("Email: ").encode())
    client.send(input("Password: ").encode())
    client.send(input("Amount to deposit: ").encode())
