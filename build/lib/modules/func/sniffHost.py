import sys
from socket import socket, AF_INET, SOCK_STREAM
import time
from asyncio import Queue, TimeoutError, gather

from async_timeout import timeout


class ScanHost(object):
    def __init__(self, ip, time_out: float = 0.1, concurrency: int = 500):
        if type(ip) is not list:
            ip = [ip]
        self.ip = ip   # 数组
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
            port = 80
            host = await self.queue.get()
            sock = socket(AF_INET, SOCK_STREAM)
            try:
                with timeout(self.timeout):
                    # 这里windows和Linux返回值不一样
                    # windows返回sock对象，Linux返回None
                    await self.loop.sock_connect(sock, (host, port))
                    # t2 = time.time()
                    # 所以这里直接直接判断sock
                    if sock:
                        res = {
                            'host': host,
                            'port': port
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
        for h in self.ip:
            self.queue.put_nowait(h)
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
    scan = ScanHost('183.232.231.174',  time_out=3.0)
    scan.loop.run_until_complete(scan.start())
    print(scan.retResult())

