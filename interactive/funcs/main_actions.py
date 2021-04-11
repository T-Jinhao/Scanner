#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import readline
import sys

Commands = {
    'usemodule': ['burp', 'scan', 'domain', 'port'],
    'help': ['usemodule', 'exit', 'main', 'works', 'search']
}

Usage = {
    'usemodule': 'Use a Scanner module.',
    'help': 'Displays the help menu.',
    'exit': 'Exit Scanner.',
    'works': 'Lists active workers.',
    'main': 'Back to the main menu'
}

def checkIn(enter):
    words = enter.split(' ')
    if words[0] == 'usemodule':
        print('usemodule')
    elif words[0] == 'works':
        print('works')
    elif words[0] == 'exit':
        sys.exit(0)
    elif words[0] == 'main':
        print('main')
    elif words[0] == 'help':
        printHelp(words)


def output(key, value):
    print("{0:10}   {1:10}".format(key, value))

# def completer(text, state, CMD=[]):
#     options = [cmd for cmd in CMD if cmd.startswith(text)]
#     if state < len(options):
#         return options[state]
#     else:
#         return None
#
# readline.parse_and_bind("tab: complete")
# readline.set_completer(completer)

def printBanner(banner):
    print("{0}\n{1}".format(banner, '='*len(banner)))
    return

def printHelp(words):
    printBanner('Commands')
    if len(words) == 1 or len(words) > 2:
        for k,v in Usage.items():
            output(k, v)
    else:
        if words[1] in Usage.keys():
            output(words[1], Usage[words[1]])
        else:
            print("*** No help on {}".format(words[1]))