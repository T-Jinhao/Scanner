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
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from reports import reports
from concurrent.futures import ThreadPoolExecutor
from .color_output import color_output

class Domain:
    def __init__(self, url, payload, REQ, name, flag):
        self.domain = self.url_check(url)
        self.payload = payload
        self.REQ = REQ
        self.flag = flag
        self.name = name
        self.url = url

    def start(self):
        color_output('>>>>>domain' + '-' * 40)
        report = []
        if self.domain:
            color_output("当前域名 {} 是否正确解析？[正确则回车，否则输入正确的域名]".format(self.domain), color='MAGENTA')
            checkin = input()
            if checkin:
                self.domain = checkin
            pan = self.panAnalysis(self.domain)   # 检测是否存在泛解析
            if pan:    # 泛解析处理块
                color_output("[{} 存在泛解析，任意键继续，直接回车将退出执行]".format(self.domain), color='YELLOW')
                select = input()
                if select != '':
                    color_output('程序继续执行，但结果准确性可能下降', color='CYAN')
                else:
                    color_output('程序终止', color='CYAN')
                    color_output('-' * 40 + 'domain<<<<<' + '\n')
                    return

            color_output("[ 开始爆破域名: {} ]".format(self.domain), color='BLUE')
            if self.flag:           # 调用rapiddns.io进行在线获取
                color_output('正在运行在线查询，请耐心等待；该过程请挂载代理，否则可能会访问超时，导致获取数据失败', color='CYAN')
                self.rapidSearch(self.domain)
                report = self.RAPID
                if report == []:
                    color_output('-X模式查询失败，稍后将继续执行', color='YELLOW')
                    time.sleep(3)

            if report == []:    # 普通模式及rapid获取数据失败的情况下，使用字典爆破
                onlineReport = self.chinaz_search()  # chinaz在线查询接口获得的数据
                payload = self.load_payload(onlineReport)  # 合并数据
                if payload:
                    color_output('[ payload导入完成 ]', color='MAGENTA')
                    report = self.run(self.domain, payload)
                else:
                    color_output('[ payload导入失败 ]', color='RED')
            if report:
                reports.Report(report, self.name, 'domain_report.txt', '网站子域名挖掘报告已存放于', '未能挖掘出网站子域名').save()
            else:
                color_output("[ 未能挖掘出网站子域名 ]", color='YELLOW')
        else:
            color_output("[ {}不支持子域名挖掘 ]".format(self.url), color='YELLOW')
        color_output('-' * 40 + 'domain<<<<<' + '\n')
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
        domain = "{0}.{1}".format(n[-2],n[-1])     # 域名切割，但会误报三级域名等
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
            res = self.REQ.autoGetAccess(url)
            pagenum = rePage.findall(res.text)[0]
            pagenum = int(pagenum)
        except:
            color_output('站长之家api没有获取数据', color='YELLOW')
            return []

        for i in range(1, pagenum+1):
            url = "https://tool.chinaz.com/subdomain/?domain={}&page={}".format(self.domain, i)
            res = self.REQ.autoGetAccess(url)
            domain = re.compile('[\w]+\.{}'.format(self.domain))    # 正则提取子域名
            domains = domain.finditer(res.text)
            if domains == []:
                break
            for d in domains:
                if d.group() not in report:
                    # color_output(d.group(), color='GREEN')  # 未知是否存活，不输出
                    report.append(d.group())
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

    def run(self,domain,payload):
        '''
        配置线程池
        :param domain:提取到的域名
        :param payload:导入的payload
        :return:
        '''
        URL = []
        url_list = []
        report = []
        for u in payload:
            URL.append(u)

        resp = self.REQ.mGetAsyncAccess(URL)
        for r in resp:
            try:
                if r.url not in url_list:
                    url_list.append(r.url)
                    msg = "当前状态码：{0} | 跳转记录：{1} | 最终URL：{2} ".format(
                        r.status_code,
                        r.history,
                        r.url
                    )
                    color_output(msg, color='GREEN')
                    report.append(msg)
            except:
                pass
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
        self.RAPID = []
        url = f'https://rapiddns.io/subdomain/{domain}?full=1&down=1'
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.rapidDns(url))
        loop.run_until_complete(task)

    async def rapidDns(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as res:
                    text = await res.read()
                    ret_dict = await self.resultParse(text)  # 获取页面解析数据
        except Exception as e:
            print(e)
        if ret_dict != []:
            color_output('获取数据成功，即将开始存活性筛选', color='CYAN')
            self.multiScan(ret_dict)
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
                    continue
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
        res = self.REQ.mGetAsyncAccess(url_dict)   # 获取访问结果
        i = -1   # 下标
        for r in res:
            i += 1
            if r == None:
                continue
            if r.status_code == 200 or r.status_code == 302 or r.status_code == 500 or r.status_code == 502:
                msg = "{status_code} : {content_length} : {url}".format(
                    status_code=r.status_code,
                    url=r.url,
                    content_length=len(r.content)
                )
                # m = ret_dict[i]
                # if m['Domain'] == m['Address']:
                #     msg = "{0} : {1} : {2} : {3}".format(r.status_code, m['Type'], m['Domain'], r.url)
                # elif m['Type'] in ['A', 'AAAA']:
                #     msg = "{0} : {1} : {2} ==> {3} : {4}".format(r.status_code, m['Type'], m['Domain'], m['Address'], r.url)
                # else:
                #     msg = "{0} : {1} : {2} ==> {3} ==> {4} : {5}".format(r.status_code, m['Type'], m['Domain'], m['Address'],
                #                                                    self.getHostname(m['Address']), r.url)
                color_output(msg, color='GREEN')
                self.RAPID.append(msg)
        return

    def getHostname(self, host):
        IP = ''
        try:
            IP = socket.gethostbyname(host)
        except:
            pass
        return IP


    def scan(self,url):
        '''
        开始扫描
        :param url:
        :return:
        '''
        try:
            res = self.REQ.autoGetAccess(url)   # 高并发，单独创建对象
            if res.status_code == 200 or res.status_code == 302 or res.status_code == 500 or res.status_code == 502:
                res_type = self.getDomainType(url)
                msg = "{0} : {1} : {2}".format(res.status_code, res_type, url)
                m = {'msg': msg, 'flag': 1}
                return m
        except:
            msg = "[Timeout : {}]".format(url)
            m = {'msg': msg, 'flag': 2}
            return m
        m = {'flag' : 0}
        return m

class celery_domain:
    def __init__(self,url,payload,REQ,name):
        self.url = url
        self.payload = payload
        self.REQ = REQ
        self.name = name

    def run(self):
        x = Domain(self.url, self.payload, self.REQ, self.name, False).start()
        return
