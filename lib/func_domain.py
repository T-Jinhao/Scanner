#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import requests
import os
import re
import hashlib
import time
import dns.resolver
from urllib.parse import urlparse
from reports import reports
from concurrent.futures import ThreadPoolExecutor
from .color_output import color_output

class Domain:
    def __init__(self,url,payload,threads,timeout,flag):
        self.domain = self.url_check(url)
        self.payload = payload
        self.threads = threads
        self.timeout = timeout
        self.flag = flag
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }

    def start(self):
        color_output('>>>>>domain' + '-' * 40)
        report = []
        if self.domain:
            check = input("当前域名 {} 是否正确解析？[正确则回车，否则输入正确的域名]\n".format(self.domain))  # 防止出错
            if check:
                self.domain = check
            self.panAnalysis(self.domain)
            color_output("[ 开始爆破域名: {} ]".format(self.domain), color='BLUE')
            onlineReport = self.chinaz_search()    # 在线查询接口获得的数据
            payload = self.load_payload(onlineReport)   # 合并数据
            if payload:
                color_output('[ payload导入完成 ]', color='MAGENTA')
                report = self.run(self.domain, payload, self.threads)
            else:
                color_output('[ payload导入失败 ]', color='RED')
            if report:
                reports.Report(report, self.url, 'domain_report.txt', '网站子域名挖掘报告已存放于', '未能挖掘出网站子域名')
            else:
                color_output("[ 未能挖掘出网站子域名 ]", color='YELLOW')
        else:
            color_output("[ {}不支持子域名挖掘 ]".format(self.url), color='YELLOW')
        color_output('-' * 40 + 'domain<<<<<' + '\n')
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
        url = "https://tool.chinaz.com/subdomain/?domain={}&page=1".format(self.domain)
        rePage = re.compile(r'共(.+?)页')
        try:
            res = requests.get(url, headers=self.headers, timeout=self.timeout)
            pagenum = rePage.findall(res.text)[0]
            pagenum = int(pagenum)
        except:
            color_output('在线api没有获取数据', color='YELLOW')
            return []

        for i in range(1, pagenum+1):
            url = "https://tool.chinaz.com/subdomain/?domain={}&page={}".format(self.domain, i)
            res = requests.get(url, headers=self.headers, timeout=self.timeout)
            domain = re.compile('[\w]+\.{}'.format(self.domain))    # 正则提取子域名
            domains = domain.finditer(res.text)
            if domains == []:
                break
            for d in domains:
                if d.group() not in report:
                    # color_output(d.group(), color='GREEN')  # 未知是否存活，不输出
                    report.append(d.group())
        return report


    def load_payload(self, report):
        '''
        读取payload
        数据合并并去重
        :param report: 在线子域名数据
        :return:
        '''
        payload = []
        path = os.path.dirname(__file__)
        if self.payload:   # 已设置好payload
            return self.payload

        file = 'dict.txt'
        filepath = "{0}/{1}/{2}".format(path, r'../dict/domain', file)
        F = open(filepath, 'r')
        for x in F:
            payload.append(x.replace('\n', ''))
        # if flag:
        #     file = 'domain.txt'
        #     filepath = "{0}/{1}/{2}".format(path, r'../dict/domain', file)
        #     F = open(filepath, 'r')
        #     for x in F:
        #         payload.append(x.replace('\n', ''))
        payload += report
        payload = list(set(payload))   # payload去重
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
                    color_output(result['msg'], color='GREEN')
                    report.append(result['msg'])
        return report


    def getDomainType(self, url):
        '''
        获取域名解析记录类型
        :param url:
        :return:
        '''
        domain = url.replace('http://', '')
        ans = dns.resolver.query(domain)
        res = ans.response.answer
        res_type = str(type(res[0][0])).split('.')[3]
        return res_type


    def panAnalysis(self, domain):
        '''
        以随机数拼接查看是否会存在泛解析
        :param domain:
        :return:
        '''
        ranstr = hashlib.md5(domain.encode()).hexdigest()
        ranstr1 = ranstr[:4]
        ranstr2 = ranstr[-4:]
        url1 = "http://{}.{}".format(ranstr1, domain)
        url2 = "http://{}.{}".format(ranstr2, domain)
        try:
            res1 = requests.get(url1, headers=self.headers, timeout=self.timeout)
            res2 = requests.get(url2, headers=self.headers, timeout=self.timeout)
            color_output("[{} 存在泛解析]".format(domain), color='YELLOW')
            time.sleep(3)
        except:
            pass
        return


    def scan(self,url):
        '''
        开始扫描
        :param url:
        :return:
        '''
        try:
            res = requests.post(url,headers=self.headers, timeout=self.timeout)   # 高并发，单独创建对象
            if res.status_code == 200 or res.status_code == 302 or res.status_code == 500 or res.status_code ==502:
                res_type = self.getDomainType(url)
                msg = "{0} : {1} : {2}".format(res.status_code, res_type, url)
                m = {'msg': msg, 'flag': 1}
                return m
        except:
            msg = "[Timeout : {}]".format(url)
            m = {'msg': msg, 'flag': 2}
            return m
        m = {'flag' : 0}
        return m

class celery_domain:
    def __init__(self,url,payload):
        self.url = url
        self.payload = payload

    def run(self):
        x = Domain(self.url,self.payload,20,5,False).start()
        return
