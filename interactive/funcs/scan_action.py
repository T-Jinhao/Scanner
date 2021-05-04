#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import sys
from interactive.funcs import util
from interactive.check import check_scan, check_set
from interactive.funcs import redisUtil
from interactive.completer import configuration
from interactive.run import Scan
r = redisUtil.Redis()

Commands = {
    'info': ['Url', 'Timeout', 'Cookie', 'Taskname', 'Workers', 'Cycles', 'Recursion', 'Tasknameid'],
    'set': ['Url', 'Cookie', 'Timeout', 'Taskname', 'Workers', 'Cycles', 'Recursion'],
    'usemodule': configuration.usemodule,
    'run': [],
    'exit': [],
    'main': [],
    'help': ['info', 'set', 'run', 'exit', 'help', 'main', 'execute'],
    'execute': []
}

Usage = {
    'info': 'Display scan module options.',
    'help': 'Displays the help menu.',
    'exit': 'Exit Scanner.',
    'set': 'Set a scan option.',
    'main': 'Back to the main menu.',
    'run': 'Start the given scan module.',
    'usemodule': 'Use a Scanner module.',
    'execute': 'Run with threads.'
}

Info = {
    'Url': ['True', '', 'Target url.'],
    'Timeout': ['False', util.getConfigIni('Scan', 'timeout'), 'Timeout of a requests connect.'],
    'Cookie': ['False', '', 'Cookie for spider.'],
    'Taskname': ['False', '', 'The abbreviation of current work.'],
    'Tasknameid': ['True', r.queryInitKey('Tasknameid'),
                   'The uniquely identifies of current work.And it can\'t be modified.'],
    'Workers': ['False', util.getConfigIni('Scan', 'threads'), 'Max number of workers.'],
    'Cycles': ['False', util.getConfigIni('Scan', 'cycles'), 'Maximum number of recursive scans.'],
    'Recursion': ['False', 'False', 'Open multi-layer crawl.']
}

def checkIn(enter):
    workbench = 'scan'
    words = enter.split(' ')
    if words[0] == 'usemodule':
        workbench = util.usemodule('scan', words, Commands['usemodule'])
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
        return False
    obj = check_scan.scan()
    if key == 'Timeout':
        return obj.checkTimeout(value)
    elif key == 'Taskname':
        return obj.checkTaskname(value)
    elif key == 'Cookie':
        return obj.setCookie(value)
    elif key == 'Url':
        obj.checkUrl(value)
        url = check_set.checkUrl(value)
        if url != False:
            k = 'current_' + key
            Info[key][1] = url
            r.save(k, url)
        # 自动刷新taskname
        obj.setTaskname(url)
        return False  # 独立保存
    elif key == 'Workers':
        return obj.checkWorkers(value)
    elif key == 'Cycles':
        return obj.checkCycles(value)
    elif key == 'Recursion':
        return obj.checkBool(value)

def run():
    obj = Scan.scan()
    if obj.checkRequired(Info):
        obj.saveRecord(
            Info=Info,
            module='scan',
            target=Info['Url'][1],
            action='run'
        )
        obj.run(Info)
        r.refreshTasknameid()

def updateInfo():
    # 刷新数值
    for i in ['Url', 'Taskname', 'Tasknameid']:
        new_value = r.queryInitKey(i)
        if new_value != None:
            Info[i][1] = new_value
        if new_value == None and i == 'Tasknameid':
            Info[i][1] = util.getRangeStr()
    return

def execute():
    obj = Scan.scan()
    if obj.checkRequired(Info):
        obj.saveRecord(
            Info=Info,
            module='scan',
            target=Info['Url'][1],
            action='execute'
        )
        obj.execute(Info)
        r.refreshTasknameid()   # 刷新tasknameid

def sysExit():
    obj = Scan.scan()
    obj.sysExit()