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
from modules.handle import scanTerminal
from modules.handle import jsTerminal

wrong_web_list = ['javascript:void(0)', None, '###', '#']

class Scan():
    def __init__(self, url, name, crazy):
        self.url = url
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
        self.results = []


    def load_config(self):
        config = Config().readConfig()
        self.timeout = config.getfloat("Scan", "timeout")
        self.threads = config.getint("Scan", "threads")
        self.ICPUrl = config.get("Scan", "ICPUrl")
        self.checkJsStatus = config.getboolean("Scan", "checkJsStatus")
        system = platform.system()
        self.saveType = config.get("Result", system)
        self.Cycles = config.getint("Scan", "cycles")
        self.isThread = False
        self.isShow = True

    def start(self):
        print(self.Output.fuchsia(">>>>>scan" + "-" * 40))
        self.load_config()
        print(self.Output.blue('[ schedule ] ') + self.Output.fuchsia('开始爬取网页链接:') + self.url)
        # 扫描
        self.webScan(self.url)
        self.jsScan(self.Js)
        if self.crazy:
            self.scanmode = 1
            self.crazyWebScan()
        # 输出
        self.output()
        self.saveResult(self.results, 'webScan', 'webScan.txt', cut=' | ')
        print(self.Output.fuchsia("-" * 40 + "<<<<<scan" + "\n"))

    def output(self):
        if self.Phone != []:
            r_phone = list(set(self.Phone))
            if self.isShow:
                phone = self.dealData(r_phone)
                print(self.Output.green('[ output ] ') + self.Output.cyan('手机号码'))
                for x in phone:
                    print(self.Output.blue('[ result ] ') + self.Output.green(x) + self.Output.interval() + phone[x])
            self.saveResult(r_phone, 'phone', 'phone.txt', cut=' | ')
        if self.Email != []:
            r_email = list(set(self.Email))
            if self.isShow:
                email = self.dealData(r_email)
                print(self.Output.green('[ output ] ') + self.Output.cyan('邮箱'))
                for x in email:
                    print(self.Output.blue('[ result ] ') + self.Output.green(x) + self.Output.interval() + email[x])
            self.saveResult(r_email, 'email', 'email.txt', cut=' | ')
        if self.ICP != []:
            r_icp = list(set(self.ICP))
            if self.isShow:
                icp = self.dealData(r_icp)
                print(self.Output.green('[ output ] ') + self.Output.cyan('备案号'))
                for x in icp:
                    print(self.Output.blue('[ result ] ') + self.Output.green(x) + self.Output.interval() + icp[x])
            self.saveResult(r_icp, 'icp', 'icp.txt', cut=' | ')
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
            reports_xlsx.Report(report, self.name, sheetname, banner, lable=cut).save()
        else:
            reports_txt.Report(report, self.name, txtFilename, '网页扫描报告已存放于', '并没有扫描出网页链接').save()

    def dealData(self, data, cut='|'):
        DATA = {}
        for d in data:
            key = d.split(cut)[0].strip()
            value = d.split(cut)[1].strip()
            if key not in DATA.keys():
                DATA[key] = value
        return DATA


    def crazyWebScan(self):
        '''
        循环爬取
        :return:
        '''
        if self.Web != []:   # 进入时判断当前页面是否爬取到链接
            web_sites = set(self.Web)  # 创建新数组
            js_sites = set(self.Js)
            Cycles = 1
            new_urls = util.filter_Url(list(set(self.Web)))
            while 1 and Cycles <= self.Cycles and new_urls != []:
                if self.isShow:
                    print(self.Output.blue('[ schedule ] ') +
                          self.Output.fuchsia(f'第{Cycles}轮遍历爬取 ') +
                          self.Output.green(f'共{len(new_urls)}个链接')
                          )
                Cycles += 1  # 防止无限运行
                self.webScan(new_urls)  # 运行后self.Web会刷新结果
                new_urls = set()           # 重置
                new_js = set()
                # 处理web链接
                for x in self.Web:
                    if x not in web_sites:
                        web_sites.add(x)
                        new_urls.add(x)
                new_urls = util.filter_Url(self.Web)
                # 处理js链接
                for m in self.Js:
                    if m not in js_sites:
                        js_sites.add(m)
                        new_js.add(m)
                new_urls = list(new_urls)
                new_js = list(new_js)
                self.jsScan(new_js)


    def webScan(self, url):
        '''
        爬取当前页面的URL
        :return:
        '''
        handler = scanTerminal.Terminal(scanmode=self.scanmode)  # scanmode暂未实现，保留接口
        REQ = asyncHttp.req(handler=handler)
        if self.isThread:
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(REQ.run(url))
        # 获取结果
        self.Email += handler.capture_Email  # 附加
        self.Phone += handler.capture_Phone  # 附加
        self.ICP += handler.capture_ICP      # 附加
        self.Web = handler.capture_Url       # 重新赋值
        self.Js = handler.capture_Js         # 重新赋值
        self.results += REQ.results
        return

    def jsScan(self, url):
        '''
        分析当前的js文件
        :param url:
        :return:
        '''
        if url == []:
            return
        handler = jsTerminal.Terminal(scanmode=self.scanmode)
        REQ = asyncHttp.req(
            handler=handler,
            workers=self.threads,
            timeout=self.timeout
        )  # 申请异步
        loop = asyncio.get_event_loop()
        loop.run_until_complete(REQ.run(url))
        self.Email += handler.capture_Email  # 附加
        self.Phone += handler.capture_Phone  # 附加
        return


class celery_scan:
    '''
    celery调用模块
    返回新的url进行递归扫描
    '''
    def __init__(self, url, name):
        self.url =url
        self.name = name

    def run(self):
        res = Scan(self.url, self.name, '1')
        new_url = self.same_check(res)
        return new_url

    def same_check(self,res):
        '''
        url相似度的检测
        :param res:爬取的url集
        :return: 同源的url
        '''
        return res
