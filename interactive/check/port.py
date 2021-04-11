#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import re
from interactive.check import common
from interactive.funcs import util

class port(common.Common):
    def checkPort(self, input):
        try:
            int(input)
            return True
        except:
            pass
        minus = input.split('-')
        if len(minus) == 2:
            try:
                if (int(minus[0]) > 0) and (int(minus[0]) < 65536)\
                        and (int(minus[1]) > 0) and (int(minus[1]) < 65536) and (int(minus[0]) < int(minus[1])):
                    return True
            except:
                pass
        interval = input.split(',')
        if len(interval) > 1:
            try:
                for p in interval:
                    p = int(p)
                    if p <= 0 or p >= 65536:
                        util.printError('Invaild Value')
                        return False
                return True
            except:
                pass
        util.printError('Invaild Value')
        return False