#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

def output(key, value):
    print("{0:10}   {1:10}".format(key, value))

def printBanner(banner):
    print("{0}\n{1}".format(banner, '='*len(banner)))
    return

def printHelp(words, Usage):
    printBanner('Commands')
    if len(words) == 1 or len(words) > 2:
        for k,v in Usage.items():
            output(k, v)
    else:
        if words[1] in Usage.keys():
            output(words[1], Usage[words[1]])
        else:
            print("*** No help on {}".format(words[1]))