#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

from interactive.funcs import util

class Common:
    def __init__(self):
        pass

    def checkRequired(self, Info):
        for x in Info:
            if Info[x][0] == 'True' and Info[x][1] == '':
                util.printWarn('{} is required'.format(x))
                return False
        return True

    def loadPayload(self, payload):
        default_file = ''