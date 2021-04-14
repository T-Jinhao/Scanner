#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

from socket import *
from concurrent.futures import ThreadPoolExecutor
from reports import reports_txt,reports_xlsx
from .load_config import Config
from .color_output import *
from modules.func import sniffPort

port_dict = {
    21:'ftp',
    22:'ssh',
    23:'telnet',
    25:'smtp',
    53:'domain',
    80:'http',
    110:'POP3',
    111:'RPC',
    113:'windows验证服务',
    135:'RPC远程调用',
    137:'NetBIOS',
    139:'共享服务',
    161:'snmp',
    162:'snmp',
    389:'LDAP',
    443:'https',
    445:'microsoft-ds',
    1080:'socks',
    1433:'mssql',
    1521:'oracle',
    3306:'mysql',
    3389:'ms-wbt-server',
    6379:'redis',
    7001:'weblogic',
    7002:'weblogic',
    8080:'http-proxy'
}

class Ports():
    def __init__(self, host, name, flag):
        self.host = host
        self.name = name
        self.flag = flag
        self.Output = ColorOutput()

    def load_config(self):
        config = Config().readConfig()
        self.max_workers = config.getint("Ports", "max_workers")
        self.timeout = config.getfloat("Ports", "timeout")
        system = platform.system()
        self.saveType = config.get("Result", system)

    def start(self):
        print(self.Output.fuchsia('>>>>>PortsScan' + '-' * 40))
        print(self.Output.blue('[ schedule ] ') + self.Output.fuchsia('开始扫描端口:') + self.Output.green(self.host))
        self.load_config()
        if self.flag:
            ports = self.scan_ports_crazy()
        else:
            ports = self.scan_ports()
        print(self.Output.blue('[ schedule ] ') + self.Output.cyan('准备就绪，开始扫描'))
        report = self.run(ports)   # 获取开放端口
        new_report = self.showReport(report)
        self.saveResult(new_report)
        print(self.Output.fuchsia('-' * 40 + 'PortsScan<<<<<' + '\n'))
        return

    def saveResult(self, report):
        '''
        保存报告
        :param report:
        :return:
        '''
        if report == []:
            print(self.Output.blue('[ result ] ') + self.Output.yellow('没有扫描出主机开放端口'))
            return
        if self.saveType == 'xlsx':
            banner = ['IP', '端口', '服务', 'banner']
            reports_xlsx.Report(report, self.name, 'Ports', banner).save()
        else:
            reports_txt.Report(report, self.name, 'port_report.txt', '主机端口扫描报告已存放于', '并没有扫描出主机开放端口').save()
        return


    def scan_ports(self):
        '''
        常用端口
        :return:
        '''
        ports = [21, 22, 23, 25, 53, 69, 80, 110, 113, 119, 135, 137,
                 139, 161, 162, 389, 443, 445, 1080, 1433, 3306, 3389,
                 6379, 7001, 7002, 8080]
        return ports



    def scan_ports_crazy(self):
        '''
        自定义扫描端口范围
        :return:
        '''
        ports = []
        start_port = input("请输入开始时扫描的端口[默认全扫]\n")
        if start_port:
            end_port = input("请输入结束时扫描的端口[回车即扫描单个端口]\n")
            if end_port == '':
                end_port = start_port
        else:
            start_port = 1
            end_port = 65535
        try:                           # try-expect : 防止错误输入
            start_port = int(start_port)
            end_port = int(end_port)
            if start_port > end_port:
                p = start_port
                start_port = end_port
                end_port = p
        except:
            start_port = 1
            end_port = 65535
        for i in range(start_port, end_port+1):
            ports.append(i)
        return ports

    def run(self,port):
        '''
        调用异步开始探测
        :param port:
        :return:
        '''
        sniff = sniffPort.ScanPort(
            ip=self.host,
            port=port,
            time_out=self.timeout,
            concurrency=self.max_workers
        )
        sniff.loop.run_until_complete(sniff.start())
        reports = sniff.retResult()
        return reports

    def showReport(self, reports):
        new_report = []
        for r in reports:
            if r['port'] in port_dict:
                service = port_dict[r['port']]
            else:
                service = 'unrecognized'
            print(self.Output.green('[ result ] ')
                  + self.Output.fuchsia('port: ') + self.Output.green(r['port']) + self.Output.interval()
                  + self.Output.fuchsia('server: ') + self.Output.green(service) + self.Output.interval()
                  + self.Output.fuchsia('banner: ') + self.Output.green(r['banner'])
                  )
            msg = "{0} : {1} : {2}  : {3}".format(self.host, str(r['port']), service, str(r['banner']))
            new_report.append(msg)
        return new_report




