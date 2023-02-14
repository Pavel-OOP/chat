from accounts.accounts import Account
from accounts.sqlDB import getTransLog
from accounts.sqlDB import login
from accounts.sqlDB import getUserID

test = Account("Georgi", 32, "georgi@test.com", "123456", 1000)
test.deposit(100)
test.withdraw(30)
print(login("georgi@test.com", "123756"))


