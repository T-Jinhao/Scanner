#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import sys
import platform
from interactive.funcs import util
from interactive.check import check_domain, check_set
from interactive.funcs import redisUtil
from interactive.completer import configuration
from interactive.run import Domain
r = redisUtil.Redis()

Commands = {
    'info': ['Url', 'Timeout', 'Workers', 'Payload', 'Taskname'],
    'set': ['Url', 'Payload', 'Timeout', 'Workers', 'Taskname', 'Online'],
    'usemodule': configuration.usemodule,
    'run': [],
    'exit': [],
    'main': [],
    'help': ['info', 'set', 'run', 'exit', 'help', 'main', 'execute'],
    'execute': []
}

Usage = {
    'info': 'Display domain module options.',
    'help': 'Displays the help menu.',
    'exit': 'Exit Scanner.',
    'set': 'Set a domain option.',
    'main': 'Back to the main menu.',
    'run': 'Start the given domain module.',
    'usemodule': 'Use a Scanner module.',
    'execute': 'Run with threads.'
}

P = {'payloads': []}

Info = {
    'Url': ['True', '', 'Target url.'],
    'Timeout': ['False', util.getConfigIni('Domain', 'timeout'), 'Timeout of a requests connect.'],
    'Workers': ['False', util.getConfigIni('Domain', 'threads'), 'Max number of workers'],
    'Payload': ['False', 'default', 'The path of the record text file.'],
    'Taskname': ['False', '', 'The uniquely identifies of current work.'],
    'Online': ['False', 'True', 'Get records on online platforms first.']
}

def checkIn(enter):
    workbench = 'domain'
    words = enter.split(' ')
    if words[0] == 'usemodule':
        workbench = util.usemodule('domain', words, Commands['usemodule'])
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
    obj = check_domain.domain()
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
    elif key == 'Online':
        return obj.checkBool(value)
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
    obj = Domain.domain()
    if obj.checkRequired(Info):
        if Info['Payload'][1] == 'default':   # 获取默认payload
            checkSetValue('Payload', 'default')
        obj.run(Info, P)

def updateInfo():
    # 刷新数值
    for i in ['Url', 'Taskname']:
        Info[i][1] = r.queryInitKey(i)
    return

def execute():
    obj = Domain.domain()
    if obj.checkRequired(Info):
        if Info['Payload'][1] == 'default':   # 获取默认payload
            checkSetValue('Payload', 'default')
        obj.execute(Info, P)

def sysExit():
    obj = Domain.domain()
    obj.sysExit()