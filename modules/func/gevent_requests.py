#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao

import grequests
import urllib3
import sys
from lib.color_output import color_output
from lib.load_config import Config
from gevent import monkey

urllib3.disable_warnings()
monkey.patch_all(select=False, thread=False)
sys.setrecursionlimit(1000000)



class Concurrent:
    def __init__(self, cookies={},debug=False):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        self.cookies = cookies
        self.debug = debug
        self.proxies = self.preProxies()

    def preProxies(self):
        config = Config().readConfig()
        isProxy = config.getboolean("Proxy", "isProxy")
        if isProxy:
            http_protocol = config.get("Proxy", "http_protocol")
            http = config.get("Proxy", "http")
            https_protocol = config.get("Proxy", "https_protocol")
            https = config.get("Proxy", "https")
            proxies = {
                'http': http_protocol + http,
                'https': https_protocol + https
            }
            return proxies
        else:
            return {}

    def autoGetAccess(self, url, threads=5, timeout=5):
        if url.startswith('http://') or url.startswith('https://'):
            ret = self.mGetAccess(url, threads=threads, timeout=timeout)
        else:
            ret = self.mGetAccess('http://' + url, threads=threads, timeout=timeout)
        return ret

    def mGetAccess(self, url, threads=5, timeout=5):
        try:
            res = [grequests.get(
                url=url,
                headers=self.headers,
                cookies=self.cookies,
                timeout=timeout,
                proxies=self.proxies
            )]
            ret = grequests.map(res, exception_handler=self.err_handler, size=threads)
            return ret[0]
        except Exception as e:
            color_output(e, color='RED')
            return

    def mGetAsyncAccess(self, urls, threads=5, timeout=5):
        '''
        构造高并发请求
        :param urls:
        :return:
        '''
        try:
            res = [
                grequests.get(
                    url='http://' + u.split('://')[-1],
                    headers=self.headers,
                    cookies=self.cookies,
                    timeout=timeout,
                    proxies=self.proxies
                ) for u in urls
            ]
            ret = grequests.map(res, exception_handler=self.err_handler, size=threads)
            return ret
        except Exception as e:
            color_output(e, color='RED')
            return

    def autoPostAccess(self, url, data={}, threads=5, timeout=5):
        if url.startswith('http://') or url.startswith('https://'):
            ret = self.mPostAccess(url, data, threads=threads, timeout=timeout)
        else:
            ret = self.mPostAccess('http://' + url, data, threads=threads, timeout=timeout)
        return ret

    def mPostAccess(self, url, data={}, threads=5, timeout=5):
        try:
            res = [grequests.post(
                url=url,
                headers=self.headers,
                cookies=self.cookies,
                timeout=timeout,
                data=data,
                proxies=self.proxies
            )]
            ret = grequests.map(res, exception_handler=self.err_handler, size=threads)
            return ret[0]
        except Exception as e:
            color_output(e, color='RED')
            return

    def err_handler(self, request, exception):
        if self.debug == True:
            color_output(request.url, color='RED')
            color_output(exception, color='RED')
        return
