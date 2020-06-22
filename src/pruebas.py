
import time
import progressbar
from pip._vendor.msgpack.fallback import xrange

if __name__ == '__main__':

    entero = 3

    size = 8

    a = bin(entero)

    corte = len(a) - size

    new_str = a[corte:]

    while len(new_str) < size:
        new_str = '0' + new_str

    new_str = new_str.replace('b', '0')

    print(new_str)















