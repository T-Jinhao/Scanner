#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import readline

Workbench = {
    'main': ['help', 'usemodule', 'exit', 'main', 'works'],
    'burp': ['main', 'help', 'info', 'set', 'run', 'exit', 'usemodule'],
    'domain': ['main', 'help', 'info', 'set', 'usemodule'],
    'scan': ['main', 'help', 'info', 'set', 'usemodule'],
    'port': ['main', 'help', 'info', 'set', 'usemodule'],
    'search': ['main', 'help', 'info', 'reset', 'set', 'usemodule']
}
class Completer:
    def __init__(self, option):
        self.option = option

    def completer(self, text, state):
        keys = self.option.keys()
        buffer = readline.get_line_buffer()   # 获取当前命令行缓存的内容
        if buffer.split(' ')[0] in sorted(self.option.keys()):
            keys = self.option[buffer.split(' ')[0]]
        options = [cmd for cmd in sorted(keys) if cmd.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None