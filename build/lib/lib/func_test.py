import aiohttp
import asyncio
import yarl
import requests

"""
    aiohttp:发送http请求
    1.创建一个ClientSession对象
    2.通过ClientSession对象去发送请求（get, post, delete等）
    3.await 异步等待返回结果
"""

async def main(url):
    u = f"http://{url}.com"
    print(u)
    timeout = aiohttp.ClientTimeout(total=5)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(u) as res:
                #
                # print(res.status)
                # print(await res.text())
                r = RES()
                await r.parse(res)
                return r
    except:
        print(f"error000000000000000000000000000000000000____{u}")
        pass
    return f"{url}__sdcdada"

URLs = [i for i in range(100)]

class RES():
    def __init__(self):
        self.status = 200
        self.text = ""

    async def parse(self, res):
        self.text = await res.text()
        self.status = res.status



async def parse(URLS):
    tasks = [asyncio.create_task(main(url)) for url in URLS]
    results = await asyncio.gather(*tasks)
    for x in results:
        try:
            print(x.status)
        except:
            print('no')


loop = asyncio.get_event_loop()
task = loop.create_task(parse(URLs))
loop.run_until_complete(task)

print('end')

def parseUrl(url):
    u = yarl.URL(url)
    print(u.scheme)
    if u.scheme == '':
        print('xxx')
    print(u)

parseUrl('https://baidu.com')

# https://www.cnblogs.com/ssyfj/p/9222342.html