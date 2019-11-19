#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import os

print(dir())
path=os.path.dirname(__file__)
f=open(path+'/../dict/domain/domain.txt','r')
print(f)