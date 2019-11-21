#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import sys,os
from urllib.parse import urlparse
from sqlmapapi import *
from reports import reports
from Sqliscan import std
from Sqliscan import sqlerrors
from Sqliscan import web
from Sqliscan import serverinfo
import threading,time,requests,json


class Sql:
    def __init__(self,url,flag):
        self.url = url
        self.flag = flag
        self.start()

    def start(self):
        print('>>>>>Sqlscan' + '-' * 40)
        result = self.Fuzz()
        if result['flag']:
            print('[ 网站数据库：{0}  闭合payload：{1} ]'.format(result['db'],result['payload']))
        else:
            print('[ 未探测出网站数据库信息 ]')
        if self.flag:
            self.Crazy()
        print('-'*40+'Sqlscan<<<<<'+'\n')
        return

    def Fuzz(self):
        '''
        数据库fuzz脚本
        :return:
        '''
        msg = {}
        urlpath = self.url.split('?')[0]
        queries = urlparse(self.url).query.split("&")
        if not any(queries):
            msg = {'flag':0 }
            return msg
        payloads = ("'", "')", "';", '"', '")', '";', '`', '`)', '`;', '\\', "%27", "%%2727", "%25%27", "%60", "%5C")
        for payload in payloads:
            website = urlpath + "?" + ("&".join([param + payload for param in queries]))
            source = web.gethtml(website)
            if source:
                vulnerable, db = sqlerrors.check(source)
                if vulnerable and db != None:
                    msg = {'flag':1 , 'db':db , 'payload':payload}
                    return msg


    def Crazy(self):
        '''
        调用sqlmapapi扫描
        :return:
        '''
        print("[ 正在启动sqlmapapi ]")
        t = threading.Thread(target=self.start_api)
        t.start()
        time.sleep(5)  # 让sqlmapapi能完全启动
        taskid = self.get_taskid()
        if taskid:
            print('[ taskid：{} ]'.format(taskid))
            url = 'http://localhost:8775/option/{}/set'.format(taskid)  # 设置任务
            if self.api_set(url):
                url = 'http://localhost:8775/scan/{}/start'.format(taskid)  # 启动扫描
                if self.api_set(url):
                    report = self.sql_results(taskid)  # 获取报告
                    if report:
                        print(report)
                        reports.Report(report, self.url, 'sqlscan_report.txt', '主机注入漏洞扫描报告已存放于', '并没有扫描出主机注入漏洞')
                    else:
                        print('[ 并没有扫描出主机注入漏洞 ]')
                else:
                    print('[ sqlmapapi 启动扫描失败 ]')
            else:
                print('[ sqlmapapi 设置任务失败 ]')
        else:
            print('[ sqlmapapi 启动失败 ]')


    def start_api(self):
        '''
        后台启动sqlmapapi
        :return:
        '''
        path = os.path.dirname(__file__)
        file = "{0}/{1}/{2}".format(path, r'../sqlmapapi', 'sqlmapapi.py')
        cmd = 'python {} -s'.format(file)
        p = os.system(cmd)


    def get_taskid(self):
        '''
        获取taskid
        :return: taskid
        '''
        url = 'http://localhost:8775/task/new'
        try:
            res = requests.get(url)
            res = res.json()
            return res['taskid']
        except:
            return


    def api_set(self,url):
        '''
        设置扫描器
        :param url:
        :return:
        '''
        # data = json.dumps({'url' : self.url})
        headers = {'Content-Type': 'application/json'}
        try:
            res = requests.post(url,data=json.dumps({'url' : self.url}),headers=headers)
            res = res.json()
            if res['success']:
                return True
            else:
                return False
        except:
            return False


    def sql_results(self,taskid):
        '''
        执行扫描并返回结果
        :param taskid:
        :return:
        '''
        num = 1
        print('[ 此流程将极为耗时 ]')
        while 1:
            url = 'http://localhost:8775/scan/{}/status'.format(taskid)
            res = requests.get(url).json()
            # print(res)
            if res['status'] == u'terminated':
                break
            if num%3 == 0:         # 30秒打一次状态报告
                x = 'http://localhost:8775/scan/{}/log'.format(taskid)
                msg = requests.get(x).json()
                print(msg['log'][-1]['message'])
            num += 1
            time.sleep(10)    # 10秒查询一次完成状态
        url = 'http://localhost:8775/scan/{}/data'.format(taskid)
        res = requests.get(url).json()
        return res['data']
