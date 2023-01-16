import re

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}'


def check(email):
    if (re.search(regex, email)):
        print("Valid Email")
    else:
        print("Invalid Email")


if __name__ == '__main__':
    email = "rohit.gupta@mcnsolutions.net"
    check(email)

    email = "praveen@c-sharpcorner.com"
    check(email)

    email = "ole@gmail.com1231231,dsadaasdasdadsa"
    check(email)