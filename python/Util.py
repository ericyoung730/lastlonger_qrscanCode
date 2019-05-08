import random
import sys
import time

def randHex(size):
    result = ''
    for i in range(0, 9):
        result += str(random.choice("0123456789ABCDEF"))
    return result