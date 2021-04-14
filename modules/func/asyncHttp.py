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


async def fetch(session, url):
    async with session.get(url) as response:  # session.get(url)获取页面
        r = parsing.Parsing()
        await r.parse(response)
        return r  # 返回页面解码后的信息


async def main(url, semaphore):
    async with semaphore:  # 这里进行执行asyncio.Semaphore，
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, url)  # 相当于 yield from
            print(html.status, html.url)

async def run(URLs, workers=500):
    if type(URLs) != list:
        URLs = [URLs]
    semaphore = asyncio.Semaphore(workers)  # 限制并发量为500,这里windows需要进行并发限制，
    to_get = [main(u, semaphore) for u in URLs]
    await asyncio.wait(to_get)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(''))
    loop.close()
