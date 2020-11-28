#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao

import grequests
import config
import urllib3
from lib.color_output import color_output
urllib3.disable_warnings()

HEADER = config.HEADERS
PROXY = config.PROXY


class Concurrent:
    def __init__(self, cookies={},  verify=False, timeout=5):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        self.cookies = cookies
        self.proxies = PROXY
        self.verify = verify
        self.timeout = timeout

    def autoGetAccess(self, url):
        if url.startswith('http://') or url.startswith('https://'):
            ret = self.mGetAccess(url)
        else:
            ret = self.mGetAccess('http://' + url)
        return ret

    def mGetAccess(self, url):
        try:
            res = [grequests.get(
                url,
                headers=self.headers,
                cookies=self.cookies,
                timeout=self.timeout
            )]
            ret = grequests.map(res)
            return ret[0]
        except Exception as e:
            color_output(e, color='RED')
            return


    def autoPostAccess(self, url, data={}):
        if url.startswith('http://') or url.startswith('https://'):
            ret = self.mPostAccess(url, data)
        else:
            ret = self.mPostAccess('http://' + url, data)
        return ret

    def mPostAccess(self, url, data={}):
        try:
            res = [grequests.post(
                url,
                headers=self.headers,
                cookies=self.cookies,
                timeout=self.timeout,
                data=data
            )]
            ret = grequests.map(res)
            return ret[0]
        except Exception as e:
            color_output(e, color='RED')
            return
