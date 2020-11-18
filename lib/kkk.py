#!/usr/bin/python
# -*-encoding:utf8 -*-
#author:Jinhao
# 测试文档

import os,re
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

def find_Email( content):
    '''
    匹配邮箱
    :param content:
    :return:
    '''
    compile_Phone = re.compile(r'1[3456789]\d{9}')
    ret = compile_Phone.findall(content)
    return ret

if __name__ == '__main__':
    email = 'asdfas d15302477100asdofjih '
    x = find_Email(email)
    print(x)



