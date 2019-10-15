# -*- coding: utf-8 -*-

from time import sleep
from serial import Serial
import sys,os
import time

def test(nm=None,fn=None):
    port = Serial(nm,1000000,timeout=0.5,rtscts=False)
    fo=open(fn,"wb+")
    print(port.name)
    print(port.port)
    print(port)
    is_start=1
    outlen=0
    while True:
        data_len=port.in_waiting
        if data_len > 0:
            data=port.read(data_len)
            if is_start == 1:
                ee=b'start'
                i=0
                j=0
                while i<data_len:
                    if data[i:i+1] is ee[j:j+1]:
                        i+=1
                        j+=1
                        while j < 5:
                            if data[i:i+1] is ee[j:j+1]:
                                print("#################%d %d %c %c",i,j,data[i:i+1],ee[j:j+1])
                            else:
                                j = 0
                                break
                            i=i+1
                            j=j+1
                    if j == 5:
                        data=data[5:]
                        print(">>>>>>>>>>>>>>>> %d" %len(data))
                        is_start=0
                        fo.write(data)
                        break
                    i=i+1
            else:
                print("***",end='')
                print(len(data))
                fo.write(data)
    fo.close()
    port.close()
    pass


if __name__=='__main__':
    test(sys.argv[1],sys.argv[2])
