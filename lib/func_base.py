#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import re
from modules import _requests

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


if __name__ == '__main__':
    r = _requests.Concurrent()
    x = IPcontent('baidu.com', r)
    rep = x.run()
    for m in rep:
        print(m)