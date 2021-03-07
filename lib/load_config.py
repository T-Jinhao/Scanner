#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import configparser
import sys
import os
import platform

class Config:
    def __init__(self):
        pass

    def readConfig(self):
        path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        if platform.system() == 'Windows':
            file = '\\config.ini'
        else:
            file = '/config.ini'
        filePath = path + file
        config = configparser.ConfigParser()
        try:
            config.read(filePath)
            return config
        except:
            print("解析config.ini出错")
            sys.exit(0)
