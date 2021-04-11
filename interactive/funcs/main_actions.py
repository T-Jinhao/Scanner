#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import readline
import sys
from interactive.funcs import util

Commands = {
    'usemodule': ['burp', 'scan', 'domain', 'port'],
    'help': ['usemodule', 'exit', 'main', 'works', 'search']
}

Usage = {
    'usemodule': 'Use a Scanner module.',
    'help': 'Displays the help menu.',
    'exit': 'Exit Scanner.',
    'works': 'Lists active workers.',
    'main': 'Back to the main menu'
}

def checkIn(enter):
    words = enter.split(' ')
    if words[0] == 'usemodule':
        print('usemodule')
    elif words[0] == 'works':
        print('works')
    elif words[0] == 'exit':
        sys.exit(0)
    elif words[0] == 'main':
        print('main')
    elif words[0] == 'help':
        util.printHelp(words, Usage)



# def completer(text, state, CMD=[]):
#     options = [cmd for cmd in CMD if cmd.startswith(text)]
#     if state < len(options):
#         return options[state]
#     else:
#         return None
#
# readline.parse_and_bind("tab: complete")
# readline.set_completer(completer)

