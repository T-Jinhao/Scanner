#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import threading
from interactive.run import common
from interactive.funcs import util
from lib import func_burp

class burp(common.Common):
    def run(self, Info, p_list, isThread=False, isShow =True):
        # 设置参数配置
        payloads = p_list['payloads']
        flag = self.getFlag(Info['Recursion'][1])
        r = func_burp.Burp(
            url=Info['Url'][1],
            payload='',    # 运行时添加
            name=Info['Taskname'][1],
            flag=flag
        )
        baseUrl = r.url_parse(Info['Url'][1]).rstrip('/')
        r.load_config()
        r.threads = int(Info['Workers'][1])
        r.timeout = float(Info['Timeout'][1])
        r.isThread = isThread
        r.isShow = isShow
        # 运行
        r.scan_mode_indetify(baseUrl=baseUrl)    # 获取Scanmode
        results = r.run(baseUrl=baseUrl, payloads=payloads)  # 运行
        r.saveResult(results)
        r.insertData(results, tasknameid=Info['Tasknameid'][1])

    def execute(self, Info, p_list):
        try:
            t = threading.Thread(target=self.run, args=(Info, p_list, True, False))
            t.setName(Info['Taskname'][1])
            t.setDaemon(True)
            t.start()
            util.printBanner('Thread', 'Status')
            util.output(t.getName(), t.is_alive())
        except Exception as e:
            util.printError("Can't execute!Something is wrong!")
            print(e)
        return