#!/usr/bin/python
# -*-encoding:utf8 -*-
#author:Jinhao
# 测试文档

import os
import re
import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup

async def ripadDns(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                text = await res.read()
                await resultParse(text)
    except Exception as e:
        print(e)
    return

async def resultParse(text):
    RAPID = []
    soup = BeautifulSoup(text, 'html.parser')
    td_links = soup.find_all('tr')
    for d in td_links:
        a = d.get_text()
        a = a.strip()
        res = a.split('\n')
        try:
            mes = {
                res[0],
                res[1],
                res[2],
                res[-1]
            }
            RAPID.append(mes)
        except:
            pass
    print(RAPID)
    return


if __name__ == '__main__':
    url = 'https://rapiddns.io/subdomain/andseclab.com?full=1&down=1#result'
    loop = asyncio.get_event_loop()
    task = loop.create_task(ripadDns(url))
    loop.run_until_complete(task)
    print('helloworld')



