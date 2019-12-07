#!/usr/bin/python
# -*- encoding=utf8 -*-
#author:Jinhao


import redis,os,threading,time
from lib.func_celery import *



class RC:
    def __init__(self,url):
        self.url = url
        self.start()

    def start(self):
        # self.start_redis()
        thread = threading.Thread(target=self.start_celery)
        thread.start()
        time.sleep(10)                       # 预留充分启动celery时间
        self.run(self.url)


    def start_redis(self):
        '''
        启动本地redis服务
        :return:
        '''
        self.save_pool = redis.Connection(host='127.0.0.1',port='6379',decode_responses=True)
        self.url_pool = redis.Redis(self.save_pool)
        self.func_pool = redis.Redis(self.save_pool)
        return


    def start_celery(self):
        '''
        启动celery服务
        :return:
        '''
        path = os.path.dirname(__file__)
        os.chdir(path)                                          # 切换工作目录
        cmd = 'celery -A func_celery worker --pool=eventlet'    # 指定工作者
        os.system(cmd)


    def run(self,url):
        result = spider.delay(url)
        print('start')
        while not result.ready():
            time.sleep(1)
        print(result.get())
        return


