#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import chardet
from colorama import init, Fore, Back, Style

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
        '''
        导入payload文件
        :param file:
        :return:
        '''
        if file == None:
            return
        payload = []
        try:
            with open(file, 'rb') as f:
                encoding = chardet.detect(f.read())['encoding']
            F = open(file, 'r', encoding=encoding)
            for x in F:
                payload.append(x.replace('\n', ''))
            payload = list(set(payload))  # payload去重
        except:
            print(Fore.RED + "文件读取失败：", file)
        return payload

    def threadSetting(self, threadN, flag):
        '''
        设置线程数
        :param threadN: 线程数
        :param flag: 标志位
        :return:
        '''
        if flag and threadN < 20:
            return 20
        return threadN

    def timeoutSetting(self, timeout):
        '''
        超时设置
        :param timeout:
        :return:
        '''
        if timeout <= 0:
            timeout = 3
        return timeout
