#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import re
import time
import asyncio
from modules.func import util
from .color_output import *
from .load_config import Config
from reports import reports_xlsx,reports_txt
from modules.func import asyncHttp
from modules.terminal import scanTerminal
from modules.terminal import jsTerminal

wrong_web_list = ['javascript:void(0)', None, '###', '#']

class Scan():
    def __init__(self, url, REQ, name, crazy):
        self.url = url
        self.REQ = REQ
        self.name = name
        self.crazy = crazy
        self.Output = ColorOutput()
        # 数据区
        self.scanmode = 0
        self.Phone = []
        self.Email = []
        self.ICP = []
        self.Js = []
        self.Web = []


    def load_config(self):
        config = Config().readConfig()
        self.timeout = config.getfloat("Scan", "timeout")
        self.threads = config.getint("Scan", "threads")
        self.ICPUrl = config.get("Scan", "ICPUrl")
        self.checkJsStatus = config.getboolean("Scan", "checkJsStatus")
        system = platform.system()
        self.saveType = config.get("Result", system)

    def start(self):
        print(self.Output.fuchsia(">>>>>scan" + "-" * 40))
        self.load_config()
        print(self.Output.blue('[ schedule ] ') + self.Output.fuchsia('开始爬取网页链接:') + self.url)
        self.webScan(self.url)   # 扫描
        self.jsScan(self.Js)
        self.output()   # 输出
        print(self.Output.fuchsia("-" * 40 + "<<<<<scan" + "\n"))

    def output(self):
        if self.Phone != []:
            print()
            print(self.Output.green('[ output ] ') + self.Output.cyan('手机号码'))
            for x in self.Phone:
                print(self.Output.blue('[ result ] ') + self.Output.green(x))
            self.saveResult(self.Phone, 'phone', 'phone.txt', cut=' | ')
        if self.Email != []:
            print()
            print(self.Output.green('[ output ] ') + self.Output.cyan('邮箱'))
            for x in self.Email:
                print(self.Output.blue('[ result ] ') + self.Output.green(x))
            self.saveResult(self.Email, 'email', 'email.txt', cut=' | ')
        if self.ICP != []:
            print()
            print(self.Output.green('[ output ] ') + self.Output.cyan('备案号'))
            for x in self.ICP:
                print(self.Output.blue('[ result ] ') + self.Output.green(x))
            self.saveResult(self.ICP, 'icp', 'icp.txt', cut=' | ')
        return

    def saveResult(self, report, sheetname='', txtFilename='', cut=':'):
        if report == []:
            print(self.Output.blue('[ result ] ') + self.Output.yellow("[ {}扫描结果为空 ]".format(sheetname)))
            return
        if self.saveType == 'xlsx':
            if sheetname == 'webScan':
                banner = ['状态码', '文本长度', '标题', 'URL']
            elif sheetname == 'webScanWithoutCheck':
                banner = ['URL']
            elif sheetname == 'phone':
                banner = ['手机号码', '捕获页面']
            elif sheetname == 'email':
                banner = ['邮箱', '捕获页面']
            elif sheetname == 'icp':
                banner = ['备案号', '捕获页面']
            else:
                banner = []
            reports_xlsx.Report(report, self.name, sheetname, banner, cut=cut).save()
        else:
            reports_txt.Report(report, self.name, txtFilename, '网页扫描报告已存放于', '并没有扫描出网页链接').save()


    def crazyRun(self,urls):
        '''
        递归各相对路径，尝试找出可疑的302等页面
        :param urls:
        :return:
        '''
        paths = []
        http = re.compile('http')
        for u in urls:
            if http.match(u):  # 属于完整链接
                pass
            else:
                u = u.lstrip('.')  # 除去左端点号
                u = u.lstrip('/')  # 除去左端/号
                for p in range(u.count('/')):
                    x = u.rsplit('/', p + 1)[0]
                    if x not in paths:
                        paths.append(x)
        return paths



    def webScan(self, url):
        '''
        爬取当前页面的URL
        :return:
        '''
        handler = scanTerminal.Terminal(scanmode=self.scanmode)
        REQ = asyncHttp.req(handler=handler)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(REQ.run(url))
        # 获取结果
        self.Email += handler.capture_Email  # 附加
        self.Phone += handler.capture_Phone  # 附加
        self.ICP += handler.capture_ICP      # 附加
        self.Web = handler.capture_Url       # 重新赋值
        self.Js = handler.capture_Js         # 重新赋值
        return

    def jsScan(self, url):
        '''
        分析当前的js文件
        :param url:
        :return:
        '''
        handler = jsTerminal.Terminal()
        REQ = asyncHttp.req(handler=handler)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(REQ.run(url))
        return


class celery_scan:
    '''
    celery调用模块
    返回新的url进行递归扫描
    '''
    def __init__(self,url,REQ,name):
        self.url =url
        self.REQ = REQ
        self.name = name

    def run(self):
        res = Scan(self.url, self.REQ, self.name, '1')
        new_url = self.same_check(res)
        return new_url

    def same_check(self,res):
        '''
        url相似度的检测
        :param res:爬取的url集
        :return: 同源的url
        '''
        return res
