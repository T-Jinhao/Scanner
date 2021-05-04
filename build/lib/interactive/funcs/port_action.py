#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import sys
from interactive.funcs import util
from interactive.check import check_port, check_set
from interactive.run import Port
from interactive.completer import configuration
from interactive.funcs import redisUtil
r = redisUtil.Redis()

Commands = {
    'info': ['Ip', 'Timeout', 'Ports', 'Workers', 'Taskname', 'Tasknameid'],
    'set': ['Ip', 'Ports', 'Timeout', 'Workers', 'Taskname'],
    'usemodule': configuration.usemodule,
    'run': [],
    'exit': [],
    'main': [],
    'help': ['info', 'set', 'run', 'exit', 'help', 'main', 'execute'],
    'execute': []
}

Usage = {
    'info': 'Display port module options.',
    'help': 'Displays the help menu.',
    'exit': 'Exit Scanner.',
    'set': 'Set a port option.',
    'main': 'Back to the main menu.',
    'run': 'Start the given port module.',
    'usemodule': 'Use a Scanner module.',
    'execute': 'Run with threads.'
}

Info = {
    'Ip': ['True', '', 'Target ip,if input an url,it will parse to ip'],
    'Ports': ['False', 'Common', 'Target port range,example:1-80;or 80,443,3306'],
    'Timeout': ['False', util.getConfigIni('Ports', 'timeout'), 'Timeout of a socket connect.'],
    'Workers': ['False', util.getConfigIni('Ports', 'max_workers'), 'Max number of workers'],
    'Taskname': ['False', '', 'The abbreviation of current work.'],
    'Tasknameid': ['True', r.queryInitKey('Tasknameid'),
                   'The uniquely identifies of current work.And it can\'t be modified.'],
}

def checkIn(enter):
    workbench = 'port'
    words = enter.split(' ')
    if words[0] == 'usemodule':
        workbench = util.usemodule('port', words, Commands['usemodule'])
    elif words[0] == 'set':
        setOption(words)
    elif words[0] == 'exit':
        sysExit()
    elif words[0] == 'main':
        workbench = 'main'
    elif words[0] == 'help':
        util.printHelp(words, Usage)
    elif words[0] == 'run':
        updateInfo()
        run()
    elif words[0] == 'execute':
        updateInfo()
        execute()
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
        util.printError("{} cannot be modified".format(key))
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
        r.refreshTasknameid()

def updateInfo():
    # 刷新数值
    for i in ['Ip', 'Taskname', 'Tasknameid']:
        Info[i][1] = r.queryInitKey(i)
    return

def execute():
    obj = Port.port()
    if obj.checkRequired(Info):
        obj.execute(Info)
        r.refreshTasknameid()

def sysExit():
    obj = Port.port()
    obj.sysExit()