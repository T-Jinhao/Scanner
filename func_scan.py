#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import os,sys
import requests,re
from dict import *
from urllib.parse import urlparse


class Scan():
    def __init__(self,url,cookies):
        self.url = self.url_parse(url)
        self.web_type = self.web_indetify(url)
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        self.cookies = cookies
        print(self.web_type)



    def url_parse(self,url):
        '''
        去除url中的params和query部分
        :param url: 待解析的链接
        :return:url的上级目录
        '''
        parse_url = urlparse(url)
        url = parse_url.scheme + '://' + parse_url.netloc + parse_url.path
        if parse_url.path == '':
            return url
        else:
            url = url.rsplit('/', 1)
            if re.match('(.*?)\.(.*?)', url[1]):
                return url[0]
            else:
                x = url[0] + '/' + url[1]
                return x

    def web_indetify(self,url):
        parse_url = urlparse(url)
        path = parse_url.path
        path = path.rsplit('/', 1)
        print(path[1])
        s = re.match('(.*?)\.(.*)', path[1])
        if s == None:
            return 'all'
        else:
            return s.group(2)
