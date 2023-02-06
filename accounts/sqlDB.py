import pymongo
from pymongo import MongoClient
import bcrypt

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

    if check:
        sPass = bcrypt.hashpw(password, bcrypt.gensalt())
        dbInject = {"name": name, "age": age, "email": email, "password": sPass, "balance": balance,
                    "active": active,
                    "transactionLog": transactionList}
        customers.insert_one(dbInject)
        print(password)
    else:
        print("Cannot create account, user already exists")
