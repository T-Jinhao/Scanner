#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import requests,sys
import re



class Spider():
    def __init__(self,url,cookies):
        self.url = url
        print(url)
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        self.cookies = cookies
        self.spider()


    def spider(self):
        '''
        爬取当前页面的URL
        :return:
        '''
        try:
            res = requests.post(self.url,headers=self.headers,cookies=self.cookies,timeout=10)
            img_sites = []      # 图片链接
            web_sites = []      # 网站链接
            img_results = re.finditer('<img.*?src="(.*?)".*?>',res.text,re.S)
            web_results = re.finditer('<a href="(.*?)".*?>',res.text,re.S)
            for i in img_results:
                img_sites.append(i.group(1))
            for j in web_results:
                web_sites.append(j.group(1))
            print(img_sites)
            print(web_sites)

        except:
            print("网站访问出现点问题了...")
            sys.exit(1)
