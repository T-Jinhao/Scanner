#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import readline
import sys
from interactive.funcs import util

Commands = {
    'usemodule': ['burp', 'scan', 'domain', 'port'],
    'help': ['usemodule', 'exit', 'main', 'works'],
    'exit': [],
    'main': [],
    'works': []
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



# def completer(text, state, CMD=[]):
#     options = [cmd for cmd in CMD if cmd.startswith(text)]
#     if state < len(options):
#         return options[state]
#     else:
#         return None
#
# readline.parse_and_bind("tab: complete")
# readline.set_completer(completer)

