#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import sys
from interactive.funcs import util
from interactive.funcs import redisUtil
from interactive.check import common, check_set
from interactive.completer import modules
r = redisUtil.Redis()

Commands = {
    'usemodule': modules.usemodule,  # 功能模块
    'help': ['usemodule', 'exit', 'main', 'works'],   # 帮助
    'set': ['Url', 'Ip', 'Taskname'],
    'info': ['Url', 'Ip', 'Taskname'],
    'exit': [],   # 退出程序
    'main': [],   # 回到主页面
    'works': []   # 查看后台工作
}

Usage = {
    'usemodule': 'Use a Scanner module.',
    'help': 'Displays the help menu.',
    'set': 'Set a Scanner option.',
    'exit': 'Exit Scanner.',
    'works': 'Lists active workers.',
    'main': 'Back to the main menu.'
}

Info = {
    'Ip': ['False', '', 'Target ip.'],
    'Url': ['True', '', 'Target url.'],
    'Taskname': ['True', r.queryInitKey('Taskname'), 'The uniquely identifies of current work.']
}

def checkIn(enter):
    workbench = 'main'
    words = enter.split(' ')
    if words[0] == 'usemodule':   # 调用其他模块
        workbench = util.usemodule('main', words, Commands['usemodule'])
    elif words[0] == 'works':     # 查看运行中任务
        print('works')
    elif words[0] == 'exit':      # 退出程序
        sys.exit(0)
    elif words[0] == 'main':      # 回到主控制台页面
        workbench = 'main'
    elif words[0] == 'help':      # 打印帮助信息
        util.printHelp(words, Usage)
    elif words[0] == 'info':      # 打印信息
        updateInfo()
        util.printInfo(words, Info)
    elif words[0] == 'set':
        setOption(words)
    return workbench

def setOption(words):
    # 插入Info字典，并存入redis
    if len(words) < 3:
        util.printError('Please specify an option value')
    else:
        if checkSetValue(words[1], words[2]):
            key = 'current_' + words[1]
            r.save(key, words[2])
    return

def checkSetValue(key, value):
    if key not in Commands['set']:
        return False
    obj = common.Common()
    if key == 'Url':
        # 存入URL
        obj.checkUrl(value)
        url = check_set.checkUrl(value)
        if url != False:
            k = 'current_' + key
            Info[key][1] = url
            r.save(k, url)
        # 传入URL时，自动获取IP并插入
        obj.checkIp(value)
        ip = check_set.getIp(value)
        if ip != False:
            key = 'Ip'
            k = 'current_' + key
            Info[key][1] = ip
            r.save(k, ip)
        return False  # 独立保存
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

def updateInfo():
    # 刷新数值
    for i in ['Ip', 'Taskname', 'Url']:
        Info[i][1] = r.queryInitKey(i)
    return


