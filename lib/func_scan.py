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
        self.checkWebStatus = config.getboolean("Scan", "checkWebStatus")
        self.checkJsStatus = config.getboolean("Scan", "checkJsStatus")
        system = platform.system()
        self.saveType = config.get("Result", system)

    def start(self):
        print(self.Output.fuchsia(">>>>>scan" + "-" * 40))
        self.load_config()
        print(self.Output.blue('[ schedule ] ') + self.Output.fuchsia('开始爬取网页链接:') + self.url)
        self.webScan(self.url)   # 扫描
        print(self.Web)
        exit()


        # if web:   # 检测爬取链接的存活性
        #     if self.checkWebStatus:
        #         web += self.crazyRun(web)
        #         res = self.statusCheck(web)
        #         self.saveResult(res, sheetname='webScan', txtFilename='webScan_report.txt', cut=' | ')
        #     else:
        #         print(self.Output.blue('[ Setting ] ') + self.Output.fuchsia('checkWebStatus ')
        #               + self.Output.yellow(self.checkWebStatus))
        #         for x in web:
        #             print(self.Output.green('[ webURL ] ') + x)
        #         self.saveResult(web, sheetname='webScanWithoutCheck', txtFilename='webScanWithoutCheck_report.txt', cut=' | ').save()
        # else:
        #     print(self.Output.blue('[ result ] ') + self.Output.yellow('没有扫描到网站链接'))
        #
        # if js and self.checkJsStatus:    # 寻找js文件内的中文字符
        #     print(self.Output.blue('[ schedule ] ') + self.Output.cyan('JS文件分析'))
        #     for u in js:
        #         self.js_analysis(u)    # 寻找敏感信息

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
                # 暂不启用
                # data = {
                #     'pageNo': 1,
                #     'pageSize': 20,
                #     'Kw': x.split('-')[0]
                # }
                # r = self.REQ.autoPostAccess(url=self.ICPUrl, data=data)
                # print(r.text)
            self.saveResult(self.ICP, 'icp', 'icp.txt', cut=' | ')
        print(self.Output.fuchsia("-" * 40 + "<<<<<scan" + "\n"))
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


    def statusCheck(self,urls):
        '''
        测试链接是否可用
        :param urls: 爬取到的url
        :return:
        '''
        result = []
        for url in list(set(urls)):
            print()
            print(self.Output.fuchsia('[ Test ]') + url)
            try:
                res = self.REQ.autoGetAccess(url, threads=self.threads, timeout=self.timeout)
                title = util.getTitle(res.text)
                print(self.Output.green('[ Info ] ')
                      + self.Output.fuchsia('状态码') + self.Output.green(res.status_code) + self.Output.interval()
                      + self.Output.fuchsia('文本长度') + self.Output.green(len(res.content)) + self.Output.interval()
                      + self.Output.fuchsia('标题') + self.Output.green(title)
                      )
                if res.status_code != 404 and len(res.content) != 0:
                    msg = " | ".join([str(res.status_code), str(len(res.content)), str(title), url])
                    result.append(msg)
            except:
                print(self.Output.green('[ Info ] ') + self.Output.yellow('访问失败'))
            time.sleep(0.5)   # 防止过于频繁导致网站崩溃
        return result

    # def js_analysis(self, url):
    #     '''
    #     找出js文件内的中文字符
    #     :return:
    #     '''
    #     compile_CN = re.compile(u"[\u4e00-\u9fa5]")   # 匹配中文
    #     print()
    #     print(self.Output.fuchsia('[ Scan ] ') + url)
    #     try:
    #         res = self.REQ.autoGetAccess(url, threads=self.threads, timeout=self.timeout)
    #         content = str(res.content.decode('utf-8'))
    #         self.match_Phone(res.text, url)
    #         self.match_Email(res.text, url)
    #         self.reg_str(res.text)
    #         ret = compile_CN.findall(content)
    #         if ret != []:
    #             print(self.Output.green('[ output ] ') + self.Output.cyan('文件中文爬取'))
    #             ret = ''.join(ret)
    #             print(self.Output.blue('[ result ] ') + self.Output.green(ret))
    #     except Exception:
    #         pass
    #     return


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
