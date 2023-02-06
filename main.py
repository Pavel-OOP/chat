from accounts.accounts import Account
# This is a sample Python script.
from engine import engine
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

test = Account("Pavel", 31, "test@test.com", "123456", 300)

test.deposit(100)
test.withdraw(50)
test.showTransactions()

