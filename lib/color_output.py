#!/usr/bin/python
# -*- encoding:utf8 -*-
from colorama import init, Fore

# Colors = {
#     "BLACK": "\033[0;30m%s\033[0m",
#     "RED": "\033[0;31m%s\033[0m",
#     "GREEN": "\033[0;32m%s\033[0m",
#     "YELLOW": "\033[0;33m%s\033[0m",
#     "BLUE": "\033[0;34m%s\033[0m",
#     "PURPLE": "\033[0;35m%s\033[0m",
# }

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
    if color not in fore_color.keys():  # 防止设置出错
        color = 'BLACK'
    if output != True:
        return
    try:
        init(autoreset=True)
        print(fore_color[color] + text)
    except:
        print(text)
    return

