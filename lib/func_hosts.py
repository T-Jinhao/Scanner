#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

from reports import reports_txt, reports_xlsx
from modules.func import sniffHost
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
        new_report = self.showReport(report)
        self.saveResult(new_report)
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
            banner = ['C段主机', '探测端口']
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
        H = "{0}.{1}.{2}.".format(h[0], h[1], h[2])
        for i in range(1, 256):
            x = H + str(i)
            url.append(x)
        return url


    def run(self, IPs):
        '''
        调用异步
        :param IPs:
        :return:
        '''
        sniff = sniffHost.ScanHost(
            ip=IPs
        )
        sniff.loop.run_until_complete(sniff.start())
        results = sniff.result
        return results

    def showReport(self, reports):
        if reports == []:
            return []
        new_report = []
        for r in reports:
            print(self.Output.green('[ result ]' )
                  + self.Output.fuchsia('host: ') + self.Output.green(r['host']) + self.Output.interval()
                  + self.Output.fuchsia('sniffPort: ') + self.Output.green(r['port'])
                  )
            msg = "{0}:{1}".format(r['host'], str(r['port']))
            new_report.append(msg)
        return new_report


