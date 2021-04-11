#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

from lib.color_output import *
from interactive.funcs import main_actions, burp_action

Commands = {
    'main': ['help', 'usemodule', 'exit', 'main', 'works'],
    'burp': ['main', 'help', 'info', 'set', 'run', 'exit', 'usemodule'],
    'domain': ['main', 'help', 'info', 'set', 'usemodule'],
    'scan': ['main', 'help', 'info', 'set', 'usemodule'],
    'port': ['main', 'help', 'info', 'set', 'usemodule'],
    'search': ['main', 'help', 'info', 'reset', 'set', 'usemodule']
}

Func = {
    'main': main_actions,
    'burp': burp_action
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
            enter = input("(Scanner\{}) > ".format(self.workbench))
            if enter == 'exit':
                break
            self.checkIn(enter)

    def checkIn(self, enter):
        # 分配工作区
        if enter.split(' ')[0] in Commands[self.workbench]:
            self.workbench = Func[self.workbench].checkIn(enter)
        else:
            self.workbench = Func[self.workbench].checkIn(enter='help')