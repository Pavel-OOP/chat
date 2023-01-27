from typing import Final


class Account:
    __slots__ = ['name', 'age', 'email', '_password', "balance", 'active']

    attributes: Final[str] = "'name', 'age', 'email', 'password', 'active'"

    def __init__(self, name="str", age="int", email="str", password="str", balance="int"):
        self.name = name
        self.age = age
        self.email = email
        self._password = password
        self.balance = balance
        self.active = True

    def getName(self):
        return self.name

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

    def withdraw(self, amount):
        if amount > 0:
            self.balance -= amount
