#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import os
import re
import hashlib
import dns.resolver
import aiohttp
import asyncio
import socket
import time
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from reports import reports_txt,reports_xlsx
from concurrent.futures import ThreadPoolExecutor
from .color_output import *
from .load_config import Config
from modules import util

class Domain:
    def __init__(self, url, payload, REQ, name, flag):
        self.check = False
        self.domain = self.url_check(url)
        self.payload = payload
        self.REQ = REQ
        self.flag = flag
        self.name = name
        self.url = url
        self.Domain_List = []
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


    def start(self):
        self.load_config()
        print(self.Output.fuchsia('>>>>>domain' + '-' * 40))
        report = []
        if self.domain:
            if self.check == False:
                print(self.Output.fuchsia('[ checkin ] ') + self.Output.red("当前域名") + self.Output.yellow(self.domain) + self.Output.red("是否正确解析？[正确则回车，否则输入正确的域名]"))
                checkin = input()
                if checkin:
                    self.domain = checkin
            pan = self.panAnalysis(self.domain)   # 检测是否存在泛解析
            if pan:    # 泛解析处理块
                print(self.Output.yellow('[ warn ] ') + self.Output.red("{} 存在泛解析 ".format(self.domain)) + self.Output.fuchsia("[输入任意值继续，直接回车将退出执行]"))
                select = input()
                if select != '':
                    print(self.Output.yellow('[ warn ] ') + self.Output.cyan('程序继续执行，但结果准确性可能下降'))
                else:
                    print(self.Output.blue('[ schedule ] ') + self.Output.red('程序终止'))
                    print(self.Output.fuchsia('-' * 40 + 'domain<<<<<' + '\n'))
                    return
            print(self.Output.blue('[ schedule ] ') + self.Output.fuchsia('开始爆破域名:') + self.Output.green(self.domain))
            if self.flag:           # 调用rapiddns.io进行在线获取
                print(self.Output.blue('[ schedule ] ') + self.Output.cyan('正在运行在线查询，请耐心等待'))
                print(self.Output.yellow('[ warn ] ') + self.Output.fuchsia('该过程请挂载代理，否则可能会访问超时，导致获取数据失败'))
                self.rapidSearch(self.domain)
                report = self.RAPID   # 该模块结果
                if report == []:
                    print(self.Output.yellow('[ warn ] ') + self.Output.fuchsia('-X模式查询失败，稍后将执行payload爆破'))
                    time.sleep(3)

            if report == []:    # 普通模式及rapid获取数据失败的情况下，使用字典爆破
                self.flag = False   # 更改为普通模式，用作保存时区别
                onlineReport = self.chinaz_search()  # chinaz在线查询接口获得的数据
                payload = self.load_payload(onlineReport)  # 合并数据
                if payload:
                    print(self.Output.blue('[ Load ] ') + self.Output.green('payload导入完成，数量：{}'.format(len(payload))))
                    report = self.run(payload)
                else:
                    print(self.Output.blue('[ Load ] ') + self.Output.red('payload导入失败'))
            self.saveDomainResult(report)
            if report:
                IP_dict = self.collectIP()
                self.saveIpResult(IP_dict)
            elif report == []:
                print(self.Output.blue('[ result ] ') + self.Output.yellow('[ 未能挖掘出网站子域名 ]'))
        else:
            print(self.Output.yellow('[ warn ] ') + self.Output.cyan("[ {}不支持子域名挖掘 ]".format(self.url)))
        print(self.Output.fuchsia('-' * 40 + 'domain<<<<<' + '\n'))
        return

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
            if self.flag:    # 修改banner等信息
                banner = ['状态码', '域名解析类型', '标题', '跳转记录', '最终URL']
                sheetname = 'subDomain-X'
                cut = ' : '
            else:       # 普通格式
                banner = ['状态码', '跳转记录', '标题', '最终URL']
                sheetname = 'subDomain'
                cut = ' | '
            reports_xlsx.Report(report, self.name, sheetname, banner, cut=cut).save()
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
        if len(n) == 2:      # 检测域名是否自动合理切割
            self.check = True
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
                        # color_output(d.group(), color='GREEN')  # 未知是否存活，不输出
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
        payload = []
        path = os.path.dirname(__file__)
        if self.payload:   # 已设置好payload
            return self.payload

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

    def run(self,payload):
        '''
        配置线程池
        :param payload:导入的payload
        :return:
        '''
        URL = [u for u in payload]
        url_list = []
        report = []
        resp = self.REQ.mGetAsyncAccess(URL, threads=self.threads, timeout=self.timeout)
        for r in resp:
            if r == None:
                continue
            try:
                if r.url not in url_list and r.status_code in self.chkStatus:
                    url_list.append(r.url)
                    title = util.getTitle(r.text)
                    self.addToList(r.url)
                    msg = "{status} | {history} | {title} | {url} ".format(
                        status=r.status_code,
                        history=r.history,
                        title=title,
                        url=r.url
                    )
                    output = "".join([
                        self.Output.green('[ result ] '), self.Output.fuchsia('status_code:'),
                        self.Output.green(r.status_code), self.Output.interval(),
                        self.Output.fuchsia('最终URL:'), r.url, self.Output.interval(),
                        self.Output.fuchsia('标题:'), self.Output.green(title), self.Output.interval(),
                        self.Output.fuchsia('跳转记录:'), self.Output.green(r.history), self.Output.interval()
                    ])
                    print(output)
                    sys.stdout.flush()
                    report.append(msg)
            except Exception as e:
                print(e)
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
        以随机数拼接域名判断是否会存在泛解析
        :param domain:
        :return:
        '''
        ranstr = hashlib.md5(domain.encode()).hexdigest()
        ranstr1 = ranstr[:4]
        ranstr2 = ranstr[-4:]
        url1 = "http://{}.{}".format(ranstr1, domain)
        url2 = "http://{}.{}".format(ranstr2, domain)
        res1 = self.REQ.autoGetAccess(url1)
        res2 = self.REQ.autoGetAccess(url2)
        if res1 == None and res2 == None:    # grequests没有抛异常，出错返回None
            return False
        return True

    def rapidSearch(self, domain):
        '''
        根据最大最全的repiddns.io平台进行在线搜索，但网速可能会比较慢
        :param domain:
        :return:
        '''
        url = f'https://rapiddns.io/subdomain/{domain}?full=1&down=1'
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.rapidDns(url))
        loop.run_until_complete(task)

    async def rapidDns(self, url):
        self.RAPID = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as res:
                    text = await res.read()
                    ret_dict = await self.resultParse(text)  # 获取页面解析数据
                    if ret_dict != []:
                        print(self.Output.blue('[ Load ] ') + self.Output.cyan('获取数据成功，即将开始存活性筛选'))
                        self.multiScan(ret_dict)
        except Exception as e:
            print(e)
        return

    async def resultParse(self, text):
        '''
        解析网页内容，筛选符合条件的数据
        :param text:
        :return:
        '''
        ret_dict = []
        cname_list = []
        soup = BeautifulSoup(text, 'html.parser')
        td_links = soup.find_all('tr')

        for d in td_links:
            a = d.get_text()
            a = a.strip()
            m = a.split('\n')
            if m[-1] in ['CNAME', 'A', 'AAAA'] and m[2] not in cname_list:  # 目前只嗅探3种类型的DNS记录
                if m[-1] in ['CNAME'] and m[2] not in cname_list:
                    cname_list.append(m[2])     # 收集被指向子域名，过多重复可不再重复收录
                ret = {
                    '#': m[0],
                    'Domain': m[1],
                    'Address': m[2],
                    'Type': m[-1]
                }
                ret_dict.append(ret.copy())
        return ret_dict

    def multiScan(self, ret_dict):
        '''
        处理字典中的数据
        :param ret_dict:
        :return:
        '''
        url_dict = [m['Domain'] for m in ret_dict]
        res = self.REQ.mGetAsyncAccess(url_dict, threads=self.threads, timeout=self.timeout)   # 获取访问结果
        i = -1   # 下标
        for r in res:
            i += 1
            if r == None:
                continue
            if r.status_code in self.chkStatus:
                m = ret_dict[i]
                title = util.getTitle(r.text)
                self.addToList(r.url)
                if m['Domain'] == m['Address']:
                    msg = "{status} : {Type} : {title} : {Domain} : {url}".format(
                        status=r.status_code,
                        Type=m['Type'],
                        title=title,
                        Domain=m['Domain'],
                        url=r.url
                    )
                    output = "".join([
                        self.Output.green('[ result ] ')
                        , self.Output.fuchsia('status_code:'), self.Output.green(
                            r.status_code), self.Output.interval()
                        , self.Output.fuchsia('URL:'), r.url, self.Output.interval()
                        , self.Output.fuchsia('Type:'), self.Output.green(m['Type']), self.Output.interval()
                        , self.Output.fuchsia('Title:'), self.Output.green(title), self.Output.interval()
                        , self.Output.fuchsia('Domain'), self.Output.green(m['Domain'])
                    ])
                    print(output)
                    sys.stdout.flush()
                elif m['Type'] in ['A', 'AAAA']:
                    msg = "{status} : {Type} : {title} : {Domain} ==> {Address} : {url}".format(
                        status=r.status_code,
                        Type=m['Type'],
                        title=title,
                        Domain=m['Domain'],
                        Address=m['Address'],
                        url=r.url
                    )
                    output = "".join([
                        self.Output.green('[ result ] ')
                        , self.Output.fuchsia('status_code:'), self.Output.green(
                            r.status_code), self.Output.interval()
                        , self.Output.fuchsia('URL:'), r.url, self.Output.interval()
                        , self.Output.fuchsia('Type:'), self.Output.green(m['Type']), self.Output.interval()
                        , self.Output.fuchsia('Title:'), self.Output.green(title), self.Output.interval()
                        , self.Output.green(m['Domain']), self.Output.white('==>'), self.Output.green(m['Address'])
                    ])
                    print(output)
                    sys.stdout.flush()
                else:
                    hostname = util.getHostname(m['Address'])
                    msg = "{status} : {Type} : {title} :{Domain} ==> {Address} ==> {hostname} : {url}".format(
                        status=r.status_code,
                        Type=m['Type'],
                        title=title,
                        Domain=m['Domain'],
                        Address=m['Address'],
                        hostname=hostname,
                        url=r.url
                    )
                    output = "".join([
                        self.Output.green('[ result ] ')
                        , self.Output.fuchsia('status_code:'), self.Output.green(r.status_code), self.Output.interval()
                        , self.Output.fuchsia('URL:'), r.url, self.Output.interval()
                        , self.Output.fuchsia('Type:'), self.Output.green(m['Type']), self.Output.interval()
                        , self.Output.fuchsia('Title:'), self.Output.green(title), self.Output.interval()
                        , self.Output.green(m['Domain']), self.Output.white('==>'), self.Output.green(m['Address'])
                        , self.Output.white('==>'), self.Output.green(hostname)])
                    print(output)
                    sys.stdout.flush()
                self.RAPID.append(msg)
        return

    def collectIP(self):
        '''
        收集IP
        :param url:
        :return:
        '''
        IP_dict = {}
        # print(self.Domain_List)
        if self.Domain_List == []:
            return
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            results = pool.map(socket.gethostbyname, self.Domain_List)
            for i in results:
                if i not in IP_dict.keys():
                    IP_dict[i] = 1
                else:
                    IP_dict[i] += 1
        return IP_dict



    def addToList(self, url):
        '''
        存储子域名
        :param url:
        :return:
        '''
        if not self.domain2IP:
            return
        try:
            domain = urlparse(url).hostname
            if domain not in self.Domain_List:
                self.Domain_List.append(domain)
        except:
            pass
        return


class celery_domain:
    def __init__(self,url,payload,REQ,name):
        self.url = url
        self.payload = payload
        self.REQ = REQ
        self.name = name

    def run(self):
        x = Domain(self.url, self.payload, self.REQ, self.name, False).start()
        return
