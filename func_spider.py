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
        try:
            res = requests.post(self.url,headers=self.headers,cookies=self.cookies,timeout=10)
            websites = []
            print(res.text)

        except:
            print("网站访问超时")
            sys.exit(1)
