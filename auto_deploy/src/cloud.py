# coding=utf-8
from re import compile
from utility import get_server_info
from utility import print_error
from utility import print_info

user_headers = {"Host": "cloud.qdreamer.com",
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
                "Accept-Encoding": "gzip, deflate"
                }


def get_csrf_token(session, url):
    resp = session.get(url, headers=user_headers)
    reg = r"<input type='hidden' name='csrfmiddlewaretoken' value='(.*)' />"
    pattern = compile(reg)
    return pattern.findall(resp.content.decode('utf-8'))[0]


def search_element(resp, html_element):
    pattern = compile(html_element)
    result = pattern.findall(resp.content.decode('utf-8'))
    if (len(result) != 0):
        return True
    else:
        return False


def add_server(session, url, ext_dir, debug=False):
    server_name, cpu_id, disk_info, mac_addr, server_type, ip_addr = get_server_info(ext_dir,
                                                                                     debug)
    user_files = {
        "csrfmiddlewaretoken": (None, get_csrf_token(session, url)),
        "name": (None, server_name),
        "cpu": (None, cpu_id),
        "disk": (None, disk_info),
        "mac": (None, mac_addr),
        "service_type": (None, server_type),
        "ip": (None, ip_addr),
        "_save": (None, "Save")
    }
    r = session.post(url, files=user_files)
    ret = search_element(r, '<ul class="errorlist"><li>')
    if (ret == True and debug):
        print_error('Same MAC address with other server')
        return False
    return True


def login(session, url, username, password, debug=False):
    user_data = {"csrfmiddlewaretoken": get_csrf_token(session, url),
                 "username": username, "password": password, "next": "/admin/"}
    r = session.post(url, headers=user_headers, data=user_data)
    ret = search_element(
        r, '<a href="/admin/qcloud_app/server_device_verify_tb/add/" class="addlink">')
    if (ret != True and debug):
        ret = search_element(r, '<p class="errornote">')
        if (ret):
            print_info('Maybe username or password error')
    return ret
