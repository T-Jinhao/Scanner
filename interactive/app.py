#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

from lib.color_output import *
from interactive.funcs import main_actions

Commands = {
    'main': ['help', 'usemodule', 'search', 'exit', 'main', 'works'],
    'burp': ['main', 'help', 'info', 'set'],
    'domain': ['main', 'help', 'info', 'set'],
    'scan': ['main', 'help', 'info', 'set'],
    'port': ['main', 'help', 'info', 'set'],
    'search': ['main', 'help', 'info', 'reset', 'set']
}

Func = {
    'main': main_actions
}

class Interactive():
    def __init__(self):
        self.Output = ColorOutput()
        self.url = ''
        self.action = ''
        self.workbench = 'main'
        print(self.Output.green("[ Scanner Console Start ]"))

    def getInput(self):
        while 1:
            enter = input("({}) > ".format(self.workbench))
            if enter == 'exit':
                break
            self.checkIn(enter)

    def checkIn(self, enter, keywords=[]):
        # 分配工作区
        if enter.split(' ')[0] in Commands[self.workbench]:
            Func[self.workbench].checkIn(enter)
        else:
            Func[self.workbench].checkIn(enter='help')