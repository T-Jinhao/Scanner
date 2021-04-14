#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao

import aiohttp
import asyncio
import yarl
from lib.color_output import color_output
from lib.load_config import Config

class Async:
    def __init__(self, cookies={}):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        self.cookies = cookies
        self.proxies = self.preProxies()

    def preProxies(self):
        # 解析代理
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

    def parseUrl(self, url):
        u = yarl.URL(url)
        if u.scheme == '':
            url += 'http://'
