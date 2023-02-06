from typing import Final
import datetime
import pytz
from .sqlDB import insertInDatabase
import bcrypt


class Account:
    @staticmethod
    def _currentTime():
        utcTime = datetime.datetime.utcnow()
        return pytz.utc.localize(utcTime)

    __slots__ = ['_name', 'age', 'email', '__password', "balance", "_transactionList", 'active']

    attributes: Final[str] = "'name', 'age', 'email', 'password', 'active'"

    def __init__(self, name, age, email, password, amount=0):
        self.balance = 0
        self._name = name
        self.age = age
        self.email = email
        self.__password = password.encode()
        self.balance += amount
        self._transactionList = [(self.balance, Account._currentTime(), amount)]
        self.active = True
        insertInDatabase(name, age, email, self.__password, self.balance, self.active, self._transactionList)
        print(f"Account opened with {amount} added to balance")

    def getName(self):
        return self._name

    def getAge(self):
        return self.age

    def getEmail(self):
        return self.email

    def getBalance(self):
        return self.balance

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
        else:
            print("Invalid deposit amount")

    def withdraw(self, amount):
        if self.balance > amount > 0:
            self.balance -= amount
            print(f"Withdrawn -{amount}, new balance:{self.showBalance()}")
            self._transactionList.append((self.balance, Account._currentTime(), -amount))
        else:
            print("Invalid withdrawal amount, your current balance is: {}".format(self.balance))

    def showBalance(self):
        return self.balance

    def showTransactions(self):
        # self.__transactionList.pop()
        for bal, date, amount in self._transactionList:
            if amount > 0:
                transType = "deposited"
            else:
                transType = "withdrawn"
            print("{:4} are {} on {} [local time: {}] your new Balance is: {}".format(amount, transType, date,
                                                                                      Account._currentTime(), bal))
