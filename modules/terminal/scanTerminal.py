#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao

import re
from bs4 import BeautifulSoup
from modules.terminal.baseModel import BaseModel
from modules.func import util

class Terminal(BaseModel):
    async def filter(self, resp, url=''):
        if resp == None:
            return
        # 多层爬取模式
        if self.scanmode:
            print('scanmode')
        else:
            text = resp.text
            rurl = str(resp.url)  # resp.url为non-str
            self.match_Url(text, rurl)
            self.match_Email(text, rurl)
            self.match_Phone(text, rurl)
            self.match_ICP(text, rurl)


    def match_Email(self, text, url):
        '''
        匹配邮箱
        :param text:
        :return:
        '''
        compile_Email = re.compile(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]{0,4}')
        ret = compile_Email.findall(text)
        if ret != []:
            for x in ret:
                if x not in self.capture_Email and x.split('.')[-1] != 'png':
                    e = " | ".join([x, url])
                    self.capture_Email.append(e)
        return

    def match_ICP(self, text, url):
        '''
        匹配ICP备案号
        :param text:
        :return:
        '''
        compile_ICP = re.compile("([\u4e00-\u9fa5]ICP备\d{8}号-([0-9]|10))")
        ret = compile_ICP.search(text)
        try:
            if ret != None and ret[0] not in self.capture_ICP and ret[0] != []:
                i = " | ".join([ret[0], url])
                self.capture_ICP.append(i)
        except:
            pass
        return

    def match_Phone(self, text, url):
        '''
        匹配手机号码
        :param text:
        :return:
        '''
        compile_Phone = re.compile(r'1[3456789]\d{9}')
        ret = compile_Phone.findall(text)
        if ret != []:
            for x in ret:
                if x not in self.capture_Phone:
                    p = " | ".join([str(x), url])
                    self.capture_Phone.append(p)
        return

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
