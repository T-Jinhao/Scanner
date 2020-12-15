#!/usr/bin/python
# -*-encoding:utf8 -*-
#author:Jinhao
# 测试文档

import aiohttp
import re
import requests
import asyncio
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

def getTitle(text):
    compile = re.compile("<title22>(.*?)</title22>")
    title = compile.findall(text)
    print(title)


if __name__ == '__main__':
    url = "https://loan.jd.com/home.htm"
    r = requests.get(url)
    getTitle(r.text)



