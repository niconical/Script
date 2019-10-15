# coding=utf-8
import sys
from os import path
from simplejson import load
from subprocess import call
from cloud import login
from cloud import add_server
from requests import Session
from utility import exit_with_msg
from utility import print_info
from utility import print_error
from utility import parseArg


def assert_ext(ext_file):
    if (path.isfile(ext_file) == False):
        exit_with_msg('file ext.json does not exist.')


def create_and_exec_install_shell(ext_object):
    try:
        cmd = '#!/bin/bash\nsudo apt-get update\n'
        for package_name in ext_object['install_packages']:
            cmd += 'sudo apt-get install -y %s\n' % package_name
        install_shell = open('./install.sh', 'w+')
        cmd += '\n'
        install_shell.write(cmd)
        install_shell.close()
        ret = call('sudo chmod a+x install.sh', shell=True)
        if (ret != 0):
            exit_with_msg('chmod for install')
        ret = call('./install.sh', shell=True)
        if (ret != 0):
            exit_with_msg('exec install.sh')
        ret = call('sudo rm -f install.sh', shell=True)
        if (ret != 0):
            exit_with_msg('rm install.sh')
    except KeyboardInterrupt:
        print_info('Keyboard interrupt by user - when install shell')
        sys.exit(1)
    except IOError:
        print_error('IO Error - when install shell')
        sys.exit(1)


def dowload_compile_and_install_libiconv():
    try:
        cmd = "axel https://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.15.tar.gz\n \
    tar -xvf libiconv-1.15.tar.gz\n \
    cd libiconv-1.15\n \
    sudo ./configure --prefix=/usr/local\n \
    sudo make\n \
    sudo make install\n \
    cd -\n \
    sudo rm libiconv* -rf\n \
    sudo ldconfig"
        ret = call(cmd, shell=True)
        if (ret != 0):
            exit_with_msg('install libiconv')
    except KeyboardInterrupt:
        print_info('Keyboard interrupt by user')
        sys.exit(1)


def ln_hiredis():
    cmd = 'sudo ln -s /usr/lib/x86_64-linux-gnu/libhiredis.so.0.10 /usr/lib/x86_64-linux-gnu/libhiredis.so.0.13'
    ret = call(cmd, shell=True)
    return ret


def link_hiredis(ext_dir):
    try:
        if (path.isfile('/usr/lib/x86_64-linux-gnu/libhiredis.so.0.13')):
            return
        if (path.isfile('/usr/lib/x86_64-linux-gnu/libhiredis.so.0.10')):
            ret = ln_hiredis()
            if (ret != 0):
                exit_with_msg('Link hiredis')
        else:
            cmd = 'sudo cp %slibhiredis.so.0.10 /usr/lib/x86_64-linux-gnu' % ext_dir
            ret = call(cmd, shell=True)
            if (ret != 0):
                exit_with_msg('cp libhiredis.so')
            else:
                ret = ln_hiredis()
                if (ret != 0):
                    exit_with_msg('Link hiredis')
    except KeyboardInterrupt:
        print_info('Keyboard interrupt by user')
        sys.exit(1)


if __name__ == "__main__":
    isCalc = False
    isCalc = parseArg(sys.argv[1:])
    ext_dir = '../ext/'
    assert_ext(ext_dir + 'ext.json')
    ext_object = load(open(ext_dir + 'ext.json', 'r'))
    create_and_exec_install_shell(ext_object)
    session = Session()
    ret = login(session, ext_object['cloud_login_url'], ext_object['cloud_username'],
                ext_object['cloud_password'], debug=ext_object['debug_mode'])
    if (ret):
        print_info('Login success')
        ret = add_server(
            session, ext_object['cloud_add_server_url'], ext_dir, debug=ext_object['debug_mode'])
        if (ret):
            print_info('Add server success')
        else:
            exit_with_msg('Add server fail')
    else:
        exit_with_msg('Login fail')
    if (isCalc == False):
        link_hiredis(ext_dir)
        dowload_compile_and_install_libiconv()
