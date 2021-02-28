#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import configparser
import sys

class config:
    def __init__(self):
        pass

    def readConfig(self, file="config.ini"):
        config = configparser.ConfigParser()
        try:
            config.read(file)
            return config
        except:
            print("解析config.ini出错")
            sys.exit(0)
