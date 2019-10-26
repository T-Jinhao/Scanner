#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import requests,sys
import re,os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import threading
from concurrent.futures import ThreadPoolExecutor


class Spider():
    def __init__(self,url,cookies,threads,flag):
        self.url = url
        self.flag = flag
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        self.cookies = cookies
        print(">>>>>spider" + "-" * 40)
        print("[ 开始爬取网页链接：{}]".format(url))
        img,web = self.spider(self.url)
        self.spider_report(self.url,img,web)
        print("-"*40+"<<<<<spider"+"\n")
        if self.flag:
            with ThreadPoolExecutor(max_workers=5) as pool:
                results = pool.map(self.crazy,web)
                for result in results:
                    print(result)
            self.flag = 0


    def crazy(self,url):
        img,web = self.spider(url)
        self.spider_report(url,img,web)
        return


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
            # sys.exit(1)


    def spider_report(self,url,img,web):
        '''
        对爬取结果进行处理
        :return:
        '''
        path = os.path.abspath(os.path.dirname(__file__))
        parse_url = urlparse(url)
        dirname = parse_url.netloc
        dirpath = "{0}\{1}\{2}".format(path,"reports",dirname)
        imgfilepath = "{0}\{1}".format(dirpath,"spider_img_report.txt")
        webfilepath = "{0}\{1}".format(dirpath, "spider_web_report.txt")
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        imgfile = open(imgfilepath,"a")
        try:
            for m in img:
                print(m)
                imgfile.write(m+"\n")
            print("[ 网站图片链接已保存于：{}]".format(imgfilepath))
        except:
            print("[ 并没有扫描到图片链接 ]")
        imgfile.close()
        webfile = open(webfilepath, "a")
        try:
            for m in web:
                print(m)
                webfile.write(m + "\n")
            print("[ 网站网页链接已保存于：{}]".format(webfilepath))
        except:
            print("[ 并没有扫描到网页链接 ]")
            self.flag = 0
        webfile.close()
        return
