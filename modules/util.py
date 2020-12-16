#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import re
import socket


def getHostname(host):
    '''
    获取hostname
    :param host: 域名信息
    :return: ip地址
    '''
    IP = ''
    try:
        IP = socket.gethostbyname(host)
    except:
        pass
    return IP

def getTitle(text):
    '''
    获取网页title
    :param text:包体text
    :return:
    '''
    compile=re.compile("<title>(.*?)</title>")
    title = compile.findall(text)
    if len(title) > 0:
        return title[0]
    return '[ X ]'