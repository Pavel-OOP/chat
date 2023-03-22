import asyncio

import pymongo
from bson import ObjectId
from pymongo import MongoClient
import hashlib
import passwordz

# client = MongoClient('mongodb://localhost:27017/')
client = MongoClient(
    f'mongodb+srv://Pavkata7000:{passwordz.password}@cluster0.hhmhz.mongodb.net/?retryWrites=true&w=majority')

db = client["accounts"]
customers = db["customers"]


def getUserID(email):
    emailQuery = customers.find({"email": email})
    for x in emailQuery:
        return x.get("_id")


def getUserName2(ids):
    idQuery = customers.find({"_id": ObjectId(ids)})
    for x in idQuery:
        return x.get("name")


def getUserName(email):
    emailQuery = customers.find({"email": email})
    for x in emailQuery:
        return x.get("name")


def switchActive(email, active):
    emailQuery = {"email": email}
    newValues = {"$set": {"active": active}}
    customers.update_one(emailQuery, newValues)
    return active


def getTransLog(email):
    emailQuery = customers.find({"email": email})
    for x in emailQuery:
        return x.get("transactionLog")


def login(email, password):
    emailQuery = customers.find({"email": email})
    for x in emailQuery:
        if x.get("password") == hashlib.sha256((x.get("name") + password).encode()).hexdigest():
            return True
    return False


def updateTransLog(email, transactionList):
    transQuery = {"email": email}
    transQueryNew = {"$set": {"transactionLog": transactionList}}
    customers.update_one(transQuery, transQueryNew)


def insertInDatabase(name, age, email, password, balance, transactionList):
    emailQuery = {"email": email}
    emailQueryRes = customers.find(emailQuery)
    check = True
    for x in emailQueryRes:
        if x.get("email") == email:
            check = False

    if check:
        sPass = hashlib.sha256((name + password).encode())
        dbInject = {"name": name, "age": age, "email": email, "password": sPass.hexdigest(), "balance": balance,
                    "active": True,
                    "transactionLog": transactionList}
        customers.insert_one(dbInject)
        return True
    else:
        print("Cannot create account, user already exists")
        return False
