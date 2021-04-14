#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao

import aiohttp
import asyncio
import yarl
import sys
import socket
from asyncio import Queue, TimeoutError, gather
from modules.func import parsing

class req:
    def __init__(self, timeout=3):
        self.timeout = timeout

    async def fetch(self, session, url):
        try:
            async with session.get(url) as response:  # session.get(url)获取页面
                r = parsing.Parsing()
                await r.parse(response)
                return r  # 返回页面解码后的信息
        except:
            pass


    async def main(self, url, semaphore):
        async with semaphore:  # 这里进行执行asyncio.Semaphore，
            try:
                async with aiohttp.ClientSession() as session:
                    resp = await self.fetch(session, url)  # 相当于 yield from
                    return resp
            except:
                pass

    async def run(self, URLs, workers=500):
        if type(URLs) != list:
            URLs = [URLs]
        semaphore = asyncio.Semaphore(workers)  # 限制并发量为500,这里windows需要进行并发限制，
        to_get = [self.main(u, semaphore) for u in URLs]
        await asyncio.wait(to_get)

if __name__ == '__main__':
    x = req()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(x.run(''))
    loop.close()
