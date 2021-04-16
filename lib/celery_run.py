#!/usr/bin/python
# -*- encoding=utf8 -*-
#author:Jinhao


import time
import redis
from lib.func_celery import *
from main import *


class RC:
    def __init__(self, args, REQ, bPayload, dPayload, lPayload, name, host=''):
        self.args = args
        self.REQ = REQ
        self.bPayload = bPayload
        self.dPayload = dPayload
        self.lPayload = lPayload
        self.name = name
        self.host = host


    def start(self):
        '''
        略有不同的调用方法
        :return:
        '''
        # print(self.args)
        if self.args.scan:
            ress = spider.delay(self.args.url, self.REQ, self.name)
            self.status(ress)
        if self.args.ports:
            resp = ports.delay(self.host, self.name)
            self.status(resp)
        if self.host:
            resh = hosts.delay(self.host, self.name)
            self.status(resh)
        if self.args.burp:
            result = burp.delay(self.args.url, self.bPayload, self.name, self.args.crazy)
            self.status(result)
        if self.args.domain:
            resd = domain.delay(self.args.url, self.dPayload, self.name)
            self.status(resd)
        if self.args.sqlscan:
            resi = sqli.delay(self.args.url, self.name)
            self.status(resi)
        else:
            # will add other things
            sys.exit()

    def status(self,res):
        '''
        检测状态
        :param res:
        :return:
        '''
        while not res.ready():
            time.sleep(1)
        print(res.get())
        return

    # def start_redis(self):
    #     '''
    #     启动本地redis服务
    #     :return:
    #     '''
    #     self.save_pool = redis.Connection(host='127.0.0.1',port='6379',decode_responses=True)
    #     self.url_pool = redis.Redis(self.save_pool)
    #     self.func_pool = redis.Redis(self.save_pool)
    #     return






