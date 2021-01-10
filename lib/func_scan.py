#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import sys
import re
import os
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .color_output import color_output,color_list_output

wrong_web_list = ['javascript:void(0)',None,'###','#']

class Scan():
    def __init__(self, url, REQ, name, crazy):
        self.url = url
        self.REQ = REQ
        self.name = name
        self.crazy = crazy
        self.Phone = []
        self.Email = []

    def start(self):
        color_output(">>>>>scan" + "-" * 40)
        color_output("[ 开始爬取网页链接：{}]".format(self.url), color='BLUE')
        web, js = self.scan(self.url)
        if web:
            if self.crazy:  # url分解访问
                web += self.crazyRun(web)
            ret = self.statusCheck(web)   # 筛选能访问的链接
            self.scan_report(ret, 'web')
        else:
            color_output("[ 并没有在{}扫描到网站链接 ]".format(self.url), color='YELLOW')
        if js and self.crazy:    # 寻找js文件内的中文字符
            color_output('-'*10 + 'js文件分析' + '-'*10, color='MAGENTA')
            for u in js:
                self.find_Disclose(u)    # 寻找敏感信息

        if self.Phone != []:
            color_output('手机号码', color='MAGENTA')
            color_list_output(self.Phone, color='GREEN')
        if self.Email != []:
            color_output('邮箱', color='MAGENTA')
            color_list_output(self.Email, color='GREEN')
        color_output("-" * 40 + "<<<<<scan" + "\n")
        return


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
        # color_output(paths)
        return paths


    def url_check(self, url, u):
        '''
        检测url完整性，返回绝对地址
        :param url: 当前扫描的页面url
        :param u: 获取到的url
        :return:
        '''
        err = ['', None, '/', '\n']
        if u in err:
            return
        if re.match("(http|https)://.*", u):  # 匹配绝对地址
            return u
        else:     # 拼凑相对地址，转换成绝对地址
            u = urljoin(url, u)
            return u


    def scan(self, url):
        '''
        爬取当前页面的URL
        :return:网站相关链接
        '''
        try:
            res = self.REQ.autoGetAccess(url)
            self.find_Email(res.text)   # 匹配邮箱
            self.find_Phone(res.text)   # 匹配电话
            web_sites = []  # 网站链接
            js_sites = []  # js脚本链接
            soup = BeautifulSoup(res.text, 'html.parser')
            web_links = soup.find_all('a')
            js_links = soup.find_all('script')
            for j in web_links:
                y = j.get('href')  # 提取href后的链接
                if y != None and y not in wrong_web_list:
                    u = self.url_check(url, y)
                    if u != None:
                        web_sites.append(u)  # 处理获取到的url
            for k in js_links:
                z = k.get('src')
                if z != None:
                    u = self.url_check(url, z)
                    if u != None:
                        js_sites.append(u)
            if not web_sites:
                web_sites = ''
            if not js_sites:
                js_sites = ''
            return web_sites, js_sites

        except Exception as e:
            color_output(e, color='RED')
            color_output("网站访问出现点问题了...", color='RED')
            sys.exit(1)



    def statusCheck(self,urls):
        '''
        测试链接是否可用
        :param urls: 爬取到的url
        :return:
        '''
        Gurls = []
        for url in list(set(urls)):
            color_output('测试链接：{0}'.format(url), color='CYAN')
            try:
                res = self.REQ.autoGetAccess(url)
                color_output("状态码：{}  文本长度：{}".format(res.status_code, len(res.content)), color='GREEN')
                if res.status_code != 404 and len(res.content) != 0:
                    Gurls.append(url)
            except:
                color_output('访问失败', color='YELLOW')
            time.sleep(0.5)   # 防止过于频繁导致网站崩溃
        return Gurls

    def find_Disclose(self, url):
        '''
        找出js文件内的中文字符
        :return:
        '''
        compile_CN = re.compile(u"[\u4e00-\u9fa5]")   # 匹配中文
        color_output('爬取链接：' + url, color='CYAN')
        try:
            res = self.REQ.autoGetAccess(url)
            content = str(res.content.decode('utf-8'))
            self.find_Phone(res.text)
            self.find_Email(res.text)
            self.reg_str(res.text)
            ret = compile_CN.findall(content)
            if ret != []:
                color_output('文件中文爬取：', color="MAGENTA")
                ret = ''.join(ret)
                color_output(ret, color='GREEN')
        except Exception:
            pass
        return

    def find_Phone(self, text):
        '''
        匹配手机号码
        :param text:
        :return:
        '''
        compile_Phone = re.compile(r'1[3456789]\d{9}')
        ret = compile_Phone.findall(text)
        if ret != []:
            for x in ret:
                if x not in self.Phone:
                    self.Phone.append(x)
        return

    def find_Email(self, text):
        '''
        匹配邮箱
        :param content:
        :return:
        '''
        compile_Email = re.compile(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]{0,4}')
        ret = compile_Email.findall(text)
        if ret != []:
            for x in ret:
                if x not in self.Email and x.split('.')[-1] != 'png':
                    self.Email.append(x)
        return

    def reg_str(self, text):
        '''
        匹配js中的链接
        感谢：https://github.com/GerbenJavado/LinkFinder
        :param text: 页面
        :return:
        '''
        resultUrls = []
        regex_str = r"""
                      (?:"|')                               # Start newline delimiter
                      (
                        ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
                        [^"'/]{1,}\.                        # Match a domainname (any character + dot)
                        [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path
                        |
                        ((?:/|\.\./|\./)                    # Start with /,../,./
                        [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
                        [^"'><,;|()]{1,})                   # Rest of the characters can't be
                        |
                        ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
                        [a-zA-Z0-9_\-/]{1,}                 # Resource name
                        \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
                        (?:[\?|/][^"|']{0,}|))              # ? mark with parameters
                        |
                        ([a-zA-Z0-9_\-]{1,}                 # filename
                        \.(?:php|asp|aspx|jsp|json|
                             action|html|js|txt|xml)             # . + extension
                        (?:\?[^"|']{0,}|))                  # ? mark with parameters
                      )
                      (?:"|')                               # End newline delimiter
                    """
        compile_str = re.compile(regex_str, re.VERBOSE)
        ret = compile_str.findall(text)
        if ret != []:
            color_output('JS链接爬取结果：', color="MAGENTA")
            for x in ret:
                for m in x:
                    u = self.url_check(self.url, m)
                    if u not in resultUrls and u:
                        resultUrls.append(u)
            color_list_output(resultUrls, color='GREEN')

    def scan_report(self, report, flag):
        '''
        对爬取结果进行处理
        :return:
        '''
        path = os.path.dirname(__file__)
        dirpath = "{0}/{1}/{2}".format(path,"../reports", self.name)
        filepath = "{0}/{1}".format(dirpath,"scan_{}_report.txt".format(flag))
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        F = open(filepath, "a")
        try:
            for m in report:
                F.write(m+"\n")
            color_output("[ 网站{1}链接已保存于：{0}]".format(filepath,flag), color='MAGENTA')
        except:
            color_output("[ 并没有扫描到{}链接 ]".format(flag), color='YELLOW')
        F.close()
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
