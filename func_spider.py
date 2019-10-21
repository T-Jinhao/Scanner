#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import requests
import re

class Spider():
    def __init__(self,url):
        self.url = url
        print(self.url)