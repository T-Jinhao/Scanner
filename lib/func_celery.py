#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao

import redis
import os,sys
import socket
from urllib.parse import urlparse
from celery import Celery
from lib import func_sqli,func_hosts,func_domain,func_ports,func_burp,func_spider,func_login

'''
celery任务分配
'''

app = Celery('task',backend='redis://localhost:6379/0',broker='redis://localhost:6379/0')

@app.task(name='tasks.spider.func_celery')
def spider(url):
    func_spider.Spider(url,'',20,0)
    return

@app.task(name='tasks.login.func_celery')
def login(url):
    func_login.Login(url,'',20,0)
    return

@app.task(name='tasks.sqli.func_celery')
def sqli(url):
    func_sqli.Sql(url,True)
    return

@app.task(name='tasks.hosts.func_celery')
def hosts(url):
    try:
        name = urlparse(url).hostname
        host = socket.gethostbyname(name)
    except:
        name = 'www.{}'.format(urlparse(url).netloc)
        host = socket.gethostbyname(name)
    func_hosts.Hosts(host,20,True)
    return

@app.task(name='tasks.burp.func_celery')
def burp(url):
    func_burp.Burp(url,'','',20,True)
    return

@app.task(name='tasks.ports.func_celery')
def ports(url):
    try:
        name = urlparse(url).hostname
        host = socket.gethostbyname(name)
    except:
        name = 'www.{}'.format(urlparse(url).netloc)
        host = socket.gethostbyname(name)
    func_ports.Ports(host,20,True)
    return

@app.task
def domain(url):
    func_domain.Domain(url,'',20,True)
    return

