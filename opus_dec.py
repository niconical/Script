import os
import subprocess
import sys

g_filename_list = []


def init_file_list(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            g_filename_list.append(os.path.join(root, filename))


def print_fn():
    for fn in g_filename_list:
        print(fn)


def process():
    for filename in g_filename_list:
        cmd = './opus_dec ' + filename + ' ret2/' + filename[4:-11] + '.pcm'
        ret = subprocess.call(cmd, shell=True)
        if (ret != 0):
            print('ERROR!')
            exit(1)


if __name__ == "__main__":
    init_file_list('ret/')
    process()
