#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import socket
import re

def getIp(input):
    url = input.split('#')[0]
    url = url.replace("http://", "").replace("https://", "")
    url = url.split('/')[0]
    try:
        hostname = socket.gethostbyname(url)
        return hostname
    except Exception as e:
        pass
    return False

def checkUrl(input):
    url = input.split('#')[0]
    if re.match('(http|https)://(.*?)\.(.*)',url):     # 匹配以http|https开头的网站
        return url
    elif re.match('(.*?)\.(.*)', url):                  # 匹配xxx.xxx...规则的网站
        url = "http://" + url                # 添加协议头
        return url
    return False
