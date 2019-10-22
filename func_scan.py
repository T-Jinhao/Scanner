#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import os,sys
import requests,re
from dict import *
from urllib.parse import urlparse
import threading
import time

class Scan():
    def __init__(self,url,cookies):
        self.url = self.url_parse(url)
        self.sites_reports = []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        self.cookies = cookies
        print('>>>>>scan'+'-'*40)
        print("[ 开始分析网站：{} ]".format(self.url))
        web_type = self.web_indetify(url)
        print("[ 网站类型：{} ]".format(web_type))
        payloads = self.load_payload(web_type)
        print('[ payload导入完成 ]')
        self.run(payloads)
        self.scan_report(self.sites_reports)
        print('-'*40+'scan<<<<<'+'\n')





    def url_parse(self,url):
        '''
        去除url中的params和query部分
        :param url: 待解析的链接
        :return:url的上级目录
        '''
        parse_url = urlparse(url)
        try:
            url = parse_url.scheme + '://' + parse_url.netloc + parse_url.path
        except:
            return url               # 返回IP形式
        if parse_url.path == '':
            return url
        else:
            url = url.rsplit('/', 1)
            if re.match('(.*?)\.(.*?)', url[1]):
                return url[0]
            else:
                x = url[0] + '/' + url[1]
                return x


    def web_indetify(self,url):
        '''
        分析网站类型
        :param url:
        :return: 网站类型
        '''
        parse_url = urlparse(url)
        path = parse_url.path
        path = path.rsplit('/', 1)
        try:
            s = re.match('(.*?)\.(.*)', path[1])
        except:
            return '未知'      # 识别无path情况的url
        if s == None:
            return '未知'
        else:
            return s.group(2)


    def load_payload(self,type):
        '''
        根据网站类型加载响应payload，但最终都会加载完整的cgi.list
        :param type: 网站类型
        :return: payloads
        '''
        file = 'cgi.list'
        payloads = []
        if type == '未知' :
            filename = ''
        elif type == 'php':
            filename = 'PHP.txt'
        elif type == 'asp':
            filename = 'ASP.txt'
        elif type == 'aspx':
            filename = 'ASPX.txt'
        elif type == 'mdb':
            filename = 'MDB.txt'
        else:
            filename = ''
        path = os.path.abspath(os.path.dirname(__file__))
        if filename != '':
            filepath = "{0}\{1}\{2}".format(path,'dict\scan',filename)
            f = open(filepath,'r')
            for x in f:
                payloads.append(x.replace('\n',''))
                # print(x.replace('\n',''))
            f.close()

        payloadpath = "{0}\{1}\{2}".format(path, 'dict\scan', file)
        F = open(payloadpath,'rb')
        for x in F:
            try:
                payloads.append(x.decode('gb2312').replace('\n',''))
            except:
                pass
        F.close()
        return payloads


    def run(self,payloads):
        '''
        部署网站路径扫描
        :param payloads:
        :return:
        '''
        Threads = []
        for x in payloads:
            url = self.url + x
            thread = threading.Thread(target=self.sites_scan,args=(url,))
            Threads.append(thread)
        for t in Threads:
            t.start()
            t.join()
            # self.sites_scan(url)


    def sites_scan(self,url):
        '''
        根据网站状态码识别后台
        :param url:
        :return:
        '''
        res = requests.post(url,cookies=self.cookies,timeout=5)
        status = res.status_code
        if status == '200' or status == '302':
            msg = "{0} : {1}".format(status,url)
            print(msg)
            self.sites_reposts.append(msg)
        return False


    def scan_report(self,report):
        path = os.path.abspath(os.path.dirname(__file__))
        dirname = self.url.replace("https://", "")
        dirpath = "{0}\{1}\{2}".format(path, "reports", dirname)
        filepath = "{0}\{1}".format(dirpath, "scan_report.txt")
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        F = open(filepath,'a')
        try:
            print("[ 网站后台扫描报告已存放于：{}]".format(filepath))
            for m in report:
                F.write(m + '\n')
        except:
            print("[ 并没有扫描出可疑后台 ]")
        F.close()
        return




