from accounts.accounts import Account
from accounts.sqlDB import getTransLog
from accounts.sqlDB import login
from accounts.sqlDB import getUserID

test = Account("Pavel", 31, "test@tesst.com", "123456", 300)
test.deposit(100)
test.withdraw(30)
test.showTransactions()
print(getUserID("test@test.com"))

