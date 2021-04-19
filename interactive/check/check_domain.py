#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

from interactive.check import common
from interactive.funcs import util

class domain(common.Common):
    def checkPayload(self, input, model=''):
        '''
        需要检查输入文件，并返回payloads
        :param input:
        :param model:
        :return:
        '''
        if input == 'default':  # 修改默认值
            input = 'dict.txt'
            model = 'domain'
        payloads = self.loadPayload(input, model)
        if not payloads:
            return False
        payloads = list(set(payloads))
        return payloads