#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import os,sys
import requests,re
from dict import *
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
import time

class Burp():
    def __init__(self,url,file,cookies,threads,flag):
        self.url = self.url_parse(url)
        self.flag = flag
        self .file = file
        self.scan_mode = 0
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        self.cookies = cookies
        self.threads = threads
        self.start(url)

    def start(self,url):
        print('>>>>>burp' + '-' * 40)
        print("[ 开始分析网站：{} ]".format(self.url))
        web_type = self.web_indetify(url)
        if not web_type:
            web_type = self.web_auto_indetify(url)
        print("[ 网站类型：{} ]".format(web_type))
        mode_msg = self.scan_mode_indetify()
        msg = {0:'基于网站状态码检验模式',1:'基于网站页面内容检验模式'}
        print('[ 网站分析模式：{} ]'.format(msg[mode_msg]))
        payloads = self.load_payload(web_type)
        if payloads:
            print('[ payload导入完成 ]')
            reports = self.run(payloads, self.threads)
            if reports:
                self.scan_report(reports)
            else:
                print("[ 并没有扫描出可疑后台 ]")
        else:
            print('[ payload导入失败 ]')
        print('-' * 40 + 'burp<<<<<' + '\n')
        return





    def url_parse(self,url):
        '''
        去除url中的params和query部分
        :param url: 待解析的链接
        :return:url的上级目录
        '''
        parse_url = urlparse(url)
        # print(parse_url)
        try:
            url = parse_url.scheme + '://' + parse_url.netloc + parse_url.path    # 除去参数
        except:
            return url             # 返回IP形式
        if parse_url.path == '/' or parse_url.path == '':
            url = parse_url.scheme + '://' + parse_url.netloc     # url最后不能以/结尾，不然影响添加payload
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
            return ''      # 识别无path情况的url
        if s == None:
            return ''
        else:
            return s.group(2)




    def web_auto_indetify(self,url):
        '''
        自动添加path并识别网页类型
        :param url:
        :return:
        '''
        for i in ['/index.php','/index.asp','/index.aspx','/index.mdb']:
            URL = "{0}{1}".format(url,i)
            try:
                res = requests.post(URL,cookies=self.cookies,headers=self.headers,timeout=5)
                if res.status_code == 200:
                    m = self.web_indetify(URL)
                    return m
            except:
                pass
        return '未能识别'


    def load_payload(self,type):
        '''
        根据网站类型加载相应payload
        :param type: 网站类型
        :return: payloads
        '''
        payloads = []
        if type == 'php':
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
        if self.file:
            F = open(self.file,'r')
            for x in F:
                try:
                    t = x.replace('\n','')
                    payloads.append(t)
                except:
                    # print('文件读取失败')
                    return
        else:
            file = 'dicc.txt'
            payloadpath = "{0}\{1}\{2}".format(path, r'dict\burp', file)
            F = open(payloadpath, "r")
            for x in F:
                try:
                    t = '/' + x.replace('\n','')
                    payloads.append(t)
                except:
                    pass
            F.close()
            if filename != '' and self.flag:         # 此模块需要启动极致模式
                filepath = "{0}\{1}\{2}".format(path,r'dict\burp',filename)
                f = open(filepath,'r')
                for x in f:
                    payloads.append(x.replace('\n',''))
                    # print(x.replace('\n',''))
                f.close()
            payloads = list(set(payloads))
        return payloads

    def scan_mode_indetify(self):
        '''
        用bad_payload去访问，获取出错页面的情况
        :return:
        '''
        impossible_payload = ['/aaaaaaaaaaaaaaaaaaaa','/bbbbbbbbbbbbbbbb','/asodhpfpowehrpoadosjfho']   # 无中生有的payload
        res = self.run(impossible_payload,3)
        if res:
            self.scan_mode = 1
            return 1
        return 0


    def run(self,payloads,threads):
        '''
        调用线程池
        :param payloads: 导入的payload
        :param threads: 最大线程数
        :return:
        '''
        URL = []
        reports = []
        for x in payloads:
            url = self.url + x
            URL.append(url)
        with ThreadPoolExecutor(max_workers=threads) as pool:
            if self.scan_mode:
                results = pool.map(self.text_scan, URL)
            else:
                results = pool.map(self.sites_scan,URL)
            for result in results:
                if result['flag'] != 0:     # 选择性输出
                    print(result['msg'])
                    if result['flag'] == 1:
                        reports.append(result['msg'])
            return reports


    def sites_scan(self,url):
        '''
        根据网站状态码识别后台
        :param url:
        :return:
        '''
        try:
            res = requests.post(url,cookies=self.cookies,headers=self.headers,timeout=10)
            status = res.status_code
            if status == 200 or status == 302 or status == 500 or status == 502:
                msg = "{0} : {1}".format(status,url)
                m = {'msg':msg,'flag':1}
                return m
        except:
            msg = "[Timeout : {}]".format(url)
            m = {'msg': msg, 'flag': 2}
            return m
        m = {'flag':0}
        return m

    def text_scan(self,url):
        '''
        根据页面信息检测网站，用于判断自定义错误页面的网站
        :param url:
        :return:
        '''
        bm = []
        bad_msg = ['404','页面不存在','不可访问','page can\'t be found']    # 用于检测页面自定义报错的信息
        try:
            res = requests.post(url,cookies=self.cookies,headers=self.headers,timeout=10)
            for msg in bad_msg:
                if msg in res.text:
                    bm.append(msg)
            if len(bm)>5:                        # 若报错信息超过一定数量可视为文章自带内容
                msg = "{0} : {1}".format(res.status_code, url)
                m = {'flag':1,'msg':msg}
            else:
                m = {'flag':0,'msg':bm}
        except:
            m = {'flag':2,'msg':'[Timeout : {}]'.format(url)}
        return m


    def scan_report(self,reports):
        '''
        导出报告
        :param reports:
        :return:
        '''
        path = os.path.abspath(os.path.dirname(__file__))
        parse_url = urlparse(self.url)
        dirname = parse_url.netloc
        dirpath = "{0}\{1}\{2}".format(path, "reports", dirname)
        filepath = "{0}\{1}".format(dirpath, "burp_report.txt")
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        F = open(filepath,'a')
        try:
            for m in reports:
                F.write(m + '\n')
            print("[ 网站目录爆破报告已存放于：{}]".format(filepath))
        except:
            print("[ 并没有扫描出可疑后台 ]")
        F.close()
        return




