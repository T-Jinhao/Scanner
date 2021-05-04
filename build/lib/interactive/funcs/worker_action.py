#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import threading
import sys
from interactive.funcs import util
from interactive.completer import configuration
from interactive.funcs import redisUtil
from interactive.run import Worker
r = redisUtil.Redis()

Commands = {
    'info': [],
    'set': [],
    'usemodule': configuration.usemodule,
    'works': [],
    'main': [],
    'help': ['info', 'set', 'usemodule', 'run', 'main', 'help', 'exit'],
    'exit': []
}

Usage = {
    'info': 'Display worker module options.',
    'help': 'Displays the help menu.',
    'exit': 'Exit Scanner.',
    'main': 'Back to the main menu.',
    'works': 'Lists active workers.',
    'usemodule': 'Use a Scanner module.',
    'set': 'Set a worker option.'
}

Info = {
    'Taskname': ['False', '', 'The uniquely identifies of current work.']
}

def checkIn(enter):
    workbench = 'worker'
    words = enter.split(' ')
    if words[0] == 'usemodule':
        workbench = util.usemodule('worker', words, Commands['usemodule'])
    elif words[0] == 'set':
        setOption(words)
    elif words[0] == 'exit':
        sysExit()
    elif words[0] == 'main':
        workbench = 'main'
    elif words[0] == 'help':
        util.printHelp(words, Usage)
    elif words[0] == 'works':
        worker()
    elif words[0] == 'info':
        # updateInfo()
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
    pass

def worker():
    obj = Worker.worker()
    obj.run()

def sysExit():
    obj = Worker.worker()
    obj.sysExit()