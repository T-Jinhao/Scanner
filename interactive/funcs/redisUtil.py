#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import redis
from lib.load_config import Config

class Redis:
    def __init__(self):
        config = Config().readConfig()
        host = config.get("Redis", "host")
        port = config.get("Redis", "port")
        password = config.get("Redis", "password")
        pool = redis.ConnectionPool(host=host, port=port, decode_responses=True, password=password)
        self.r = redis.Redis(connection_pool=pool)

    def query(self, key):
        try:
            res = self.r.get(key)
            return res
        except:
            return None

    def save(self, key, value):
        try:
            self.r.set(key, value)
        except:
            pass

    def initTask(self, ran_str):
        try:
            self.r.set('current_Taskname', ran_str)
        except:
            pass

    def queryInitKey(self, key):
        k = 'current_' + key
        try:
            res = self.r.get(k)
            return res
        except:
            return