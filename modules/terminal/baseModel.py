#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao

from lib.color_output import ColorOutput

class BaseModel:
    def __init__(self):
        self.Output = ColorOutput()

    async def filter(self, resp):
        # base过滤器
        if resp == None:
            return
        return resp