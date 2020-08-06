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
def spider(url,REQ):
    func_spider.celery_spider(url,REQ).run()
    return


@app.task(name='tasks.sqli.func_celery')
def sqli(url):
    func_sqli.Sql(url,True).start()
    return

@app.task(name='tasks.hosts.func_celery')
def hosts(host):
    func_hosts.Hosts(host).start()
    return

@app.task(name='tasks.burp.func_celery')
def burp(url,payload,flag):
    func_burp.celery_burp(url,payload,flag).run()
    return

@app.task(name='tasks.ports.func_celery')
def ports(host):
    func_ports.Ports(host,False).start()
    return

@app.task(name='tasks.domain.func_celery')
def domain(url,payload):
    func_domain.celery_domain(url,payload).run()
    return

