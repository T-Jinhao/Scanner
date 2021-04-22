#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import sys
import platform
from interactive.funcs import util
from interactive.check import check_set, check_burp
from interactive.funcs import redisUtil
from interactive.run import Burp
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

P = {}

Info = {
    'Url': ['True', '', 'Target url.'],
    'Timeout': ['False', util.getConfigIni('Burp', 'timeout'), 'Timeout of a requests connect.'],
    'Workers': ['False', util.getConfigIni('Burp', 'threads'), 'Max number of workers'],
    'Payload': ['False', 'default', 'The path of the record text file.'],
    'Taskname': ['False', '', 'The uniquely identifies of current work.']
}

def checkIn(enter):
    workbench = 'burp'
    words = enter.split(' ')
    if words[0] == 'usemodule':
        workbench = util.usemodule('burp', words, Commands['usemodule'])
    elif words[0] == 'set':
        setOption(words)
    elif words[0] == 'exit':
        sys.exit(0)
    elif words[0] == 'main':
        workbench = 'main'
    elif words[0] == 'help':
        util.printHelp(words, Usage)
    elif words[0] == 'run':
        run()
    elif words[0] == 'info':
        Info['Taskname'][1] = getTaskname()
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
    obj = check_burp.burp()
    if key == 'Timeout':
        return obj.checkTimeout(value)
    elif key == 'Taskname':
        return obj.checkTaskname(value)
    elif key == 'Workers':
        return obj.checkWorkers(value)
    elif key == 'Url':
        obj.checkUrl(value)
        url = check_set.checkUrl(value)
        if url != False:
            k = 'current_' + key
            Info[key][1] = url
            r.save(k, url)
        return False  # 独立保存
    elif key == 'Payload':
        payloads = obj.checkPayload(value)
        if payloads != False:
            P['payloads'] = payloads
            if platform.system() == 'Windows':
                Info['Payload'][1] = value.split('\\')[-1]
            else:
                Info['Payload'][1] = value.split('/')[-1]
        return False

def run():
    obj = Burp.burp()
    if obj.checkRequired(Info):
        if Info['Payload'][1] == 'default':   # 获取默认payload
            checkSetValue('Payload', 'default')
        obj.run(Info, P)

def getTaskname():
    taskname = r.queryInitKey('Taskname')
    return taskname