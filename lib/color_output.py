#!/usr/bin/python
# -*- encoding:utf8 -*-
import platform
import os
import sys
import ctypes
from colorama import Fore,init
from .load_config import Config

# 前景色彩色表
Red = '\033[1;31m'  # 红色
Green = '\033[1;32m'  # 绿色
Yellow = '\033[1;33m'  # 黄色
Blue = '\033[1;34m'  # 蓝色
Fuchsia = '\033[1;35m'  # 紫红色
Cyan = '\033[1;36m'  # 青蓝色
White = '\033[1;37m'  # 白色
Reset = '\033[0m'  # 终端默认颜色

# colorama彩色表
fore_color = {
    'BLACK': Fore.BLACK,   # 默认
    'RED': Fore.RED,       # 警报类，系统出错
    'GREEN': Fore.GREEN,   # 成功事件
    'YELLOW': Fore.YELLOW, # 利用失败事件
    'BLUE': Fore.BLUE,     # 运行进度
    'CYAN': Fore.CYAN,     # 配置加载
    'MAGENTA': Fore.MAGENTA   # 系统提示
}

class ColorOutput:
    def __init__(self):
        filePath = self.getConfigPath()
        self.system = platform.system()
        config = Config().readConfig(filePath)
        self.isShow = config.getboolean("Output", self.system)

    def getConfigPath(self):
        path = os.getcwd()
        if path.split('/')[-1] != 'Scanner':
            file = '/../config.ini'
        else:
            file = '/config.ini'
        filePath = path + file
        return filePath

    def red(self, s):
        if self.isShow:
            if self.system == 'Windows':
                init(autoreset=True)
            return "{0}{1}{2}".format(Red, str(s), Reset)
        return str(s)

    def green(self, s):
        if self.isShow:
            if self.system == 'Windows':
                init(autoreset=True)
            return "{0}{1}{2}".format(Green, str(s), Reset)
        return str(s)

    def yellow(self, s):
        if self.isShow:
            if self.system == 'Windows':
                init(autoreset=True)
            return "{0}{1}{2}".format(Yellow, str(s), Reset)
        return str(s)

    def blue(self, s):
        if self.isShow:
            if self.system == 'Windows':
                init(autoreset=True)
            return "{0}{1}{2}".format(Blue, str(s), Reset)
        return str(s)

    def fuchsia(self, s):
        if self.isShow:
            if self.system == 'Windows':
                init(autoreset=True)
            return "{0}{1}{2}".format(Fuchsia, str(s), Reset)
        return str(s)

    def cyan(self, s):
        if self.isShow:
            if self.system == 'Windows':
                init(autoreset=True)
            return "{0}{1}{2}".format(Cyan, str(s), Reset)
        return str(s)

    def white(self, s):
        if self.isShow:
            if self.system == 'Windows':
                init(autoreset=True)
            return "{0}{1}{2}".format(White, str(s), Reset)
        return str(s)

    def interval(self):
        if self.isShow:
            if self.system == 'Windows':
                init(autoreset=True)
            return "{0}{1}{2}".format(Red, ' | ', Reset)
        return ' | '



def color_output(text, color='BLACK', output=True):
    '''
    用作单一输出
    :param text:
    :param color:
    :param output:
    :return:
    '''
    if color not in fore_color.keys():  # 防止设置出错
        color = 'BLACK'
    if output != True:
        return
    if platform.system() != 'Windows':
        print(text)
        return
    try:
        init(autoreset=True)
        print(fore_color[color] + str(text))
    except:
        print(text)
    return

def color_list_output(textList, color='BLACK', output=True):
    '''
    用作列表输出
    :param textList:
    :param color:
    :param output:
    :return:
    '''
    if color not in fore_color.keys():  # 防止设置出错
        color = 'BLACK'
    if output != True:
        return
    if platform.system() != 'Windows':
        for x in textList:
            print(x)
        return
    for t in textList:
        try:
            print(fore_color[color] + str(t))
        except:
            print(t)
    init(autoreset=True)
    print()    # 恢复前景色
    return