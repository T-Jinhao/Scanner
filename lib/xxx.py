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

save_pool = redis.Connection(host='127.0.0.1',port=6379,decode_responses=True)
host_pool = redis.Redis(save_pool)
app = Celery('xxx',backend='redis://localhost:6379/0',broker='redis://localhost:6379/0')
os.system('celery -A xxx worker -l info')

@app.task
def add(x,y):
    print('helloworld')
    return x+y





