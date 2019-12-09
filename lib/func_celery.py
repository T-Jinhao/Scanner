#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao


import socket
from urllib.parse import urlparse
from celery import Celery
from lib import func_sqli,func_hosts,func_domain,func_ports,func_burp,func_spider

'''
celery任务分配
'''

app = Celery('task',backend='redis://localhost:6379/0',broker='redis://localhost:6379/0')

@app.task(name='tasks.spider.func_celery')
def spider(url,cookies):
    func_spider.celery_spider(url,cookies)
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
    func_hosts.Hosts(host,20)
    return

@app.task(name='tasks.burp.func_celery')
def burp(url,file,cookies,flag):
    func_burp.celery_burp(url,file,cookies,flag)
    return

@app.task(name='tasks.ports.func_celery')
def ports(url):
    try:
        name = urlparse(url).hostname
        host = socket.gethostbyname(name)
    except:
        name = 'www.{}'.format(urlparse(url).netloc)
        host = socket.gethostbyname(name)
    func_ports.Ports(host,20,False)
    return

@app.task(name='tasks.domain.func_celery')
def domain(url,file):
    func_domain.celery_domain(url,file)
    return

