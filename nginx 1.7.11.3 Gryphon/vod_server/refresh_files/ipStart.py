#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def start_url(port, path, proto="http"):
    import os
    cmd = "start " + proto + "://" + get_ip() + ":" + str(port) + "" + path
    print("cmd", cmd)
    os.system(cmd)


def start_url(port, path):
    import os
    url = "http://" + get_ip() + ":" + str(port) + "" + path
    cmd = "start " + url
    print(url)
    os.system(cmd)


def print_help():
    print('''port [path]
    port 端口
    path 可选参数 默认是/
    示例:
    [this py] 8888   ->  http://192.168.1.5:8888/
    [this py] 8888 /login  ->  http://192.168.1.5:8888/login
                ''')


def handle(args):
    if len(args) < 1:
        print_help()
        return
    port = args[0]
    try:
        port = int(args[0])
    except:
        print("port [%s] is illgegal!" % port)
        pass
    path = "/"
    if len(args) > 1:
        path = args[1]
        if path[0] != '/':
            path = '/' + path

    start_url(port, path)


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    handle(args)
