#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

from socket import *
from concurrent.futures import ThreadPoolExecutor
from reports import reports
from .color_output import color_output

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

    def start(self):
        color_output('>>>>>PortsScan' + '-' * 40)
        color_output("[ 开始扫描端口 : {} ]".format(self.host), color='BLUE')
        if self.flag:
            ports = self.scan_ports_crazy()
        else:
            ports = self.scan_ports()
        color_output('[ 准备就绪，开始扫描 ]', color='CYAN')
        report = self.run(ports)
        if report:
            reports.Report(report, self.name, 'port_report.txt', '主机端口扫描报告已存放于', '并没有扫描出主机开放端口').save()
        else:
            color_output("[ 并没有扫描出主机开放端口 ]", color='YELLOW')
        color_output('-' * 40 + 'PortsScan<<<<<' + '\n')
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
        for i in range(start_port,end_port+1):
            ports.append(i)
        return ports

    def run(self,port):
        '''
        调用线程池开始探测
        :param port:
        :return:
        '''
        reports = []
        with ThreadPoolExecutor(max_workers=20) as pool:
            results = pool.map(self.scan,port)
            for result in results:
                if result['flag']:
                    color_output(result['msg'], color='GREEN')
                    reports.append(result['msg'])
        return reports


    def scan(self,port):
        '''
        扫描端口
        :param port: 需要扫描的端口
        :return:
        '''
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((self.host, port))
        if result == 0:
            banner = self.getBanner(sock)
            if port in port_dict:
                msg = "[ {0} : {1}已开启  :  {2}]".format(str(port),port_dict[port],banner)
            else:
                msg = "[ {0} : 已开启  :  {1}]".format(str(port),banner)
            m = {'msg':msg,'flag':1}
            return m
        else:
            m = {'flag':0}
            return m

    def getBanner(self, sock):
        '''
        获取端口banner信息
        :param sock:
        :return:
        '''
        try:
            banner = sock.recv(1024)
            banner = banner.strip()
        except:
            banner = ''
        sock.close()  # 关闭连接
        return banner



