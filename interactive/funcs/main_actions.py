#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import readline

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
    if words[0] == 'help':
        printHelp(words)


def output(key, value):
    print("{0:10}   {1:10}".format(key, value))

def printHelp(words):
    if len(words) == 1 or len(words) > 2:
        for k,v in Usage.items():
            output(k, v)
    else:
        if words[1] in Usage.keys():
            output(words[1], Usage[words[1]])
        else:
            print("*** No help on {}".format(words[1]))