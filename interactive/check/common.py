#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import re
import socket
from interactive.funcs import util

class Common:
    def __init__(self):
        pass

    def checkTimeout(self, input):
        try:
            t = int(input)
            if t > 0:
                return True
        except:
            pass
        util.printError('Invaild Value')
        return False

    def checkWorkers(self, input):
        try:
            w = int(input)
            if w > 0:
                return True
        except:
            pass
        util.printError('Invaild Value')
        return False

    def checkTaskname(self, input):
        if len(input) > 15:
            util.printError('Taskname too long')
            return False
        return True

    def checkIp(self, input):
        url = input.split('#')[0]
        url = url.replace("http://", "").replace("https://", "")
        url = url.split('/')[0]
        try:
            socket.gethostbyname(url)
            return True
        except Exception as e:
            print(e)
        util.printError("can't parse to ip")
        return False

    def checkUrl(self, input):
        url = input.split('#')[0]
        if re.match('(http|https)://(.*?)\.(.*)',url):     # 匹配以http|https开头的网站
            return True
        elif re.match('(.*?)\.(.*)',url):                  # 匹配xxx.xxx...规则的网站
            return True
        util.printError('Invaild Url')
        return False