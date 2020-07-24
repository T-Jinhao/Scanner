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

def ggg():
    a = "aaa.com/"
    b = "https://aaa.com/"
    c = "http://aaa.com/aa/bb/"
    print(a.strip('http://'))
    print(b.strip('http://').strip('https://'))
    print(c.strip('http://'))

if __name__ == '__main__':
    # test(name='aaa',file='xxx')
    ggg()



