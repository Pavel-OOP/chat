import pymongo
from pymongo import MongoClient
import bcrypt

client = MongoClient('mongodb://localhost:27017/')

db = client["accounts"]
customers = db["customers"]


def insertInDatabase(name, age, email, password, balance, active):
    sPass = bcrypt.hashpw(password, bcrypt.gensalt())
    dbInject = {"name": name, "age": age, "email": email, "password": sPass, "balance": balance, "active": active}
    customers.insert_one(dbInject)

