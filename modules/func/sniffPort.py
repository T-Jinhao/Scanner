import sys
from socket import socket, AF_INET, SOCK_STREAM
import time
from asyncio import Queue, TimeoutError, gather
from typing import List

from async_timeout import timeout


class ScanPort(object):
    def __init__(self, ip: str = '', time_out: float = 0.1, port: List[int] = None, concurrency: int = 500):
        if not ip:
            raise ValueError(f'wrong ip! {ip}')
        self.ip = ip
        self.port = port
        self.result = []
        self.loop = self.get_event_loop()
        # 队列的事件循环需要用同一个，如果不用同一个会报错，这里还有一点不明白
        self.queue = Queue(loop=self.loop)
        self.timeout = time_out
        # 并发数
        self.concurrency = concurrency


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

    async def scan(self):
        while True:
            # t1 = time.time()
            port = await self.queue.get()
            sock = socket(AF_INET, SOCK_STREAM)
            try:
                with timeout(self.timeout):
                    # 这里windows和Linux返回值不一样
                    # windows返回sock对象，Linux返回None
                    await self.loop.sock_connect(sock, (self.ip, port))
                    # t2 = time.time()
                    # 所以这里直接直接判断sock
                    if sock:
                        try:
                            banner = await self.loop.sock_recv(sock, 1024)
                        except:
                            banner = ''
                        res = {
                            'port': port,
                            'banner': banner
                        }
                        self.result.append(res.copy())
                        # print(time.strftime('%Y-%m-%d %H:%M:%S'), port, 'open', round(t2 - t1, 2))
            # 这里要捕获所有可能的异常，windows会抛出前两个异常，Linux直接抛最后一个异常
            # 如果有异常不处理的话会卡在这
            except (TimeoutError, PermissionError, ConnectionRefusedError) as _:
                sock.close()
            sock.close()
            self.queue.task_done()

    async def start(self):
        # start = time.time()
        if self.port:
            for a in self.port:
                self.queue.put_nowait(a)
        else:
            for a in range(1, 65535 + 1):
                self.queue.put_nowait(a)
        task = [self.loop.create_task(self.scan()) for _ in range(self.concurrency)]
        # 如果队列不为空，则一直在这里阻塞
        await self.queue.join()
        # 依次退出
        for a in task:
            a.cancel()
        # Wait until all worker tasks are cancelled.
        await gather(*task, return_exceptions=True)
        # print(f'扫描所用时间为：{time.time() - start:.2f}')

    def retResult(self):
        return self.result



if __name__ == '__main__':
    ports = [i for i in range(1, 1000)]
    scan = ScanPort('183.232.231.174', port=ports, time_out=3.0)
    scan.loop.run_until_complete(scan.start())
    print(scan.retResult())

