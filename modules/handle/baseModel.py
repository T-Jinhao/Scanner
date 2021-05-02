#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao

import re
from lib.color_output import ColorOutput

class BaseModel:
    def __init__(self, scanmode=0, isShow=True):
        self.Output = ColorOutput()
        self.scanmode = scanmode
        self.isShow = isShow
        # burp模块
        self.title_list = []
        self.length_list = []
        # subdomain模块
        self.IP_list = {}
        # scan模块
        self.capture_Email = []
        self.capture_Phone = []
        self.capture_ICP = []
        self.capture_Js = []
        self.capture_Url = []

    async def filter(self, resp):
        # base过滤器
        if resp == None:
            return
        return resp

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
                    msg = {
                        'url': url,
                        'email': x
                    }
                    self.capture_Email.append(msg.copy())
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
                msg = {
                    'icp': ret[0],
                    'url': url
                }
                self.capture_ICP.append(msg.copy())
        except:
            pass
        return

    def match_Phone(self, text, url):
        '''
        匹配手机号码
        :param text:
        :return:
        '''
        compile_Phone = re.compile(r'1[358]\d{9}')
        ret = compile_Phone.findall(text)
        if ret != []:
            for x in ret:
                if x not in self.capture_Phone:
                    msg = {
                        'capture_phone': str(x),
                        'current_url': url
                    }
                    self.capture_Phone.append(msg.copy())
        return