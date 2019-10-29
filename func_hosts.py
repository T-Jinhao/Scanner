#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import sys,os
from socket import *
from concurrent.futures import ThreadPoolExecutor

class Hosts:
    def __init__(self,host,threads,flag):
        self.host = host
        self.threads = threads
        self.flag = flag
        self.start()

    def start(self):
        print('>>>>>hosts'+'-'*40)
        print('[ 开始扫描存活主机 ]')
        url = self.c_hosts()
        report = self.run(url)
        if report:
            self.hosts_report(report)
        else:
            print("[ 并没有扫描出存活主机 ]")
        print('-'*40+'hosts<<<<<')


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
        with ThreadPoolExecutor(max_workers=self.threads) as pool:
            results = pool.map(self.scan,url)
            for result in results:
                if result['flag'] == 1:
                    print(result['msg'])
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
            msg = "[ {} : 已开启 ]".format(url)
            m = {'msg':msg,'flag':1}
        else:
            m = {'flag':0}
        return m


    def hosts_report(self,reports):
        '''
        保存报告
        :param reports:
        :return:
        '''
        path = os.path.abspath(os.path.dirname(__file__))
        dirname = self.host
        dirpath = "{0}\{1}\{2}".format(path, "reports", dirname)
        filepath = "{0}\{1}".format(dirpath, "c_hosts_report.txt")
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        F = open(filepath, 'a')
        try:
            for m in reports:
                F.write(m + '\n')
            print("[ 主机c段扫描报告已存放于：{}]".format(filepath))
        except:
            print("[ 并没有扫描出存活主机 ]")
        F.close()
        return