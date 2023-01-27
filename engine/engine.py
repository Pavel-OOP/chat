from accounts import accounts


def start():
    accounts.Account(str(input("Enter your name: ")), int(input("Enter your age: ")), str(input("Enter your email: ")), str(input("Enter your password: ")))

