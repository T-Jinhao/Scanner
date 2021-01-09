#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import os
import re
from reports import reports
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from .color_output import color_output,color_list_output
from modules import util

class Burp():
    def __init__(self, url, payload, REQ, name, flag):
        self.url = self.url_parse(url).rstrip('/')
        self.flag = flag
        self.name = name
        self.payload = payload
        self.scan_mode = 0
        self.REQ = REQ


    def start(self):
        url = self.url
        color_output('>>>>>burp' + '-' * 40)
        color_output("[ 开始分析网站：{} ]".format(self.url), color='BLUE')
        web_type = self.web_indetify(url)
        if not web_type:
            web_type = self.web_auto_indetify(url)
        color_output("[ 网站类型：{} ]".format(web_type), color='CYAN')
        mode_msg = self.scan_mode_indetify()
        msg = {0:'基于网站状态码检验模式',1:'基于网站页面内容检验模式'}
        color_output('[ 网站分析模式：{} ]'.format(msg[mode_msg]), color='CYAN')
        payloads = self.load_payload(web_type)
        if payloads:
            color_output('[ payload导入完成 ]', color='MAGENTA')
            report = self.run(payloads)
            if report:
                color_list_output(report, color='GREEN')
                reports.Report(report, self.name, 'burp_report.txt', '网站目录爆破报告已存放于', '并没有扫描出可疑后台').save()
            else:
                color_output("[ 并没有扫描出可疑后台 ]", color='YELLOW')
        else:
            color_output('[ payload导入失败 ]', color='RED')
        color_output('-' * 40 + 'burp<<<<<' + '\n')
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
        for i in ['/index.php','/index.asp','/index.aspx','/index.mdb','/index.jsp']:
            URL = "{0}{1}".format(url, i)
            try:
                res = self.REQ.autoGetAccess(url)
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
        elif type == 'jsp':
            filename = 'JSP.txt'
        else:
            filename = ''

        path = os.path.dirname(__file__)
        if self.payload:   # 已设置payload
            return self.payload

        file = 'dicc.txt'
        payloadpath = "{0}/{1}/{2}".format(path, r'../dict/burp', file)
        F = open(payloadpath, "r")
        for x in F:
            try:
                t = '/' + x.replace('\n','')
                payloads.append(t)
            except:
                pass
        F.close()

        if filename != '' and self.flag:         # 此模块需要启动极致模式
            filepath = "{0}/{1}/{2}".format(path, r'../dict/burp', filename)
            f = open(filepath,'r')
            for x in f:
                payloads.append(x.replace('\n', ''))
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
        res = self.run(impossible_payload)
        if res:
            self.scan_mode = 1
            return 1
        return 0


    def run(self,payloads):
        '''
        调用线程池
        :param payloads: 导入的payload
        :return:
        '''
        URL = []
        reports = []
        for x in payloads:
            url = self.url + x
            URL.append(url)
        if self.scan_mode:
            results = self.text_scan(URL)
        else:
            results = self.status_scan(URL)

        for result in results:
            if result['flag'] != 0:  # 选择性输出
                if result['flag'] == 1:
                    # color_output(result['msg'], color='GREEN')
                    reports.append(result['msg'])
                else:
                    pass
                    # color_output(result['msg'], color='YELLOW')

        return reports


    def status_scan(self, url):
        '''
        根据网站状态码识别后台
        :param url:
        :return:
        '''
        report = []
        exist_list = []
        resp = self.REQ.mGetAsyncAccess(url)
        for r in resp:
            m = {'flag': 0}
            try:
                status = r.status_code
                if status == 200 or status == 302 or status == 500 or status == 502:
                    check_msg = {r.url: r.headers.get('Content-Length')}
                    if check_msg not in exist_list:
                        exist_list.append(check_msg.copy())
                        msg = "{status} : {len} : {title} : {url}".format(
                            status=status,
                            len=r.headers.get('Content-Length'),
                            title=util.getTitle(r.text),
                            url=r.url
                        )
                        m = {'msg': msg, 'flag': 1}
            except:
                pass
            report.append(m.copy())
        return report

    def text_scan(self, url):
        '''
        根据页面信息检测网站，用于判断自定义错误页面的网站
        :param url:
        :return:
        '''
        exist_list = []
        report = []
        bm = []
        bad_msg = ['404','页面不存在','不可访问','page can\'t be found','无法加载模块']    # 用于检测页面自定义报错的信息
        resp = self.REQ.mGetAsyncAccess(url)
        for r in resp:
            try:
                for msg in bad_msg:
                    if msg in r.text:
                        bm.append(msg)
                check_msg = {r.url: r.headers.get('Content-Length')}
                if check_msg not in exist_list:
                    exist_list.append(check_msg.copy())
                    if len(bm) > 5:                        # 若报错信息超过一定数量可视为文章自带内容
                        msg = "{status} : {len} : {title} : {url}".format(
                            status=r.status_code,
                            len=len(r.get('Content-Length')),
                            title=util.getTitle(r.text),
                            url=url
                        )
                        m = {'flag':1,'msg':msg}
                    else:
                        m = {'flag':0,'msg':bm}
                    report.append(m.copy())
            except:
                pass
        return report


class celery_burp:
    '''
    celery调用模块
    '''
    def __init__(self, url, payload, REQ, name, flag):
        self.url = url
        self.payload = payload
        self.REQ = REQ
        self.flag = flag
        self.name = name

    def run(self):
        x = Burp(self.url, self.payload, self.REQ, self.name, self.flag).start()    # 线程有所减少
        return


