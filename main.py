from accounts.accounts import Account
from accounts.sqlDB import getTransLog
from accounts.sqlDB import login


test = Account("Pavel", 31, "testtesst.com", "123456", 300)
test.deposit(100)
test.withdraw(30)
test.showTransactions()

