#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import requests,sys
import re,os
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class Spider():
    def __init__(self,url,cookies):
        self.url = url
        print(">>>>>spider"+"-"*40)
        print("[ 开始爬取网页链接：{}]".format(url))
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        self.cookies = cookies
        self.img,self.web = self.spider()
        self.spider_report()
        print("-"*40+"<<<<<spider"+"\n")


    def spider(self):
        '''
        爬取当前页面的URL
        :return:网站相关链接
        '''
        try:
            res = requests.post(self.url,headers=self.headers,cookies=self.cookies,timeout=10)
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


    def spider_report(self):
        '''
        对爬取结果进行处理
        :return:
        '''
        path = os.path.abspath(os.path.dirname(__file__))
        parse_url = urlparse(self.url)
        dirname = parse_url.netloc
        dirpath = "{0}\{1}\{2}".format(path,"reports",dirname)
        imgfilepath = "{0}\{1}".format(dirpath,"spider_img_report.txt")
        webfilepath = "{0}\{1}".format(dirpath, "spider_web_report.txt")
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        imgfile = open(imgfilepath,"a")
        try:
            for m in self.img:
                print(m)
                imgfile.write(m+"\n")
            print("[ 网站图片链接已保存于：{}]".format(imgfilepath))
        except:
            print("[ 并没有扫描到图片链接 ]")
        imgfile.close()
        webfile = open(webfilepath, "a")
        try:
            for m in self.web:
                print(m)
                webfile.write(m + "\n")
            print("[ 网站网页链接已保存于：{}]".format(webfilepath))
        except:
            print("[ 并没有扫描到网页链接 ]")
        webfile.close()
        return
