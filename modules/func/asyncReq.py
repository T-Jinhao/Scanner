#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao

import aiohttp
import asyncio
import yarl
import sys
import socket
from asyncio import Queue, TimeoutError, gather
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
        # 添加协议头
        u = yarl.URL(url)
        if u.scheme == '':
            url += 'http://'
        return url

    async def getMethod(self, url, timeout=3, **kwargs):
        u = self.parseUrl(url)
        timeout = aiohttp.ClientTimeout(total=timeout)
        try:
            async with asyncio.Semaphore(500):
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.get(u, **kwargs) as res:
                        r = Parsing()
                        await r.parse(res)
                        return r
        except:
            pass

    async def postMethod(self, url, timeout=3, data={}, **kwargs):
        u = self.parseUrl(url)
        timeout = aiohttp.ClientTimeout(total=timeout)
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(u, data=data, **kwargs) as res:
                    r = Parsing()
                    await r.parse(res)
                    return r
        except:
            pass

    async def autoRun(self, URLs, Method='GET', timeout=3, data={}, **kwargs):
        '''
        主要调用方法
        异步请求
        :param URLs:
        :param Method:
        :param kwargs:
        :return:
        '''
        if type(URLs) != list:
            URLs = [URLs]
        if Method == 'POST':
            tasks = [asyncio.create_task(self.postMethod(u, timeout=timeout, data=data, **kwargs)) for u in URLs]
        else:
            tasks = [asyncio.create_task(self.getMethod(u, timeout=timeout, **kwargs)) for u in URLs]
        results = await asyncio.gather(*tasks)
        return results

    @staticmethod
    def get_event_loop():
        """
        判断不同平台使用不同的事件循环实现

        :return:
        """
        if sys.platform == 'win32':
            from asyncio import ProactorEventLoop
            # 用 "I/O Completion Ports" (I O C P) 构建的专为Windows 的事件循环
            return ProactorEventLoop()
        else:
            from asyncio import SelectorEventLoop
            return SelectorEventLoop()

class Parsing:
    def __init__(self):
        self.text = ''
        self.status = ''
        self.url = ''
        self.history = ''
        self.ip = ''

    async def parse(self, res):
        self.text = await res.text()
        self.status = res.status
        self.url = res.url
        self.history = res.history
        self.ip = await self.getIp(self.url)

    async def getIp(self, url):
        host = yarl.URL(url).host
        try:
            ip = socket.gethostbyname(host)
        except:
            ip = ''
        return ip


