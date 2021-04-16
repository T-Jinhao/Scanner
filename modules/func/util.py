#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import re
import socket
import yarl
from urllib.parse import urljoin

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

def splicingUrl(url, u):
    '''
    检测url完整性，拼接返回绝对地址
    :param url: 当前扫描的页面url
    :param u: 获取到的url
    :return:
    '''
    err = ['', None, '/', '\n']
    if u in err:
        return
    if re.match("(http|https)://.*", u):  # 匹配绝对地址
        return u.split('#')[0]
    else:     # 拼凑相对地址，转换成绝对地址
        u = urljoin(url, u)
        return u.split('#')[0]

def judgingOrigin(originUrl, checkUrl):
    '''
    判断同源
    或返回IP
    :param originUrl:
    :param checkUrl:
    :return:
    '''
    ourl = yarl.URL(originUrl)
    curl = yarl.URL(checkUrl)
    ip = re.compile('[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}')
    netloc = curl.host
    res = ip.match(netloc)  # ip均检测
    if res:
        return True
    n = netloc.split('.')
    if n[-2] not in ["com", "edu", "ac", "net", "org", "gov"]:  # 带地域标签的域名
        c_domain = n[-2]
    else:
        c_domain = n[-3]
    m = ourl.host.split('.')
    if m[-2] not in ["com", "edu", "ac", "net", "org", "gov"]:  # 带地域标签的域名
        o_domain = m[-2]
    else:
        o_domain = m[-3]
    if c_domain == o_domain:
        return True
    return False