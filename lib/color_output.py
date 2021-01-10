#!/usr/bin/python
# -*- encoding:utf8 -*-
import platform
from colorama import Fore,init

Red = '\033[1;31m'  # 红色
Green = '\033[1;32m'  # 绿色
Yellow = '\033[1;33m'  # 黄色
Blue = '\033[1;34m'  # 蓝色
Fuchsia = '\033[1;35m'  # 紫红色
Cyan = '\033[1;36m'  # 青蓝色
White = '\033[1;37m'  # 白色
Reset = '\033[0m'  # 终端默认颜色

def red(s):
    return "{0}{1}{2}".format(Red, str(s), Reset)

def green(s):
    return "{0}{1}{2}".format(Green, str(s), Reset)

def yellow(s):
    return "{0}{1}{2}".format(Yellow, str(s), Reset)

def blue(s):
    return "{0}{1}{2}".format(Blue, str(s), Reset)

def fuchsia(s):
    return "{0}{1}{2}".format(Fuchsia, str(s), Reset)

def cyan(s):
    return "{0}{1}{2}".format(Cyan, str(s), Reset)

def white(s):
    return "{0}{1}{2}".format(White, str(s), Reset)

def interval():
    return "{0}{1}{2}".format(Red, ' | ', Reset)


fore_color = {
    'BLACK': Fore.BLACK,   # 默认
    'RED': Fore.RED,       # 警报类，系统出错
    'GREEN': Fore.GREEN,   # 成功事件
    'YELLOW': Fore.YELLOW, # 利用失败事件
    'BLUE': Fore.BLUE,     # 运行进度
    'CYAN': Fore.CYAN,     # 配置加载
    'MAGENTA': Fore.MAGENTA   # 系统提示
}

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

