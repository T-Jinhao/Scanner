#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import os,json
import requests
import subprocess
import threading,time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import redis
from celery import Celery
from lib.func_celery import *

def api():
    cmd = 'celery -A func_celery worker --pool=eventlet'    # 启动celery
    os.system(cmd)

def main():
    thread = threading.Thread(target=api)
    thread.start()
    time.sleep(10)     # 充分启动
    result = spider.delay('http://www.keyboy.xyz')
    print('start')
    while not result.ready():
        time.sleep(1)
        # print('sleep')
    print(result.get())
    return


if __name__ == '__main__':
    main()

