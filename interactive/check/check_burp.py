#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

from interactive.check import common
from interactive.funcs import util

class burp(common.Common):
    def checkPayload(self, input, model=''):
        if input == 'default':   # 修改默认值
            input = 'dicc.txt'
            model = 'burp'
        payloads = self.loadPayload(input, model)
        if not payloads:
            return False
        return True