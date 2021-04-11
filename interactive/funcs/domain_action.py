#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import sys
from interactive.funcs import util
from interactive.check import common
from interactive.funcs import redisUtil
r = redisUtil.Redis()

Commands = {
    'info': ['Url', 'Timeout', 'Workers', 'Payload', 'Taskname'],
    'set': ['Url', 'Payload', 'Timeout', 'Workers', 'Taskname'],
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
    'Url': ['True', '', 'Target url.'],
    'Timeout': ['False', util.getConfigIni('Domain', 'timeout'), 'Timeout of a requests connect.'],
    'Workers': ['False', util.getConfigIni('Domain', 'threads'), 'Max number of workers'],
    'Payload': ['False', '', 'The path of the record text file.'],
    'Taskname': ['False', '', 'The uniquely identifies of current work.']
}

def checkIn(enter):
    workbench = 'domain'
    words = enter.split(' ')
    if words[0] == 'usemodule':
        workbench = util.usemodule('domain', words, Commands['usemodule'])
    elif words[0] == 'set':
        setOption(words)
    elif words[0] == 'exit':
        sys.exit(0)
    elif words[0] == 'main':
        workbench = 'main'
    elif words[0] == 'help':
        util.printHelp(words, Usage)
    elif words[0] == 'run':
        print('run')
    elif words[0] == 'info':
        util.printInfo(words, Info)
    return workbench

def setOption(words):
    if len(words) < 3:
        util.printError('Please specify an option value')
    else:
        if checkSetValue(words[1], words[2]):
            key = 'current_' + words[1]
            Info[words[1]][1] = words[2]
            r.save(key, words[2])
    return

def checkSetValue(key, value):
    if key not in Commands['set']:
        return False
    obj = common.Common()
    if key == 'Timeout':
        return obj.checkTimeout(value)
    elif key == 'Taskname':
        return obj.checkTaskname(value)
    elif key == 'Ip':
        return obj.checkIp(value)
    elif key == 'Workers':
        return obj.checkWorkers(value)
    elif key == 'Url':
        return obj.checkUrl(value)