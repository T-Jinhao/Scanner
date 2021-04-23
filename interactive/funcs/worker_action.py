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
    'run': [],
    'main': [],
    'help': [],
    'exit': []
}

Usage = {
    'info': 'Display worker module options.',
    'help': 'Displays the help menu.',
    'exit': 'Exit Scanner.',
    'main': 'Back to the main menu.',
    'run': 'Start the given worker module.',
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
        sys.exit(0)
    elif words[0] == 'main':
        workbench = 'main'
    elif words[0] == 'help':
        util.printHelp(words, Usage)
    elif words[0] == 'run':
        print('run')
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