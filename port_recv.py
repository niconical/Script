# -*- coding: utf-8 -*-

from time import sleep
from serial import Serial
import sys
import os
import time
import threading

if sys.version > '3':
    import queue as Queue
else:
    import Queue


def send(nm=None, fn=None):
    port = Serial(nm, 1000000, timeout=0.5, rtscts=False)
    fo = open(fn, "rb")
    while True:
        line = fo.read(248)
        if not line:
            break
        port.write(line)
        print('print write')
        time.sleep(0.01)
    fo.close()
    port.close()
    pass


def recv(nm=None, fn=None):
    port = Serial(nm, 1000000, timeout=0.5, rtscts=False)
    fo = open(fn, "wb")
    while True:
        len = port.inWaiting()
        if len > 0:
            print(len)
            data = port.read(len)
            fo.write(data)
            fo.flush()
    fo.close()
    port.close()
    pass


if __name__ == '__main__':
    recv(sys.argv[1], sys.argv[2])
