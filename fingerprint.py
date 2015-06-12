import Adafruit_BBIO.UART as UART
import serial
import binascii as b
from ctypes import *
import sys
import time
s_dormant = "\xf5\x2c\x00\x00\x00\x00\x2c\xf5"
s_addmode = "\xf5\x2d\x00\x01\x00\x00\x2c\xf5"
s_add1 = "\xf5\x01\x00\x01\x01\x00\x01\xf5"

SUCCESS = '00'
FAIL = '01'
FULL = '04'
NOUSER = '05'
USER_EXIST = '07'
TIME_OUT = '08'
# user1, user2 is '\x01' format
def decode(x, y):
    return ord(x)*(16**2)+ord(y)

def encode(x):
    p1 = x/(16**2)
    p2 = x-p1*(16**2)
    return b.b2a_hex(chr(p1))+b.b2a_hex(chr(p2))

def chk(s):
    temp = []
    for ss in s:
        temp.append(ord(ss))
    temp[6] = temp[1]^temp[2]^temp[3]^temp[4]^temp[5]
    return temp


def communication(cmd):
    for s in cmd:
        ser.write(chr(s))
    response = ser.read(8)
    return response

def communication_h(cmd):
    for s in cmd:
        ser.write(chr(s))
    s = ser.read(1)
    s = ''
    response = ''
    while s == '\xf5':
        response = response+ser.read(1)
    return response

def print_response(response):
    for s in response:
        print b.b2a_hex(s)+' ',
    print ''

def delete_all():
    s_delete_all = b.a2b_hex('f505000000002cf5')
    s_delete_all = chk(s_delete_all)
    response = communication(s_delete_all)
    print_response(response)
    return print_q(response, [1, 1, 0, 0, 0, 0, 0, 0, 0])

def dormant():
    s_dormant = b.a2b_hex('f52c000000002cf5')
    s_dormant = chk(s_dormant)
    response = communication(s_dormant)
    print_response(response)
    return print_q(response, [1, 1, 0, 0, 0, 0, 0, 0, 0])

def add(user):
    add_mode = b.a2b_hex('f52d000100002cf5')
    add_mode = chk(add_mode)
    s_add1 = b.a2b_hex('f501'+encode(user)+'010000f5')
    s_add1 = chk(s_add1)
    s_add2 = b.a2b_hex('f502'+encode(user)+'010000f5')
    s_add2 = chk(s_add2)
    s_add3 = b.a2b_hex('f503'+encode(user)+'010000f5')
    s_add3 = chk(s_add3)
    response = communication(add_mode)
    print_response(response)
    if print_q(response, [1, 1, 0, 0, 0, 0, 0, 0, 0]) != 'ACK_SUCCESS':
        return print_q(response, [1, 1, 0, 0, 0, 0, 0, 0, 0])
    response = communication(s_add1)
    print_response(response)
    if print_q(response, [1, 1, 0, 0, 1, 0, 0, 0, 1]) != 'ACK_SUCCESS':
        return print_q(response, [1, 1, 0, 0, 1, 0, 0, 0, 1])
    response = communication(s_add2)
    print_response(response)
    if print_q(response, [1, 0, 0, 0, 0, 0, 0, 0, 1]) != 'ACK_SUCCESS':
        return print_q(response, [1, 0, 0, 0, 0, 0, 0, 0, 1])
    response = communication(s_add3)
    print_response(response)
    return 'ACK_SUCCESS'

def compare_n():
    s_compare = b.a2b_hex('f50c000000002cf5')
    s_compare = chk(s_compare)
    response = communication(s_compare)
    print_response(response)
    if print_q(response, [0, 0, 0, 0, 0, 1, 0, 0, 1]) != 'ACK_SUCCESS':
        return print_q(response, [0, 0, 0, 0, 0, 1, 0, 0, 1])
    return decode(response[2], response[3])

def delete_user(user):
    s_delete_user = b.a2b_hex('f504'+encode(user)+'00002cf5')
    s_delete_user = chk(s_delete_user)
    response = communication(s_delete_user)
    print_response(response)
    if print_q(response, [1, 1, 0, 0, 0, 0, 0, 0, 0]) != 'ACK_SUCCESS':
        return print_q(response, [1, 1, 0, 0, 0, 0, 0, 0, 0])
    return 'ACK_SUCCESS'

def version():
    s = b.a2b_hex('f5260000000000f5')
    s = chk(s)
    response = communication_h(s)
    print_response(response)

def total_num():
    s = b.a2b_hex('f5090000000000f5')
    s = chk(s)
    response = communication(s)
    print_response(response)
    if print_q(response, [1, 1, 0, 0, 0, 0, 0, 0, 0]) != 'ACK_SUCCESS':
        return print_q(response, [1, 1, 0, 0, 0, 0, 0, 0, 0])
    return decode(response[2], response[3])

def print_privilege(s):
    q = s[4]
    print 'user privilege: ',
    print ord(s[4])

def print_q(s, check):
    q = s[4]
    cmd = s[1]
    if q == '\x00' and check[0] == 1:
        return 'ACK_SUCCESS'
    elif q == '\x01' and check[1] == 1:
        return 'ACK_FAIL'
    elif q == '\x04' and check[4] == 1:
        return 'ACK_FULL'
    elif q == '\x05' and check[5] == 1:
        return 'ACK_NOUSER'
    elif q == '\x07' and check[7] == 1:
        return 'ACK_USER_EXIST'
    elif q == '\x08' and check[8] == 1:
        return 'ACK_TIMEOUT'
    else :
        return 'ACK_SUCCESS'


UART.setup("UART4")
ser = serial.Serial(port="/dev/ttyO4", baudrate=19200)
ser.close()
ser.open()

def close():
    ser.close()
#    if ser.isOpen() :
#        print "Serial is open!"
#        print total_num()
#        delete_user(compare_n())
#    ser.close()
