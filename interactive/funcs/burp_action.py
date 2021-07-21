#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import sys
import platform
from interactive.funcs import util
from interactive.check import check_set, check_burp
from interactive.funcs import redisUtil
from interactive.completer import configuration
from interactive.run import Burp
r = redisUtil.Redis()

Commands = {
    'info': ['Url', 'Timeout', 'Workers', 'Payload', 'Taskname', 'Tasknameid', 'Recursion'],
    'set': ['Url', 'Payload', 'Timeout', 'Workers', 'Taskname', 'Recursion'],
    'usemodule': configuration.usemodule,
    'run': [],
    'exit': [],
    'main': [],
    'help': ['info', 'set', 'run', 'exit', 'help', 'main', 'execute'],
    'execute': []
}

Usage = {
    'info': 'Display burp module options.',
    'help': 'Displays the help menu.',
    'exit': 'Exit Scanner.',
    'set': 'Set a burp option.',
    'main': 'Back to the main menu.',
    'run': 'Start the given burp module.',
    'usemodule': 'Use a Scanner module.',
    'execute': 'Run with threads.'
}

P = {}

Info = {
    'Url': ['True', '', 'Target url.'],
    'Timeout': ['False', util.getConfigIni('Burp', 'timeout'), 'Timeout of a requests connect.'],
    'Workers': ['False', util.getConfigIni('Burp', 'threads'), 'Max number of workers'],
    'Payload': ['False', 'default', 'The path of the record text file.'],
    'Taskname': ['False', '', 'The abbreviation of current work.'],
    'Tasknameid': ['True', r.queryInitKey('Tasknameid'),
                   'The uniquely identifies of current work.And it can\'t be modified.'],
    'Recursion': ['False', 'False', 'Recursive directory blasting.']
}

def checkIn(enter):
    workbench = 'burp'
    words = enter.split(' ')
    if words[0] == 'usemodule':
        workbench = util.usemodule('burp', words, Commands['usemodule'])
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
        # 自动刷新taskname
        obj.setTaskname(url)
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
        obj.saveRecord(
            Info=Info,
            module='burp',
            target=Info['Url'][1],
            action='run'
        )
        obj.run(Info, P)
        r.refreshTasknameid()   # 刷新tasknameid

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
    obj = Burp.burp()
    if obj.checkRequired(Info):
        if Info['Payload'][1] == 'default':   # 获取默认payload
            checkSetValue('Payload', 'default')
        obj.saveRecord(
            Info=Info,
            module='burp',
            target=Info['Url'][1],
            action='execute'
        )
        obj.execute(Info, P)
        r.refreshTasknameid()   # 刷新tasknameid

def sysExit():
    obj = Burp.burp()
    obj.sysExit()