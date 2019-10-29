#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import requests,sys
import re,os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor


class Spider():
    def __init__(self,url,cookies,threads,flag):
        self.url = url
        self.flag = flag
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        self.cookies = cookies
        self.start()


    def start(self):
        print(">>>>>spider" + "-" * 40)
        print("[ 开始爬取网页链接：{}]".format(self.url))
        img, web = self.spider(self.url)
        if img:
            self.spider_report(self.url, img, 'img')
        else:
            print("[ 并没有在{}扫描到图片链接 ]".format(self.url))
        if web:
            self.spider_report(self.url, web, 'web')
        else:
            print("[ 并没有在{}扫描到网站链接 ]".format(self.url))
        print("-" * 40 + "<<<<<spider" + "\n")
        while self.flag:
            with ThreadPoolExecutor(max_workers=5) as pool:
                results = pool.map(self.crazy,web)
                for result in results:
                    print(result)
            self.flag = 0
        return


    def crazy(self,url):
        '''
        crazy模式
        :param url:
        :return:
        '''
        url = self.url_check(url)        # 规范化url
        img,web = self.spider(url)
        self.spider_report(url,img,web)
        self.flag = 0  # 调用一次即停止
        return


    def url_check(self,url):
        '''
        检测url完整性
        :param url:
        :return:
        '''
        if re.match("(http|https)://.*",url):
            return url
        else:
            u = "http://{}".format(url)
            return u


    def spider(self,url):
        '''
        爬取当前页面的URL
        :return:网站相关链接
        '''
        try:
            res = requests.post(url,headers=self.headers,cookies=self.cookies,timeout=10)
            img_sites = []      # 图片链接
            web_sites = []      # 网站链接
            soup = BeautifulSoup(res.text,'html.parser')
            img_links = soup.find_all('img')
            web_links = soup.find_all('a')
            for i in img_links:
                x = i.get('src')           # 提取src后的链接
                img_sites.append(x)
            for j in web_links:
                y = j.get('href')          # 提取href后的链接
                web_sites.append(y)
            if not img_sites:
                img_sites = ''
            if not web_sites:
                web_sites = ''
            return img_sites,web_sites

        except:
            print("网站访问出现点问题了...")
            sys.exit(1)


    def spider_report(self,url,report,flag):
        '''
        对爬取结果进行处理
        :return:
        '''
        path = os.path.abspath(os.path.dirname(__file__))
        parse_url = urlparse(url)
        dirname = parse_url.netloc
        dirpath = "{0}\{1}\{2}".format(path,"reports",dirname)
        filepath = "{0}\{1}".format(dirpath,"spider_{}_report.txt".format(flag))
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        F = open(filepath,"a")
        try:
            for m in report:
                print(m)
                F.write(m+"\n")
            print("[ 网站{1}链接已保存于：{0}]".format(filepath,flag))
        except:
            print("[ 并没有扫描到{}链接 ]".format(flag))
        F.close()
        # self.flag = 0
        return
