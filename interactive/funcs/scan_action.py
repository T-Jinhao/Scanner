#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import sys
from interactive.funcs import util
from interactive.check import scan
from interactive.funcs import redisUtil
r = redisUtil.Redis()

Commands = {
    'info': ['Url', 'Timeout', 'Cookie', 'Taskname', 'Workers'],
    'set': ['Url', 'Cookie', 'Timeout', 'Taskname', 'Workers'],
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
    'set': 'Set a scan option.',
    'main': 'Back to the main menu.',
    'run': 'Start the given scan module.',
    'usemodule': 'Use a Scanner module.',
}

Info = {
    'Url': ['True', '', 'Target url.'],
    'Timeout': ['False', util.getConfigIni('Scan', 'timeout'), 'Timeout of a requests connect.'],
    'Cookie': ['False', '', 'Cookie for spider.'],
    'Taskname': ['False', '', 'The uniquely identifies of current work.'],
    'Workers': ['False', util.getConfigIni('Scan', 'threads'), 'Max number of workers'],
}

def checkIn(enter):
    workbench = 'burp'
    words = enter.split(' ')
    if words[0] == 'usemodule':
        workbench = util.usemodule('scan', words, Commands['usemodule'])
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
    obj = scan.scan()
    if key == 'Timeout':
        return obj.checkTimeout(value)
    elif key == 'Taskname':
        return obj.checkTaskname(value)
    elif key == 'Cookie':
        return obj.setCookie(value)
    elif key == 'Url':
        return obj.checkUrl(value)
    elif key == 'Workers':
        return obj.checkWorkers(value)
