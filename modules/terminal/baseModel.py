#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao

from lib.color_output import ColorOutput

class BaseModel:
    def __init__(self, scanmode=0):
        self.Output = ColorOutput()
        self.scanmode = scanmode
        # burp模块
        self.title_list = []
        self.length_list = []

    async def filter(self, resp):
        # base过滤器
        if resp == None:
            return
        return resp