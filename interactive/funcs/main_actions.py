#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import sys
from interactive.funcs import util

Commands = {
    'usemodule': ['burp', 'scan', 'domain', 'port'],  # 功能模块
    'help': ['usemodule', 'exit', 'main', 'works'],   # 帮助
    'exit': [],   # 退出程序
    'main': [],   # 回到主页面
    'works': []   # 查看后台工作
}

Usage = {
    'usemodule': 'Use a Scanner module.',
    'help': 'Displays the help menu.',
    'exit': 'Exit Scanner.',
    'works': 'Lists active workers.',
    'main': 'Back to the main menu.'
}

def checkIn(enter):
    workbench = 'main'
    words = enter.split(' ')
    if words[0] == 'usemodule':   # 调用其他模块
        workbench = util.usemodule('main', words, Commands['usemodule'])
    elif words[0] == 'works':     # 查看运行中任务
        print('works')
    elif words[0] == 'exit':      # 退出程序
        sys.exit(0)
    elif words[0] == 'main':      # 回到主控制台页面
        workbench = 'main'
    elif words[0] == 'help':      # 打印帮助信息
        util.printHelp(words, Usage)
    return workbench




