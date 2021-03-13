#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import platform
from socket import *
from concurrent.futures import ThreadPoolExecutor
from reports import reports_txt,reports_xlsx
from .color_output import *
from .load_config import Config

class Hosts:
    def __init__(self, host, name):
        self.host = host
        self.name = name
        self.Output = ColorOutput()

    def start(self):
        print(self.Output.fuchsia('>>>>>hosts'+'-'*40))
        print(self.Output.blue('[ schedule ] ') + self.Output.cyan('开始扫描开放主机'))
        url = self.c_hosts()
        report = self.run(url)
        self.saveResult(report)
        print(self.Output.fuchsia('-'*40+'hosts<<<<<'))
        return report

    def saveResult(self, report):
        '''
        保存报告
        :param report:
        :return:
        '''
        if report == []:
            print(self.Output.green('[ result ] ') + self.Output.yellow('没有扫描出开放主机'))
            return
        config = Config().readConfig()
        system = platform.system()
        saveType = config.get("Result", system)
        if saveType == 'xlsx':
            banner = ['C段IP信息', '端口情况']
            reports_xlsx.Report(report, self.name, 'Hosts', banner).save()
        else:    # txt类型为默认格式
            reports_txt.Report(report, self.name, 'c_hosts_report.txt', '主机c段扫描报告已存放于', '并没有扫描出存活主机').save()


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
            msg = "{} : 80".format(url)
            print(self.Output.green('[ result ] ') + self.Output.cyan(url))
            m = {'msg':msg,'flag':1}
        else:
            m = {'flag':0}
        return m



