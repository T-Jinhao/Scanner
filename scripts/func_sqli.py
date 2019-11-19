#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import subprocess
import sys,os


class Sql:
    def __init__(self,url,flag):
        self.url = url
        self.flag = flag
        self.start()

    def start(self):
        pass