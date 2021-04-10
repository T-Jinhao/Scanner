#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

from lib.color_output import *

class Interactive():
    def __init__(self):
        self.Output = ColorOutput()
        print(self.Output.green("[ Scanner Console Start ]"))

    def getInput(self):
        enter = input("# ")
        print(enter)