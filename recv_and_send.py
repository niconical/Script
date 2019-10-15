# -*- coding: utf-8 -*-

from time import sleep
from serial import Serial
import sys
import os
import time
import threading
import queue

g_filename_list = []
g_thread_queue = queue.Queue(10)

FEED_FILE_LEN = 256
FEED_FILE_INTERVAL = 0.03

g_serial_nm = ''
g_resource_dir = ''
g_result_dir = ''

UART_SEND_BITRATE = 1000000
UART_RECV_BITRATE = 1000000
RESULT_SUFFIX_NAME = 'pcm'
WAV_HEADER = 44


'''
@brief: open file in folder and each sending FEED_FILE_LEN bytes data at a time FEED_FILE_INTERVAL per interval
'''


def send_single_file2(fn):
    port = Serial(g_serial_nm, UART_SEND_BITRATE, timeout=0.5, rtscts=False)
    print(fn)
    fo = open(fn, "rb")
    fo.seek(WAV_HEADER, 0)
    while True:
        line = fo.read(FEED_FILE_LEN)
        if not line:
            break
        port.write(line)
        time.sleep(FEED_FILE_INTERVAL)
        #port.flush()
    fo.close()
    port.close()


'''
@brief: fill list recurisvly, every item is path+filename
'''


def init_file_list():
    for root, dirs, files in os.walk(g_resource_dir):
        for filename in files:
            g_filename_list.append(os.path.join(root, filename))

def check_result_dir():
    if (os.path.exists(g_result_dir) == True):
        pass
    else:
        os.makedirs(g_result_dir)

'''
@brief: iterate file list and call recv thread
@info: postfix is filename.result, you can change it when necessary
@note: When the sending thread finishes sending, an end instruction is sent.
        At the same time, the receiving thread terminates 
'''


def process_dir(path):
    for filename in g_filename_list:
        threading.Thread(target=recv, args=(filename[:-3] + RESULT_SUFFIX_NAME,)).start()
        send_single_file2(filename)
        is_start = False
        g_thread_queue.put(is_start)


'''
@brief: main process
'''


def process():
    process_dir(g_resource_dir)



'''
@brief: recv function call by recv thread to receive data from UART
'''


def recv(fn):
    fn = g_result_dir + fn[4:]
    fo = open(fn, 'wb')
    port = Serial(g_serial_nm, UART_RECV_BITRATE, timeout=0.5, rtscts=False)
    while True:
        if ((g_thread_queue.empty() == False) and g_thread_queue.get() == False):
            break
        len = port.inWaiting()
        if len > 0:
            print(len)
            data = port.read(len)
            fo.write(data)
            fo.flush()
    fo.close()
    port.close()


'''
@brief: main process to init and start main thread
'''
if __name__ == '__main__':
    g_serial_nm = sys.argv[1]
    g_resource_dir = sys.argv[2]
    g_result_dir = sys.argv[3]
    check_result_dir()
    init_file_list()
    t1 = threading.Thread(target=process)
    t1.start()
