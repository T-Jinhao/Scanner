#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

from interactive.check import common
from interactive.funcs import util

class burp(common.Common):
    def checkPayload(self, input, model=''):
        '''
        需要检查输入文件，并返回payloads
        :param input:
        :param model:
        :return:
        '''
        if input == 'default':   # 修改默认值
            input = 'dicc.txt'
            model = 'burp'
        payloads = self.loadPayload(input, model)
        if not payloads:
            return False
        payloads = ['/'+x for x in payloads]
        payloads = [x.replace('//', '/') for x in payloads]  # 统一格式，再去重
        payloads = list(set(payloads))
        return payloads