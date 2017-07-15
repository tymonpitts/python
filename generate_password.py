#! /usr/bin/python
from random import choice

charsets = [
    'abcdefghijklmnopqrstuvwxyz',
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    '0123456789',
    '^!\$%&/()=?{[]}+~#-_.:,;<>|\\',
    ]


def mkpassword(length=16):
    pwd = ''
    charset = choice(charsets)
    while len(pwd) < length:
        pwd += choice(charset)
        charset = choice(list(set(charsets) - set([charset])))
    return pwd


if __name__ == '__main__':
    print mkpassword(8)
