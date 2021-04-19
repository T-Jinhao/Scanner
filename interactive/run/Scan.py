#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

from interactive.run import common
from lib import func_scan

class scan(common.Common):
    def run(self, Info):
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
        r.scanmode = flag
        # 运行
        if flag:
            r.crazyWebScan()
        else:
            r.webScan(Info['Url'][1])
        self.getResult(r)   # 获取结果

    def getResult(self, obj):
        obj.output()
        phone = obj.Phone
        email = obj.Email
        icp = obj.ICP
        results = obj.results
        obj.saveResult(phone, 'phone', 'phone.txt', cut=' | ')
        obj.saveResult(email, 'email', 'email.txt', cut=' | ')
        obj.saveResult(icp, 'icp', 'icp.txt', cut=' | ')
        obj.saveResult(results, 'webScan', 'webScan.txt', cut=' | ')