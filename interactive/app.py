#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import readline
from lib.color_output import *
from interactive.funcs import main_actions, burp_action, domain_action, port_action
from interactive.completer import main_completer
from interactive.funcs import redisUtil, util

Func = {
    'main': main_actions,
    'burp': burp_action,
    'domain': domain_action,
    'port': port_action
}

class Interactive():
    def __init__(self):
        self.Output = ColorOutput()
        self.url = ''
        self.action = ''
        self.workbench = 'main'
        ran_str = util.getRangeStr()
        redisUtil.Redis().initTask(ran_str)   # 初始化
        print(self.Output.green("[ Scanner Console Start ]"))

    def getInput(self):
        readline.parse_and_bind("tab: complete")
        while 1:
            readline.set_completer(main_completer.Completer(Func[self.workbench].Commands).completer)  # 自动补全
            enter = input("(Scanner\{}) > ".format(self.Output.green(self.workbench)))
            if enter == 'exit':
                break
            self.checkIn(enter)

    def checkIn(self, enter):
        # 分配工作区
        if enter.split(' ')[0] in main_completer.Workbench[self.workbench]:
            self.workbench = Func[self.workbench].checkIn(enter)
        elif enter == '':
            pass
        else:
            self.workbench = Func[self.workbench].checkIn(enter='help')
