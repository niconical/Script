import os
import wave
import sys

g_in_file = ''
g_out_file = ''
g_channels = 1
g_samplerate = 16000

def pcm2wav(in_file, out_file):
    print('====> start' + in_file)
    in_file = open(in_file, 'rb')
    out_file = wave.open(out_file, 'wb')

    out_file.setnchannels(int(g_channels))
    out_file.setframerate(int(g_samplerate))
    out_file.setsampwidth(2) # 16bit
    out_file.writeframesraw(in_file.read())
    in_file.close()
    out_file.close()
    print('====> finish' + out_file)

if __name__ == '__main__':
    g_in_file = sys.argv[1]
    g_out_file = g_in_file.split('.')[0] + '.wav'
    g_channels = sys.argv[2]
    g_samplerate = sys.argv[3]
    pcm2wav(g_in_file, g_out_file)
