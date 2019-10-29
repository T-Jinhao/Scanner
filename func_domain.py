#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import requests
import os,sys,re
from urllib.parse import urlparse
from dict import *
from concurrent.futures import ThreadPoolExecutor

class Domain:
    def __init__(self,url,file,threads,flag):
        self.domain = self.url_check(url)
        self.file = file
        self.threads = threads
        self.flag = flag
        self.start(url)

    def start(self,url):
        print('>>>>>domain' + '-' * 40)
        if self.domain:
            check = input("当前域名 {} 是否正确解析？[正确则回车，否则输入正确的域名]\n".format(self.domain))  # 防止出错
            if check:
                self.domain = check
            print("[ 开始爆破域名: {} ]".format(self.domain))
            report = self.chinaz_search()
            payload = self.load_payload(file, self.flag)
            if payload:
                print('[ payload导入完成 ]')
                report += self.run(self.domain, payload, self.threads)
            else:
                print('[ payload导入失败 ]')
            if report:
                self.domain_report(url, report)
            else:
                print("[ 未能挖掘出网站子域名 ]")
        else:
            print("[ {}不支持子域名挖掘 ]".format(url))
        print('-' * 40 + 'domain<<<<<' + '\n')
        return

    def url_check(self,url):
        '''
        检测url合理性
        :param url:
        :return:
        '''
        ip = re.compile('[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}')
        netloc = urlparse(url).netloc
        res = ip.match(netloc)                     # ip不支持子域名挖掘
        if res:
            return
        n = netloc.split('.')
        domain = "{0}.{1}".format(n[-2],n[-1])     # 域名切割，但会误报三级域名等
        return domain


    def chinaz_search(self):
        '''
        调用站长之家接口来查询子域名
        :return:
        '''
        report = []
        url = "https://tool.chinaz.com/subdomain/?domain={}".format(self.domain)
        res = requests.get(url,timeout=10)
        domain = re.compile('[\w]+\.{}'.format(self.domain))    # 正则提取子域名
        domains = domain.finditer(res.text)
        for d in domains:
            if d.group() not in report:
                print(d.group())
                report.append(d.group())
        return report


    def load_payload(self,file,flag):
        '''
        读取payload
        :param file: 外部payload，可为空
        :param flag: crazy标识
        :return:
        '''
        payload = []
        path = os.path.abspath(os.path.dirname(__file__))
        if file:
            try:
                F = open(file,'r')
                for x in F:
                    payload.append(x.replace('\n',''))
                return payload
            except:
                return
        
        else:
            file = 'dict.txt'
            filepath = "{0}\{1}\{2}".format(path, r'dict\domain', file)
            F = open(filepath, 'r')
            for x in F:
                payload.append(x.replace('\n', ''))
            if flag:
                file = 'domain.txt'
                filepath = "{0}\{1}\{2}".format(path, r'dict\domain', file)
                F = open(filepath, 'r')
                for x in F:
                    payload.append(x.replace('\n', ''))

        payload = list(set(payload))
        return payload

    def run(self,domain,payload,threads):
        '''
        配置线程池
        :param domain:提取到的域名
        :param payload:导入的payload
        :param threads:最大线程数
        :return:
        '''
        URL = []
        report = []
        for x in payload:
            url = 'http://{}.{}'.format(str(x),domain)
            URL.append(url)
        with ThreadPoolExecutor(max_workers=threads) as pool:
            results = pool.map(self.scan,URL)
            for result in results:
                if result['flag'] == 1:
                    print(result['msg'])
                    report.append(result['msg'])
        return report




    def scan(self,url):
        '''
        开始扫描
        :param url:
        :return:
        '''
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        try:
            res = requests.post(url,headers=headers,timeout=10)
            if res.status_code == 200 or res.status_code == 302 or res.status_code == 500 or res.status_code ==502:
                msg = "{0} : {1}".format(res.status_code, url)
                m = {'msg': msg, 'flag': 1}
                return m
        except:
            msg = "[Timeout : {}]".format(url)
            m = {'msg': msg, 'flag': 2}
            return m
        m = {'flag' : 0}
        return m



    def domain_report(self,url,report):
        '''
        导出报告
        :param url: 用作文件夹命名
        :param report: 报告list
        :return:
        '''
        report = list(set(report))
        path = os.path.abspath(os.path.dirname(__file__))
        dirname = urlparse(url).netloc
        dirpath = "{0}\{1}\{2}".format(path, "reports", dirname)
        filepath = "{0}\{1}".format(dirpath, "domain_report.txt")
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        F = open(filepath,'a')
        try:
            for m in report:
                F.write(m + '\n')
            print("[ 网站子域名挖掘报告已存放于：{} ]".format(filepath))
        except:
            print("[ 未能挖掘出网站子域名 ]")
        F.close()
        return


