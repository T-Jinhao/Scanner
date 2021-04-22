#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import sys
from interactive.funcs import util
from interactive.check import check_port, check_set
from interactive.run import Port
from interactive.funcs import redisUtil
r = redisUtil.Redis()

Commands = {
    'info': ['Ip', 'Timeout', 'Ports', 'Workers', 'Taskname'],
    'set': ['Ip', 'Ports', 'Timeout', 'Workers', 'Taskname'],
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
    'set': 'Set a port option.',
    'main': 'Back to the main menu.',
    'run': 'Start the given port module.',
    'usemodule': 'Use a Scanner module.',
}

Info = {
    'Ip': ['True', '', 'Target ip,if input an url,it will parse to ip'],
    'Ports': ['False', 'Common', 'Target port range,example:1-80;or 80,443,3306'],
    'Timeout': ['False', util.getConfigIni('Ports', 'timeout'), 'Timeout of a socket connect.'],
    'Workers': ['False', util.getConfigIni('Ports', 'max_workers'), 'Max number of workers'],
    'Taskname': ['False', '', 'The uniquely identifies of current work.']
}

def checkIn(enter):
    workbench = 'port'
    words = enter.split(' ')
    if words[0] == 'usemodule':
        workbench = util.usemodule('port', words, Commands['usemodule'])
    elif words[0] == 'set':
        setOption(words)
    elif words[0] == 'exit':
        sys.exit(0)
    elif words[0] == 'main':
        workbench = 'main'
    elif words[0] == 'help':
        util.printHelp(words, Usage)
    elif words[0] == 'run':
        updateInfo()
        run()
    elif words[0] == 'info':
        updateInfo()
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
    obj = check_port.port()
    if key == 'Timeout':
        return obj.checkTimeout(value)
    elif key == 'Ports':
        return obj.checkPort(value)
    elif key == 'Workers':
        return obj.checkWorkers(value)
    elif key == 'Taskname':
        return obj.checkTaskname(value)
    elif key == 'Ip':
        obj.checkIp(value)
        ip = check_set.getIp(value)
        if ip != False:
            k = 'current_' + key
            Info[key][1] = ip
            r.save(k, ip)
        return False  # 独立保存

def run():
    obj = Port.port()
    if obj.checkRequired(Info):
        obj.run(Info)

def updateInfo():
    # 刷新数值
    for i in ['Ip', 'Taskname']:
        Info[i][1] = r.queryInitKey(i)
    return