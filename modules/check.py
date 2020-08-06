#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

class O:
    def checkCookies(self, cookie):
        '''
        检查cookie并组合cookie
        :param cookie:
        :return:
        '''
        if cookie == None:
            return
        cookies = {}  # 初始化cookies字典变量
        for x in cookie.split(';'):  # 按照字符：进行划分读取
            name, value = x.strip().split('=', 1)
            cookies[name] = value  # 为字典cookies添加内容
        return cookies

    def fileRead(self, file):
        if file == None:
            return

    def threadSetting(self, threadN, flag):
        if flag and threadN < 20:
            return 20
        return threadN

    def timeoutSetting(self, timeout):
        if timeout <= 0:
            timeout = 3
        return timeout
