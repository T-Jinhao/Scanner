#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import sys
import re
import os
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin
from .color_output import color_output

wrong_web_list = ['javascript:void(0)',None,'###','#']

class Spider():
    def __init__(self, url, REQ, crazy):
        self.url = url
        self.REQ = REQ
        self.crazy = crazy
        self.Phone = []
        self.Email = []

    def start(self):
        color_output(">>>>>spider" + "-" * 40)
        color_output("[ 开始爬取网页链接：{}]".format(self.url), color='BLUE')
        img, web, js = self.spider(self.url)
        if img:
            self.spider_report(self.url, img, 'img')
        else:
            color_output("[ 并没有在{}扫描到图片链接 ]".format(self.url), color='YELLOW')
        if web:
            if self.crazy:  # url分解访问
                web += self.crazyRun(web)
            ret = self.statusCheck(web)   # 筛选能访问的链接
            self.spider_report(self.url, ret, 'web')
        else:
            color_output("[ 并没有在{}扫描到网站链接 ]".format(self.url), color='YELLOW')
        if js and self.crazy:    # 寻找js文件内的中文字符
            color_output('-'*10 + 'js文件分析' + '-'*10, color='BLUE')
            for x in js:
                color_output(x)    # js链接
                color_output(self.find_CN(x), color='GREEN')    # 正则js文件中的中文
        if self.Phone != []:
            color_output('手机号码', color='MAGENTA')
            for x in self.Phone:
                color_output(x, color='GREEN')
        if self.Email != []:
            color_output('邮箱', color='MAGENTA')
            for x in self.Email:
                color_output(x, color='GREEN')
        color_output("-" * 40 + "<<<<<spider" + "\n")
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
        color_output(paths)
        return paths


    def url_check(self, url, u):
        '''
        检测url完整性，返回绝对地址
        :param url: 当前扫描的页面url
        :param u: 获取到的url
        :return:
        '''
        if re.match("(http|https)://.*",u):  # 匹配绝对地址
            return u
        else:     # 拼凑相对地址，转换成绝对地址
            u = urljoin(url, u)
            return u


    def spider(self,url):
        '''
        爬取当前页面的URL
        :return:网站相关链接
        '''
        try:
            res = self.REQ.autoAccess(url)
            self.find_Email(res.text)   # 匹配邮箱
            self.find_Phone(res.text)   # 匹配电话
            img_sites = []      # 图片链接
            web_sites = []      # 网站链接
            js_sites = []        # js脚本链接
            soup = BeautifulSoup(res.text,'html.parser')
            img_links = soup.find_all('img')
            web_links = soup.find_all('a')
            js_links = soup.find_all('script')
            for i in img_links:
                x = i.get('src')           # 提取src后的链接
                img_sites.append(self.url_check(url, x))
            for j in web_links:
                y = j.get('href')          # 提取href后的链接
                if y not in wrong_web_list:  # 除去杂乱的链接
                    web_sites.append(self.url_check(url, y))   # 处理获取到的url
            for k in js_links:
                z = k.get('src')
                if z != None:
                    js_sites.append(self.url_check(url, z))
            if not img_sites:
                img_sites = ''
            if not web_sites:
                web_sites = ''
            if not js_sites:
                js_sites = ''
            return img_sites,web_sites,js_sites

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
                res = self.REQ.httpAccess(url)
                color_output("状态码：{}  文本长度：{}".format(res.status_code, len(res.content)), color='GREEN')
                if res.status_code != 404 and len(res.content) != 0:
                    Gurls.append(url)
            except:
                color_output('访问失败', color='YELLOW')
            time.sleep(0.5)   # 防止过于频繁导致网站崩溃
        return Gurls

    def find_CN(self, url):
        '''
        找出js文件内的中文字符
        :return:
        '''
        compile_CN = re.compile(u"[\u4e00-\u9fa5]")   # 匹配中文
        try:
            res = self.REQ.httpAccess(url)
            content = str(res.content.decode('utf-8'))
            self.find_Phone(res.text)
            self.find_Email(res.text)
            ret = compile_CN.findall(content)
            ret = ''.join(ret)
        except:
            return
        return ret

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

    def spider_report(self,url,report,flag):
        '''
        对爬取结果进行处理
        :return:
        '''
        path = os.path.dirname(__file__)
        parse_url = urlparse(url)
        dirname = parse_url.netloc
        dirpath = "{0}/{1}/{2}".format(path,"../reports",dirname)
        filepath = "{0}/{1}".format(dirpath,"spider_{}_report.txt".format(flag))
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        F = open(filepath,"a")
        try:
            for m in report:
                color_output(m)
                F.write(m+"\n")
            color_output("[ 网站{1}链接已保存于：{0}]".format(filepath,flag), color='MAGENTA')
        except:
            color_output("[ 并没有扫描到{}链接 ]".format(flag), color='YELLOW')
        F.close()
        return

class celery_spider:
    '''
    celery调用模块
    返回新的url进行递归扫描
    '''
    def __init__(self,url,REQ):
        self.url =url
        self.REQ = REQ

    def run(self):
        res = Spider(self.url, self.REQ, '1')
        new_url = self.same_check(res)
        return new_url

    def same_check(self,res):
        '''
        url相似度的检测
        :param res:爬取的url集
        :return: 同源的url
        '''
        return res
