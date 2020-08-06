#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao

import requests

class URL:
    def __init__(self, cookies={}, proxies={}, verify=False, timeout=5):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        self.cookies = cookies
        self.proxies = proxies
        self.verify = verify
        self.timeout = timeout

    def autoAccess(self, url):
        if url.startswith('http://'):
            ret = self.httpAccess(url)
        elif url.startswith('https://'):
            ret = self.httpsAccess(url)
        else:
            ret = self.httpAccess('http://'+url)
        return ret

    def httpAccess(self, url):
        try:
            res = requests.get(
                url,
                headers=self.headers,
                cookies=self.cookies,
                timeout=self.timeout
            )
            return res
        except Exception as e:
            print(e)
            return

    def httpsAccess(self, url):
        try:
            res = requests.get(
                url,
                headers=self.headers,
                cookies=self.cookies,
                verify=self.verify,
                timeout=self.timeout
            )
            return res
        except Exception as e:
            print(e)
            return

    def autoPostAccess(self, url, data):
        if url.startswith('http://'):
            ret = self.httpPostAccess(url)
        elif url.startswith('https://'):
            ret = self.httpsPostAccess(url)
        else:
            ret = self.httpPostAccess('http://'+url)
        return ret

    def httpPostAccess(self, url, data):
        try:
            res = requests.post(
                url,
                headers=self.headers,
                cookies=self.cookies,
                timeout=self.timeout,
                data=data
            )
            return res
        except Exception as e:
            print(e)
            return

    def httpsPostAccess(self, url, data):
        try:
            res = requests.post(
                url,
                headers=self.headers,
                cookies=self.cookies,
                verify=self.verify,
                timeout=self.timeout,
                data=data
            )
            return res
        except Exception as e:
            print(e)
            return