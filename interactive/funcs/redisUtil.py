#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import redis
from lib.load_config import Config

class Redis:
    def __init__(self, taskname=''):
        config = Config().readConfig()
        host = config.get("Redis", "host")
        port = config.get("Redis", "port")
        password = config.get("Redis", "password")
        pool = redis.ConnectionPool(host=host, port=port, decode_responses=True, password=password)
        self.r = redis.Redis(connection_pool=pool)
        self.taskname = taskname

    def query(self, key):
        k = self.taskname + '_' + key
        try:
            res = self.r.get(k)
            return res
        except:
            return None

    def save(self, key, value):
        k = self.taskname + '_' + key
        try:
            self.r.set(k, value)
        except:
            pass

    def initTask(self):
        try:
            self.r.set('current_taskname', '')  # 每次启动前清空上次任务
        except:
            pass