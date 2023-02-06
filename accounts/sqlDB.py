import pymongo
from pymongo import MongoClient
import bcrypt
import hashlib

client = MongoClient('mongodb://localhost:27017/')
# client = mongodb+srv://Pavkata7000:<password>@cluster0.hhmhz.mongodb.net/?retryWrites=true&w=majority

db = client["accounts"]
customers = db["customers"]


def insertInDatabase(name, age, email, password, balance, active, transactionList):
    emailQuery = {"email": email}
    emailQueryRes = customers.find(emailQuery)
    check = True
    for x in emailQueryRes:
        if x.get("email") == email:
            check = False
        elif x.get("name") == name and x.get("age") == age:
            prompt = input("Are you sure you don't already have an account and you can't find the credentials? y/n:")
            if prompt == "n":
                print("Please try to find your email and password!")
                check = False
    if check:
        sPass = hashlib.sha256(password.encode())
        dbInject = {"name": name, "age": age, "email": email, "password": sPass.hexdigest(), "balance": balance,
                    "active": active,
                    "transactionLog": transactionList}
        customers.insert_one(dbInject)
    else:
        print("Cannot create account, user already exists")
