#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import re
import hashlib
import dns.resolver
import aiohttp
import asyncio
import json
import yarl
import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from reports import reports_txt, reports_xlsx
from .color_output import *
from .load_config import Config
from modules.func import util
from modules.handle import subdomainTerminal
from modules.func import asyncHttp
from modules.func import gevent_requests
from model import pgsql
from model.DomainModel import DomainModel



class Domain:
    def __init__(self, url, payload,  name, flag):
        self.domain = self.url_check(url)
        self.payload = payload
        self.REQ = gevent_requests.Concurrent()
        self.flag = flag
        self.name = name
        self.url = url
        self.Domain_List = []
        self.IP_list = {}
        self.scanmode = 0
        self.Output = ColorOutput()

    def load_config(self):
        config = Config().readConfig()
        self.threads = config.getint("Domain", "threads")
        self.timeout = config.getfloat("Domain", "timeout")
        self.domain2IP = config.getboolean("Domain", "domain2IP")
        self.showIP = config.getboolean("Domain", "showIP")
        self.max_workers = config.getint("Domain", "max_workers")
        chkStatus = config.get("Domain", "chkStatus")
        self.chkStatus = json.loads(chkStatus)
        system = platform.system()
        self.saveType = config.get("Result", system)
        self.isThread = False
        self.isShow = True


    def start(self):
        self.load_config()
        print(self.Output.fuchsia('>>>>>domain' + '-' * 40))
        if not self.domain:
            print(self.Output.yellow('[ warn ] ') + self.Output.cyan("[ {}不支持子域名挖掘 ]".format(self.url)))
            print(self.Output.fuchsia('-' * 40 + 'domain<<<<<' + '\n'))
            return

        report = []
        # 检测是否存在泛解析
        self.panAnalysis(self.domain)

        # 调用rapiddns.io进行在线获取
        print(self.Output.blue('[ schedule ] ') + self.Output.fuchsia('开始爆破域名:') + self.Output.green(self.domain))
        if self.flag:
            report = self.onlineMethod(self.domain)

        # 普通模式及rapid获取数据失败的情况下，使用字典爆破
        if report == []:
            self.flag = False   # 更改为普通模式，用作保存时区别
            # onlineReport = self.chinaz_search()  # chinaz在线查询接口获得的数据
            payload = self.load_payload(report)  # 合并数据
            if payload:
                print(self.Output.blue('[ Load ] ') + self.Output.green('payload导入完成，数量：{}'.format(len(payload))))
                report = self.run(payload)   # 运行爆破
            else:
                print(self.Output.blue('[ Load ] ') + self.Output.red('payload导入失败'))
        self.saveDomainResult(report)
        self.insertSubDomainData(report)
        if self.IP_list:
            self.saveIpResult(self.IP_list)
        print(self.Output.fuchsia('-' * 40 + 'domain<<<<<' + '\n'))
        return

    def onlineMethod(self, domain):
        '''
        在线查询模式
        :param domain:
        :return:
        '''
        report = []
        if self.isShow:
            print(self.Output.blue('[ schedule ] ') + self.Output.cyan('正在运行在线查询，请耐心等待'))
            print(self.Output.yellow('[ warn ] ') + self.Output.fuchsia('该过程请挂载代理，否则可能会访问超时，导致获取数据失败'))
        urls = self.rapidSearch(domain)
        if urls == []:
            if self.isShow:
                print(self.Output.yellow('[ warn ] ') + self.Output.fuchsia('-X模式查询失败，稍后将执行payload爆破'))
        else:
            report = self.run(urls)
        return report

    def saveDomainResult(self, report):
        '''
        保存域名结果
        :param report:
        :return:
        '''
        if report == []:
            print(self.Output.blue('[ result ] ') + self.Output.yellow('[ 未能挖掘出网站子域名 ]'))
            return
        if self.saveType == 'xlsx':
            banner = ['状态码', '初始URL', '标题', '文本长度', '跳转记录', '最终URL']
            sheetname = 'subDomain'
            lable = ['status_code', 'protourl', 'title', 'content_length','ip', 'url']
            reports_xlsx.Report(report, self.name, sheetname, banner, lable=lable).save()
        else:
            reports_txt.Report(report, self.name, 'domain_report.txt', '网站子域名挖掘报告已存放于', '保存出错').save()
        return

    def saveIpResult(self, report_dict):
        '''
        保存子域名IP分布情况
        :param report_dict:
        :return:
        '''
        if report_dict == {}:
            return
        if self.showIP:   # 是否需要输出
            print()
            print(self.Output.blue('[ schedule ] ') + self.Output.fuchsia('IP分布情况'))
        ip_result = [str(x) + " : " + str(y) for x, y in report_dict.items()]
        if self.saveType == 'xlsx':
            banner = ['子域名IP', '分布数量']
            reports_xlsx.Report(ip_result, self.name, 'subDomain_IP', banner).save()
        else:
            reports_txt.Report(ip_result, self.name, 'IP_collect_report.txt', '网站子域名IP分布报告已存放于', '保存出错').save()
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
        if n[-2] not in ["com", "edu", "ac", "net", "org", "gov"]:   # 带地域标签的域名
            domain = "{0}.{1}".format(n[-2], n[-1])
        else:
            domain = "{0}.{1}.{2}".format(n[-3], n[-2], n[-1])
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
            res = self.REQ.autoGetAccess(url, threads=self.threads, timeout=self.timeout)
            pagenum = rePage.findall(res.text)[0]
            pagenum = int(pagenum)
        except:
            print(self.Output.yellow('[ warn ] ') + self.Output.cyan('站长之家api没有获取数据'))
            return []
        domain = re.compile('[\w]+\.{}'.format(self.domain))  # 正则提取子域名
        for i in range(1, pagenum+1):
            url = "https://tool.chinaz.com/subdomain/?domain={}&page={}".format(self.domain, str(i))
            res = self.REQ.autoGetAccess(url, threads=self.threads, timeout=self.timeout)
            try:
                domains = domain.finditer(res.text)
                if domains == []:
                    break
                for d in domains:
                    if d.group() not in report:
                        report.append(d.group())
            except:
                pass
        return report


    def load_payload(self, report):
        '''
        读取payload
        数据合并并去重
        :param report: 在线子域名数据
        :return:
        '''
        if self.payload:  # 已设置好payload
            return self.payload
        payload = []
        path = os.path.dirname(__file__)
        file = 'dict.txt'
        filepath = "{0}/{1}/{2}".format(path, r'../dict/domain', file)
        F = open(filepath, 'r')
        for x in F:
            url = '{}.{}'.format(x.replace('\n', ''), self.domain)
            payload.append(url)
        payload += report
        payload = list(set(payload))   # payload去重
        # print(payload)
        return payload

    def run(self, payload):
        '''
        调用异步请求
        :param payload:导入的payload
        :return:
        '''
        URL = ['http://'+u for u in payload]  # 需要添加协议头
        handler = subdomainTerminal.Terminal(scanmode=self.scanmode, isShow=self.isShow)  # 申请文本处理起
        REQ = asyncHttp.req(
            handler=handler,
            workers=self.threads,
            timeout=self.timeout
        )  # 申请异步
        if self.isThread:   # 多线程异步
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(REQ.run(URL))
        results = REQ.results   # 获取结果
        self.IP_list = handler.IP_list   # 获取IP结果
        return results


    # def getDomainType(self, url):
    #     '''
    #     获取域名解析记录类型
    #     :param url:
    #     :return:
    #     '''
    #     domain = str(url).replace('http://', '').replace('https://', '').split('/')[0]
    #     ans = dns.resolver(domain)
    #     res = ans.response.answer
    #     res_type = str(type(res[0][0])).split('.')[3]
    #     return res_type


    def panAnalysis(self, domain):
        '''
        以随机数拼接域名判断是否会存在泛解析
        :param domain:
        :return:
        '''
        ranstr = hashlib.md5(domain.encode()).hexdigest()
        ranstr1 = ranstr[:4]
        ranstr2 = ranstr[-4:]
        url1 = "{}.{}".format(ranstr1, domain)
        url2 = "{}.{}".format(ranstr2, domain)
        if self.isShow:
            print(self.Output.blue('[ checking ] ') + self.Output.fuchsia('是否存在泛解析'))
        res = self.run([url1, url2])
        if len(res) == 2:   # 泛解析
            self.scanmode = 1  # 修改判断逻辑
            if self.isShow:
                print(self.Output.yellow('[ warn ] ') + self.Output.red("{} 存在泛解析 ".format(self.domain)))
                print(self.Output.yellow('[ warn ] ') + self.Output.cyan('程序将使用差异化进行判断，但结果准确性可能下降'))
        return

    def rapidSearch(self, domain):
        '''
        根据最大最全的repiddns.io平台进行在线搜索，但网速可能会比较慢
        :param domain:
        :return:
        '''
        url = f'https://rapiddns.io/subdomain/{domain}?full=1&down=1'
        if self.isThread:
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.rapidDns(url))
        result = loop.run_until_complete(task)
        return result

    async def rapidDns(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as res:
                    text = await res.read()
                    ret_dict = await self.resultParse(text)  # 获取页面解析数据
                    if ret_dict != []:
                        if self.isShow:
                            print(self.Output.blue('[ Load ] ') + self.Output.cyan('获取数据成功，即将开始存活性筛选'))
                        return ret_dict
        except Exception as e:
            print(e)
        return []

    async def resultParse(self, text):
        '''
        解析网页内容，筛选符合条件的数据
        :param text:
        :return:
        '''
        Urls = []
        cname_list = []
        soup = BeautifulSoup(text, 'html.parser')
        td_links = soup.find_all('tr')

        for d in td_links:
            a = d.get_text()
            a = a.strip()
            m = a.split('\n')
            if m[-2] in ['CNAME', 'A', 'AAAA'] and m[2] not in cname_list:  # 目前只嗅探3种类型的DNS记录
                if m[-2] in ['CNAME'] and m[2] not in cname_list:
                    cname_list.append(m[2])     # 收集被指向子域名，过多重复可不再重复收录
                Urls.append(m[1])
        return Urls

    def insertSubDomainData(self, data, tasknameid=''):
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
            d['subdomain'] = yarl.URL(d['url']).host
            pgsql.insert(DomainModel, data=d)
        return


class celery_domain:
    def __init__(self, url, payload, name):
        self.url = url
        self.payload = payload
        self.name = name

    def run(self):
        x = Domain(self.url, self.payload, self.name, False).start()
        return
