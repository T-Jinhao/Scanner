#!/usr/bin/python
# -*- encoding=utf8 -*-
#author:Jinhao


import time,redis
from lib.func_celery import *



class RC:
    def __init__(self,url):
        self.url = url
        self.start()

    def start(self):
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




    def run(self,url):
        result = domain.delay(url)
        print('start')
        while not result.ready():
            time.sleep(1)
        print(result.get())
        return


