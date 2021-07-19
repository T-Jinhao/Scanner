#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import re
import asyncio
import yarl
import datetime
from reports import reports_txt,reports_xlsx
from urllib.parse import urlparse
from .color_output import *
from .load_config import Config
from modules.func import util
from modules.handle import burpTerminal
from modules.func import asyncHttp
from model import pgsql
from model.BurpModel import BurpModel

class Burp():
    def __init__(self, url, payload, name, flag):
        self.url = self.url_parse(url).rstrip('/')
        self.proto_url = url
        self.flag = flag
        self.name = name
        self.payload = payload
        self.scan_mode = 0
        self.Output = ColorOutput()

    def load_config(self):
        config = Config().readConfig()
        self.threads = config.getint("Burp", "threads")
        self.timeout = config.getfloat("Burp", "timeout")
        system = platform.system()
        self.saveType = config.get("Result", system)
        self.isThread = False
        self.isShow = True

    def start(self):
        print(self.Output.fuchsia('>>>>>burp' + '-' * 40))
        print(self.Output.blue('[ schedule ] ') + self.Output.fuchsia('开始分析网站: ') + self.Output.cyan(self.url))
        self.load_config()
        payloads = self.autoLoad(self.proto_url)
        if not payloads:   # 空白payload数组
            print(self.Output.blue('[ Load ]') + self.Output.red('payload导入失败'))
            print(self.Output.fuchsia('-' * 40 + 'burp<<<<<' + '\n'))
            return
        print(self.Output.blue('[ Load ] ') + self.Output.green('payload导入完成，数量：{}'.format(len(payloads))))
        report = self.run(self.proto_url, payloads)
        if self.flag:   # 递归403页面爆破
            pass
        self.saveResult(report)
        self.insertData(report)


    def autoLoad(self, baseUrl):
        '''
        自动识别并加载payload
        :param baseUrl: 基础URL
        :return:
        '''
        web_type = self.web_indetify(baseUrl)
        if web_type == '':
            web_type = self.web_auto_indetify(baseUrl)
        print(self.Output.blue('[ schedule ] ') + self.Output.fuchsia('网站类型: ') + self.Output.cyan(web_type))
        mode_msg = self.scan_mode_indetify(baseUrl)
        msg = {0: '基于网站状态码检验模式', 1: '基于网站页面内容检验模式'}
        print(self.Output.blue('[ schedule ] ') + self.Output.fuchsia('分析模式: ') + self.Output.cyan(msg[mode_msg]))
        sys.stdout.flush()
        payloads = self.load_payload(web_type)
        return payloads

    def autoRun(self):
        pass

    def saveResult(self, report):
        if report == []:
            print(self.Output.blue('[ result ] ') + self.Output.yellow("[ 并没有扫描出可疑后台 ]"))
            return
        if self.saveType == 'xlsx':
            banner = ['网页状态码', '文本长度', '页面标题', 'URL']
            lable = ['status_code', 'content_length', 'title', 'url']
            reports_xlsx.Report(report, self.name, 'Burp', banner, lable=lable).save()
        else:
            reports_txt.Report(report, self.name, 'burp_report.txt', '网站目录爆破报告已存放于', '并没有扫描出可疑后台').save()
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


    def web_indetify(self, url):
        '''
        分析网站类型
        :param url:
        :return: 网站类型
        '''
        u = yarl.URL(url)
        try:
            name = u.name.split('.')[-1]   # 可能为空格
            return name
        except :
            return ''


    def web_auto_indetify(self, baseUrl):
        '''
        自动添加path并识别网页类型
        :return:
        '''
        # web_type = []
        sites = ['/index.php', '/index.asp', '/index.aspx', '/index.mdb', '/index.jsp']
        res = self.run(baseUrl, sites)
        if len(res) > 1 or res == []:
            return '未能识别'
        else:
            web_type = self.web_indetify(res[0]['url'])
            return web_type

    def load_payload(self, type):
        '''
        根据网站类型加载相应payload
        :param type: 网站类型
        :return: payloads
        '''
        if self.payload:   # 已设置payload
            return self.payload

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
        if filename != '':
            filepath = "{0}/{1}/{2}".format(path, r'../dict/burp', filename)
            f = open(filepath, 'r')
            for x in f:
                payloads.append(x.replace('\n', ''))
            f.close()

        elif filename == '':   # 未能识别网站类型
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
        payloads = list(set(payloads))
        return payloads

    def scan_mode_indetify(self, baseUrl):
        '''
        用bad_payload去访问，获取出错页面的情况
        :return:
        '''
        impossible_payload = ['/aaaaaaaaaaaaaaaa','/bbbbbbbbbbbbbbbb','/asodhpfpowehrpoadosjfho']   # 无中生有的payload
        res = self.run(baseUrl, impossible_payload)
        if res != []:
            self.scan_mode = 1
            return 1
        return 0


    def run(self, baseUrl, payloads):
        '''
        调用异步请求
        :param payloads: 导入的payload
        :return:
        '''
        URL = [baseUrl.rstrip('/')+x for x in payloads]
        handler = burpTerminal.Terminal(scanmode=self.scan_mode, isShow=self.isShow)  # 获取文本处理对象+分类检测
        REQ = asyncHttp.req(
            handler=handler,
            workers=self.threads,
            timeout=self.timeout
        )   # 申请异步
        if self.isThread:   # 多线程异步
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(REQ.run(URL))
        results = REQ.results   # 获取结果
        # loop.close()
        return results

    def insertData(self, data, tasknameid=''):
        '''
        保存数据进入数据库
        :param data:
        :param tasknameid:
        :return:
        '''
        for d in data:
            d['taskname'] = self.name
            d['timestamp'] = datetime.datetime.now()
            d['tasknameid'] = tasknameid
            pgsql.insert(BurpModel, data=d)
        return



class celery_burp:
    '''
    celery调用模块
    '''
    def __init__(self, url, payload, name, flag):
        self.url = url
        self.payload = payload
        self.flag = flag
        self.name = name

    def run(self):
        x = Burp(self.url, self.payload, self.name, self.flag).start()    # 线程有所减少
        return


