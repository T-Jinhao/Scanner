#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

from socket import *
from concurrent.futures import ThreadPoolExecutor
from reports import reports
from .color_output import color_output,color_list_output

class Hosts:
    def __init__(self, host, name):
        self.host = host
        self.name = name

    def start(self):
        color_output('>>>>>hosts'+'-'*40)
        color_output('[ 开始扫描开放主机 ]', color='BLUE')
        url = self.c_hosts()
        report = self.run(url)
        if report:
            color_list_output(report, color='GREEN')
            reports.Report(report, self.name, 'c_hosts_report.txt', '主机c段扫描报告已存放于', '并没有扫描出存活主机').save()
        else:
            color_output("[ 并没有扫描出开放主机 ]", color='YELLOW')
        color_output('-'*40+'hosts<<<<<')
        return report


    def c_hosts(self):
        '''
        构造c段字典
        :return:
        '''
        url = []
        h = self.host.split('.')
        H = "{0}.{1}.{2}.".format(h[0],h[1],h[2])
        for i in range(1,256):
            x = H + str(i)
            url.append(x)
        return url


    def run(self,url):
        '''
        调用线程池
        :param url:
        :return:
        '''
        reports = []
        with ThreadPoolExecutor(max_workers=255) as pool:
            results = pool.map(self.scan,url)
            for result in results:
                if result['flag'] == 1:
                    # color_output(result['msg'], color='GREEN')
                    reports.append(result['msg'])
        return reports


    def scan(self,url):
        '''
        扫描主机80端口是否开放
        :param url:
        :return:
        '''
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((url,80))
        if result == 0:
            msg = "[ {} : 80端口已开启 ]".format(url)
            m = {'msg':msg,'flag':1}
        else:
            m = {'flag':0}
        return m



