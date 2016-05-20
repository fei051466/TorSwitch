# coding=utf-8

import socket

def tor_new_identity(tor_ip, control_port, auth_code=''):
    # switch new identity
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(tor_ip, control_port)
        s.connect((tor_ip, control_port))
        s.send("AUTHENTICATE %s\r\n" % auth_code)
        response = s.recv(1024)
        code, text = response.split(' ')
        if code != '250':
            return False
        s.send("signal NEWNYM\r\n")
        response = s.recv(1024)
        code, text = response.split(' ')
        if code != '250':
            return False
        s.close()
        return True
    except Exception, e:
        print(str(e))
        return False


def tor_get_cookie(cookie_path):
    # get current cookie
    with open(cookie_path, 'r') as cookie_file:
        cookie = cookie_file.read()
        hex_cookie = ''
        for i in cookie:
            h = hex(ord(i))[2:]
            hex_cookie += h.zfill(2)
        print hex_cookie.upper()
        return hex_cookie.upper()


def tor_switch():
    # switch tor
    cookie_path = r'C:\Users\admin\Desktop\Tor Browser\Browser\TorBrowser\Data\Tor\control_auth_cookie'
    cookie = tor_get_cookie(cookie_path)
    
    tor_ip= '127.0.0.1'
    control_port= 9151
    switch_success = False
    switch_times = 0
    while not switch_success and switch_times <= 10:
        switch_success = tor_new_identity(tor_ip, control_port, cookie)
        switch_times += 1
    if switch_success:
        return True 
    else:
        return False


if __name__ == '__main__':
    if tor_switch():
        print('success')
    else:
        print('fail')
