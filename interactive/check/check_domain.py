#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

from interactive.check import common
from interactive.funcs import util

class domain(common.Common):
    def checkOnline(self, input):
        if input not in ['True', 'False', 'true', 'false', '0', '1']:
            util.printError('Invail Value.You can choice 0 or 1.')
            return False
        return True