#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import threading
import sys
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

    def getFlag(self, input):
        if input in ['True', 'true', '1']:
            return 1
        else:
            return 0

    def sysExit(self):
        threads = threading.enumerate()
        for t in threads:
            t.setDaemon(True)
            t.join(0)
        sys.exit()