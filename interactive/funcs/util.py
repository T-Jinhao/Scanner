#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import random
import string
import datetime
import yarl
import re
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

def getTaskname(url, name=None):
    '''
    获取任务简称名，以域名为主
    :param url: 网址
    :param name: 自定义名称
    :return:
    '''
    if name != None:
        taskname = name
    else:
        ip = re.compile('[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}')
        netloc = yarl.URL(url).host
        res = ip.match(netloc)
        if res:    # ip形式的名称，需要改名
            today = datetime.datetime.today()
            formatted_today = today.strftime('%y%m%d')
            taskname = formatted_today
        else:
            n = netloc.split(".")
            if len(n) == 2:
                taskname = n[0]
            elif n[-2] not in ["com", "edu", "ac", "net", "org", "gov"]:  # 带地域标签的域名
                taskname = n[-2]
            else:
                taskname = n[-3]
    return taskname