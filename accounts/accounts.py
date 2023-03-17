from typing import Final
import datetime
import pytz
from .sqlDB import insertInDatabase, getTransLog
from .sqlDB import updateTransLog
import re
import asyncio


def isValidEmail(email):
    emailRegex = re.compile(r'^[a-zA-Z0-9]{3,}[-]?\@[a-zA-Z0-9]{3,}[-]?\.[a-zA-Z]{2,}$')
    return bool(emailRegex.match(email))


def validateName(name):
    nameRegex = re.compile(r"^[A-Za-z]+(([',. -][A-Za-z ])?[A-Za-z]*)*$")
    return bool(nameRegex.match(name))





class Account:
    @staticmethod
    def _currentTime():
        utcTime = datetime.datetime.utcnow()
        return str(pytz.utc.localize(utcTime)).split(".")[0]

    __slots__ = ['_name', 'age', 'email', '__password', "balance", "_transactionList", 'active']

    attributes: Final[str] = "'name', 'age', 'email', 'password'"

    def __init__(self, name, age, email, password, amount=0):
        self.balance = 0
        if validateName(name):
            self._name = name
        else:
            raise Exception("Name is invalid!")
        self.age = age
        if isValidEmail(email):
            self.email = email
        else:
            raise Exception("The email provided is invalid!")
        self.__password = password
        self.balance += int(amount)
        self._transactionList = [(self.balance, Account._currentTime(), amount)]
        self.active = bool(insertInDatabase(name, age, email, self.__password, self.balance,
                                            self._transactionList))
        insertInDatabase(name, age, email, self.__password, self.balance,
                         self._transactionList)
        print(f"Account opened with {amount} added to balance")

    def getName(self):
        return self._name

    def getAge(self):
        return self.age

    def getEmail(self):
        return self.email

    def getBalance(self):
        return self.balance

    def isActive(self):
        return self.active

    def switchToEnabledOrDisabled(self):
        if self.active:
            self.active = False
        elif not self.active:
            self.active = True

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited {amount}, new balance:{self.showBalance()}")
            self._transactionList.append((self.balance, Account._currentTime(), amount))
            updateTransLog(self.getEmail(), self._transactionList)
        else:
            print("Invalid deposit amount")

    def withdraw(self, amount):
        if self.balance > amount > 0:
            self.balance -= amount
            print(f"Withdrawn -{amount}, new balance:{self.showBalance()}")
            self._transactionList.append((self.balance, Account._currentTime(), -amount))
            updateTransLog(self.getEmail(), self._transactionList)
        else:
            print("Invalid withdrawal amount, your current balance is: {}".format(self.balance))

    def showBalance(self):
        return self.balance

    def showTransactions(self):
        for bal, date, amount in getTransLog(self.getEmail()):
            if amount > 0:
                transType = "deposited"
            else:
                transType = "withdrawn"
            print("{:4} are {} on {} [local time: {}] your new Balance is: {}".format(amount, transType, date,
                                                                                      Account._currentTime(), bal))
