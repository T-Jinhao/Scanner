#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import random
import string
from lib.load_config import Config
from lib.color_output import ColorOutput
out = ColorOutput()

def output(*args):
    # 分块打印
    s = ''
    for x in args:
        s += '{0:15}   '.format(str(x))
    print(s)
    return

def printBanner(*args):
    # 打印banner
    banner = ''
    interval = ''
    for x in args:
        banner += "{0:15}   ".format(str(x))
        interval += "{0:15}   ".format('-' * len(str(x)))
    print(banner)
    print(interval)
    return

def printHelp(words, Usage):
    # 打印帮助信息
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
    # 切换工作台
    if len(words) != 2:
        printError('Invaild Module')
    elif words[1] not in CMD:
        printError('Invaild Module')
    else:
        # print('use module', words[1])
        workbench = words[1]
    return workbench

def printError(s):
    # 打印错误
    print(out.red('[!] Error: {}'.format(s)))
    return

def printWarn(s):
    # 打印警告
    print(out.yellow('[!] Warn: {}'.format(s)))
    return

def printInfo(words, Info):
    # 打印配置
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
    # 获取config
    config = Config().readConfig()
    res = config.get(model, name)
    return res

def getRangeStr(len=6):
    # 设置随机字符串
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, len))
    return ran_str