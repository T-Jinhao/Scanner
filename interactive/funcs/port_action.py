#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import sys
from interactive.funcs import util

Commands = {
    'info': [],
    'set': ['Ip', 'Ports', 'Timeout', 'Workers'],
    'usemodule': ['burp', 'scan', 'domain', 'port'],
    'run': [],
    'exit': [],
    'main': [],
    'help': ['info', 'set', 'run', 'exit', 'help', 'main'],
}

Usage = {
    'info': 'Display burp module options.',
    'help': 'Displays the help menu.',
    'exit': 'Exit Scanner.',
    'set': 'Set a burp option.',
    'main': 'Back to the main menu.',
    'run': 'Start the given burp module.',
    'usemodule': 'Use a Scanner module.',
}

Info = {
    'Ip': ['True', '', 'Target ip.'],
    'Ports': ['False', 'Comman Ports', 'Target port range.'],
    'Timeout': ['False', '5', 'Timeout of a socket connect.'],
    'Workers': ['False', '50', 'Max number of workers'],
}

def checkIn(enter):
    workbench = 'port'
    words = enter.split(' ')
    if words[0] == 'usemodule':
        workbench = util.usemodule('port', words, Commands['usemodule'])
    elif words[0] == 'set':
        print('set')
    elif words[0] == 'exit':
        sys.exit(0)
    elif words[0] == 'main':
        workbench = 'main'
    elif words[0] == 'help':
        util.printHelp(words, Usage)
    elif words[0] == 'run':
        print('run')
    elif words[0] == 'info':
        info()
    return workbench

def info():
    util.printBanner('Name', 'Required', 'Value', 'Description')
    for k, v in sorted(Info.items()):
        util.output(k, v[0], v[1], v[2])
    return



