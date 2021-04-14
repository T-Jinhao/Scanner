#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao

class BaseModel:
    def __init__(self):
        pass

    def filter(self, resp):
        # base过滤器
        if resp == None:
            return
        return resp