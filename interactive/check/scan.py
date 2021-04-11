#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import re
from interactive.check import common
from interactive.funcs import util

class scan(common.Common):
    def setCookie(self, cookie):
        try:
            cookies = {}  # 初始化cookies字典变量
            for x in cookie.split(';'):  # 按照字符：进行划分读取
                name, value = x.strip().split('=', 1)
                cookies[name] = value  # 为字典cookies添加内容
            return cookies
        except:
            util.printError('Invaild Value')
            return False