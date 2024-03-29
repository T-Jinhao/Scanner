#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import threading
from interactive.run import common
from interactive.funcs import util
from lib import func_scan

class scan(common.Common):
    def run(self, Info, isThread=False, isShow=True):
        # 设置参数配置
        flag = self.getFlag(Info['Recursion'][1])
        r = func_scan.Scan(
            url=Info['Url'][1],
            name=Info['Taskname'][1],
            crazy=flag
        )
        r.load_config()
        r.timeout = float(Info['Timeout'][1])
        r.threads = int(Info['Workers'][1])
        r.Cycles = int(Info['Cycles'][1])
        r.isThread = isThread
        r.isShow = isShow
        r.scanmode = flag
        # 运行
        if flag:
            r.webScan(Info['Url'][1])
            r.crazyWebScan()
        else:
            r.webScan(Info['Url'][1])
        self.getResult(r, tasknameid=Info['Tasknameid'][1])   # 获取结果

    def getResult(self, obj, tasknameid=''):
        obj.output()   # 内置其他信息的数据库保存调用
        results = obj.results
        obj.saveResult(results, 'webScan', 'webScan.txt')
        obj.insertUrlData(results, tasknameid=tasknameid)

    def execute(self, Info):
        try:
            t = threading.Thread(target=self.run, args=(Info, True, False))
            t.setName(Info['Taskname'][1])
            t.setDaemon(True)
            t.start()
            util.printBanner('Thread', 'Status')
            util.output(t.getName(), t.is_alive())
        except Exception as e:
            util.printError("Can't execute!Something is wrong!")
            print(e)
        return