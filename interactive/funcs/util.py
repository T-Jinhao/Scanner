#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

from lib.load_config import Config
from lib.color_output import ColorOutput
out = ColorOutput()

def output(*args):
    s = ''
    for x in args:
        s += '{0:15}   '.format(x)
    print(s)
    return

def printBanner(*args):
    banner = ''
    interval = ''
    for x in args:
        banner += "{0:15}   ".format(x)
        interval += "{0:15}   ".format('-' * len(str(x)))
    print(banner)
    print(interval)
    return

def printHelp(words, Usage):
    if len(words) == 1 or len(words) > 2:
        printBanner('Commands', 'Description')
        for k,v in sorted(Usage.items()):
            output(k, v)
    else:
        if words[1] in Usage.keys():
            printBanner('Commands', 'Description')
            output(words[1], Usage[words[1]])
        else:
            print("*** No help on {}".format(words[1]))

def usemodule(workbench, words, CMD=[]):
    if len(words) != 2:
        printError('Invaild Module')
    elif words[1] not in CMD:
        printError('Invaild Module')
    else:
        # print('use module', words[1])
        workbench = words[1]
    return workbench

def printError(s):
    print(out.red('[!] Error: {}'.format(s)))
    return

def printWarn(s):
    print(out.yellow('[!] Warn: {}'.format(s)))
    return

def printInfo(words, Info):
    if len(words) == 1 or len(words) > 2:
        printBanner('Name', 'Required', 'Value', 'Description')
        for k, v in sorted(Info.items()):
            output(k, v[0], v[1], v[2])
    else:
        if words[1] in Info.keys():
            printBanner('Name', 'Required', 'Value', 'Description')
            output(words[1], Info[words[1]][0], Info[words[1]][1], Info[words[1]][2])
        else:
            print("*** No option on {}".format(words[1]))
    return

def getConfigIni(model, name):
    config = Config().readConfig()
    res = config.get(model, name)
    return res