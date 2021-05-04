#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import redis
import datetime
from lib.load_config import Config
from interactive.funcs import util

class Redis:
    def __init__(self):
        config = Config().readConfig()
        host = config.get("Redis", "host")
        port = config.get("Redis", "port")
        password = config.get("Redis", "password")
        try:
            pool = redis.ConnectionPool(host=host, port=port, decode_responses=True, password=password)
            self.r = redis.Redis(connection_pool=pool)
        except redis.ConnectionError as e:
            util.printError("[!]Redis")
            print(e)

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
        today = datetime.datetime.today()
        formatted_today = today.strftime('%y%m%d')
        taskname = formatted_today
        try:
            self.r.set('current_Tasknameid', ran_str)
            self.r.set('current_Url', '')
            self.r.set('current_Ip', '')
            self.r.set('current_Taskname', taskname)
        except Exception as e:
            util.printWarn(str(e))
            return False

    def queryInitKey(self, key):
        k = 'current_' + key
        try:
            res = self.r.get(k)
            return res
        except:
            return

    def refreshTasknameid(self):
        ran_str = util.getRangeStr()
        self.r.set('current_Tasknameid', ran_str)

if __name__ == '__main__':
    r = Redis()
    u = r.query('current_Taskname')
    print(u)