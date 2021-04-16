#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao

import re
import yarl
from bs4 import BeautifulSoup
from modules.terminal.baseModel import BaseModel
from modules.func import util

class Terminal(BaseModel):
    async def filter(self, resp, url=''):
        if resp == None:
            return
        text = resp.text
        rurl = str(resp.url)  # resp.url为non-str
        self.match_Email(text, rurl)
        self.match_Phone(text, rurl)
        self.match_ICP(text, rurl)
        self.match_Url(text, rurl)
        # 递归爬取，过滤部分页面
        if self.scanmode:
            self.capture_Url = self.filter_Url(self.capture_Url)


    def match_Url(self, text, url):
        '''
        提取页面url
        :param text: 文本
        :param url: 当前URL
        :return:
        '''
        wrong_list = ['javascript:void(0)', None, '###', '#']
        soup = BeautifulSoup(text, 'html.parser')
        web_links = soup.find_all('a')
        js_links = soup.find_all('script')

        for j in web_links:
            y = j.get('href')  # 提取href后的链接
            if y not in wrong_list:
                u = util.splicingUrl(url, y)
                if u != None and u.startswith('http'):
                    if util.judgingOrigin(url, u):
                        self.capture_Url.append(u)  # 处理获取到的url

        for k in js_links:
            z = k.get('src')
            if z != None:
                u = util.splicingUrl(url, z)
                if u != None and u.startswith('http'):
                    self.capture_Js.append(u)

    def filter_Url(self, url):
        ignore_name = ['html', 'htm']   # 这些静态页面暂时过滤
        for u in url:
            name = yarl.URL(u).name.split('.')[-1]
            if name in ignore_name:     # 忽略静态页面
                url.remove(u)
            if util.isNumber(name):     # 移除页面，xxx.com/2等页码网址
                url.remove(u)
        return url
