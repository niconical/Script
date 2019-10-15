from getopt import getopt, GetoptError
import sys
# # import simplejson as json
# # def readEOF():
# #   try:
# #     server_name = input('Please enter the server name: ')
# #   except EOFError:
# #     pass
# #   server_type = input('Please enter the device type with a semicolon separate(like asr;tts.): ')
# #   print('test exit')
# #   return server_name, server_type

# # def checkJSON():
# #   ext_object = json.load(open('./ext.json','r'))
# #   if (ext_object['debug_mode'] == False):
# #     print('bool false')
# #   elif (ext_object['debug_mode'] == True):
# #     print('bool true')
# #   elif (ext_object['debug_mode'] == 'false'):
# #     print('str false')
# #   else:
# #     print('error')
# import os
# import subprocess

# def get_cpu_mac():
#   subprocess.call('sudo gcc ./server_auth.c',shell=True)
#   if (os.path.isfile('a.out')):
#     subprocess.call('sudo ./a.out',shell=True)
#     with open('DEVICE_INFO', 'r') as f:
#       lines = f.readlines()
#       mac_addr = lines[0][5:]
#       cpu_id = lines[-1][5:]
#       return mac_addr,cpu_id
#   else:
#     print('no file')


# def parseArg(argv):
#     try:
#         opts, args = getopt.getopt(argv, "hc", ['calc','help'])
#     except getopt.GetoptError:
#         print('deploy [options]')
#         sys.exit(2)
#     for opt, arg in opts:
#         if opt == '-h':
#             print('deploy [options]')
#             sys.exit()
#         elif opt in ("-c", "--calc"):
#             print('calc')


# def parseArg(argv, ret):
#     try:
#         opts, args = getopt(argv, 'hc', ['calc', 'help'])
#     except GetoptError:
#         print('error')
#     for opt, arg in opts:
#         if opt in ('-h', '--help'):
#             print('deploy or deploy -c or deploy --calc')
#         elif opt in ('-c', '--calc'):
#             print(opt)
#             ret = True


# if __name__ == "__main__":
#     isCalc = False
#     parseArg(sys.argv[1:], isCalc)
#     print(isCalc)
