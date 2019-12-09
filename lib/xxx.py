#!/usr/bin/python
# -*-encoding:utf8 -*-
#author:Jinhao
# 测试文档

import os
def test(**kwargs):
    b = {}
    for key,value in kwargs.items():
        print("{}:{}".format(key,value))
        b[key] = value
    print(b['name'])

if __name__ == '__main__':
    test(name='aaa',file='xxx')



