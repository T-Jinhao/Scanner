#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import re
import socket
from modules.func import gevent_requests

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }

class IPcontent:
    def __init__(self, ip, REQ):
        self.ip = ip
        self.REQ = REQ

    def run(self):
        res = self.getDomainData()
        date = self.soupDate(res)
        domain = self.reDomain(res)
        mes = self._zip(date, domain)
        report = [x+' : '+y for x,y in dict(mes).items()]
        return report

    def getDomainData(self):
        url = "https://site.ip138.com/{ip}/".format(
            ip=self.ip
        )
        res = self.REQ.mGetAccess(url)
        return res

    def soupDate(self, res):
        content = res.content.decode('utf-8')
        compile = re.compile('<span class="date">(.*?)</span>')
        date = compile.findall(content)
        return date

    def reDomain(self, res):
        compile = re.compile('<li><span.*target="_blank">(.*?)</a></li>')
        content = res.content.decode('utf-8')
        domains = compile.findall(content)
        return domains

    def _zip(self, date, domain):
        mes = zip(date, domain)
        return mes


class CDNcontent:
    # 检测CDN
    def __init__(self, url):
        self.url = url.replace('http://', '').replace('https://', '').split('/')[0]

    def run(self):
        ip_list = []
        socket.setdefaulttimeout(5)
        addrs = socket.getaddrinfo(self.url, None)   # 端口处置空
        for item in addrs:
            if item[4][0] not in ip_list:
                ip_list.append(item[4][0])
        return ip_list

    def isCDN(self):
        try:
            ip_lsit = self.run()
            if len(ip_lsit) > 1:
                return 1
            else:
                return 0
        except:
            return -1


if __name__ == '__main__':
    r = gevent_requests.Concurrent()
    x = IPcontent('baidu.com', r)
    rep = x.run()
    for m in rep:
        print(m)