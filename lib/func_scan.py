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
    def __init__(self, url, name, crazy, Cycles=5):
        self.url = url
        self.name = name
        self.crazy = crazy
        self.Cycles = Cycles   # crazy下的循环最大次数
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
        # 扫描
        self.webScan(self.url)
        self.jsScan(self.Js)
        if self.crazy:
            self.scanmode = 1
            self.crazyWebScan()
        # 输出
        self.output()
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

    def crazyWebScan(self):
        '''
        循环爬取
        :return:
        '''
        if self.Web != []:   # 进入时判断当前页面是否爬取到链接
            web_sites = self.Web  # 创建新数组
            js_sites = self.Js
            Cycles = 1
            new_urls = self.Web   # 初始数据
            while 1 and Cycles <= self.Cycles:
                print(self.Output.blue('[ schedule ] ') +
                      self.Output.fuchsia(f'第{Cycles}轮遍历爬取') +
                      self.Output.green(f'共{len(new_urls)}个链接')
                      )
                Cycles += 1  # 防止无限运行
                self.webScan(new_urls)  # 运行后self.Web会刷新结果
                new_urls = []           # 重置
                new_js = []
                for x in self.Web:
                    if x not in web_sites:
                        web_sites.append(x)
                        new_urls.append(x)
                for m in self.Js:
                    if m not in js_sites:
                        js_sites.append(m)
                        new_js.append(m)
                self.jsScan(new_js)
                if new_urls == []:   # 运行至无新页面
                    break


    def webScan(self, url):
        '''
        爬取当前页面的URL
        :return:
        '''
        handler = scanTerminal.Terminal(scanmode=self.scanmode)  # scanmode暂未实现，保留接口
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
        if url == []:
            return
        handler = jsTerminal.Terminal(scanmode=self.scanmode)
        REQ = asyncHttp.req(handler=handler)
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
