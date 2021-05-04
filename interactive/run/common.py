#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import sys
import datetime
from interactive.funcs import util
from model import pgsql
from model.TaskModel import TaskModel
from lib.color_output import ColorOutput

class Common:
    def __init__(self):
        pass

    def checkRequired(self, Info):
        for x in Info:
            if Info[x][0] == 'True' and Info[x][1] in ['', None]:
                util.printWarn('{} is required'.format(x))
                return False
        return True

    def getFlag(self, input):
        if input in ['True', 'true', '1']:
            return 1
        else:
            return 0

    def sysExit(self):
        out = ColorOutput()
        confirm = input(out.red("Whether to exit the program? Y/n\n"))
        if confirm not in ['Y', 'y']:
            return
        sys.exit()

    def saveRecord(self, Info, description='', target='', action=''):
        d = {
            'timestamp': datetime.datetime.now(),
            'taskname': Info['Taskname'][1],
            'tasknameid': Info['Tasknameid'][1],
            'description': description,
            'target': target,
            'action': action
        }
        pgsql.insert(TaskModel, data=d)
        return