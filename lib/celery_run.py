#!/usr/bin/python
# -*- encoding=utf8 -*-
#author:Jinhao


import time
import redis
from lib.func_celery import *
from main import *


class RC:
    def __init__(self,args):
        self.opt = {}
        for x, y in args._get_kwargs():
            self.opt[x] = y
        self.url_check(self.opt['url'])
        self.start()


    def url_check(self,url):
        '''
        很随意的URL合理性检测
        :param url: 待检测的URL
        :return: bool值
        '''
        url = url.split('#')[0]
        if re.match('(http|https)://(.*?)\.(.*)',url):     # 匹配以http|https开头的网站
            return
        elif re.match('(.*?)\.(.*)',url):                  # 匹配xxx.xxx...规则的网站
            self.opt['url'] = "http://"+url                # 添加协议头
            return
        else:
            print("URL格式出错!")
            sys.exit(1)

    def start(self):
        '''
        略有不同的调用方法
        :return:
        '''
        if self.opt['spider']:
            ress = spider.delay(self.opt['url'],self.opt['cookies'])
            self.status(ress)
        if self.opt['ports']:
            resp = spider.delay(self.opt['url'])
            self.status(resp)
        if self.opt['hosts']:
            resh = hosts.delay(self.opt['url'])
            self.status(resh)
        if self.opt['burp']:
            result = burp.delay(self.opt['url'],self.opt['file'],self.opt['cookies'],self.opt['crazy'])
            self.status(result)
        if self.opt['domain']:
            resd = domain.delay(self.opt['url'],self.opt['file'])
            self.status(resd)
        if self.opt['sqlscan']:
            resi = sqli.delay(self.opt['url'])
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






