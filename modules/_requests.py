#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao

import grequests
import config
import urllib3
import sys
from lib.color_output import color_output
from gevent import monkey

urllib3.disable_warnings()
monkey.patch_all(select=False, thread=False)
sys.setrecursionlimit(1000000)

HEADER = config.HEADERS
PROXY = config.PROXY


class Concurrent:
    def __init__(self, cookies={},  timeout=5, threads=5):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        self.cookies = cookies
        self.proxies = PROXY
        self.timeout = timeout
        self.threads = threads

    def autoGetAccess(self, url):
        if url.startswith('http://') or url.startswith('https://'):
            ret = self.mGetAccess(url)
        else:
            ret = self.mGetAccess('http://' + url)
        return ret

    def mGetAccess(self, url):
        try:
            res = [grequests.get(
                url=url,
                headers=self.headers,
                cookies=self.cookies,
                timeout=self.timeout
            )]
            ret = grequests.map(res, exception_handler=self.err_handler, size=self.threads)
            return ret[0]
        except Exception as e:
            color_output(e, color='RED')
            return

    def mGetAsyncAccess(self, urls):
        '''
        构造高并发请求
        :param urls:
        :return:
        '''
        try:
            res = [
                grequests.get(
                    url=u,
                    headers=self.headers,
                    cookies=self.cookies,
                    timeout=self.timeout
                ) for u in urls
            ]
            ret = grequests.map(res, exception_handler=self.err_handler, size=self.threads)
            return ret
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
                url=url,
                headers=self.headers,
                cookies=self.cookies,
                timeout=self.timeout,
                data=data
            )]
            ret = grequests.map(res, exception_handler=self.err_handler, size=self.threads)
            return ret[0]
        except Exception as e:
            color_output(e, color='RED')
            return

    def err_handler(self, request, exception):
        color_output(request.url, color='RED')
        color_output(exception, color='RED')
