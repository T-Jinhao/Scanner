#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao


import socket
from urllib.parse import urlparse
from celery import Celery
from lib import func_sqli,func_hosts,func_domain,func_ports,func_burp,func_scan

'''
celery任务分配
'''

app = Celery('task',backend='redis://localhost:6379/0',broker='redis://localhost:6379/0')

@app.task(name='tasks.spider.func_celery')
def spider(url,REQ,name):
    func_scan.celery_scan(url, REQ, name).run()
    return


@app.task(name='tasks.sqli.func_celery')
def sqli(url, name):
    func_sqli.Sql(url, name, True).start()
    return

@app.task(name='tasks.hosts.func_celery')
def hosts(host, name):
    func_hosts.Hosts(host, name).start()
    return

@app.task(name='tasks.burp.func_celery')
def burp(url, payload, name, flag):
    func_burp.celery_burp(url, payload, name, flag).run()
    return

@app.task(name='tasks.ports.func_celery')
def ports(host, name):
    func_ports.Ports(host, name, False).start()
    return

@app.task(name='tasks.domain.func_celery')
def domain(url, payload, REQ, name):
    func_domain.celery_domain(url, payload, REQ, name).run()
    return

