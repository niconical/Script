from os import path
from subprocess import call
from sys import exit
from getopt import getopt, GetoptError


def print_error(msg):
    print('\n*****ERROR***** %s\n' % msg)


def print_info(msg):
    print('\n*****INFO***** %s\n' % msg)


def exit_with_msg(msg):
    print_error(msg)
    exit(1)


def get_server_info(ext_dir, debug=False):
    # try:
    disk_info = get_disk_info(debug)
    mac_addr, cpu_id = get_cpu_mac(ext_dir, debug)
    ip_addr = get_ip(debug)
    # if (sys.version_info.major > 2):
    #   try:
    #     server_name = input('Please enter the server name: ')
    #     if (debug):
    #       print_info(server_name)
    #   except EOFError:
    #     print_info('Server name is EOF')
    #     server_name = ''
    #   try:
    #     server_type = input('Please enter the device type with a semicolon separate(like asr;tts;en.tts;eval): ')
    #     if (debug):
    #       print_info(server_type)
    #   except EOFError:
    #     print_info('Server type is EOF')
    #     server_type = ''
    # else:
    # try:
    server_name = input('Please enter the server name: ')
    if (debug):
        print_info(server_name)
    # except EOFError:
    #   print_info('Server name is EOF')
    #   server_name = ''
    # try:
    server_type = input(
        'Please enter the device type with a semicolon separate(like asr;tts;en.tts;eval): ')
    if (debug):
        print_info(server_type)
    # except EOFError:
    #   print_info('Server type is EOF')
    #   server_type = ''
    return server_name, cpu_id, disk_info, mac_addr, server_type, ip_addr
    # except KeyboardInterrupt:
    #   print_info('keyboard interrupt by user')
    # except Exception:
    # finally:
    #   print('ERROR')
    #   exit(1)


def get_cpu_mac(ext_dir, debug):
    # FIXME: default read first line as MAC address and the last line as CPUId
    ret = call('gcc %sserver_auth.c' % ext_dir, shell=True)
    if (ret != 0):
        print_error('gcc server auth')
        exit(1)
    if (path.isfile('a.out')):
        call('./a.out', shell=True)
        with open('DEVICE_INFO', 'r') as f:
            lines = f.readlines()
            mac_addr = lines[0][5:]
            cpu_id = lines[-1][5:]
            if (debug):
                print_info('MAC: %s' % mac_addr)
                print_info('CPU: %s' % cpu_id)
        ret = call('sudo rm -f DEVICE_INFO a.out', shell=True)
        if (ret != 0):
            print_error('sudo rm DEVICE INFO')
            exit(1)
        return mac_addr, cpu_id
    else:
        print_error('no a.out file')
        exit(1)


def get_disk_info(debug):
    # TODO: Disk info
    disk_info = ''
    if (debug):
        print_info('Disk: %s' % disk_info)
    return disk_info


def get_ip(debug):
    # TODO: IP address
    ip_addr = ''
    if (debug):
        print_info('IP: %s' % ip_addr)
    return ip_addr


def parseArg(argv):
    try:
        opts, args = getopt(argv, 'hc', ['calc', 'help'])
    except GetoptError:
        exit_with_msg('parse args')
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('deploy or deploy -c or deploy --calc')
            exit_with_msg('arg help')
        elif opt in ('-c', '--calc'):
            return True
