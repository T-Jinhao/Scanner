#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

from interactive.run import common
from lib import func_burp

class burp(common.Common):
    def run(self, Info, p_list):
        # 设置参数配置
        payloads = p_list['payloads']
        r = func_burp.Burp(
            url=Info['Url'][1],
            payload='',    # 运行时添加
            name=Info['Taskname'][1],
            flag=0
        )
        r.load_config()
        r.threads = Info['Workers'][1]
        r.timeout = Info['Timeout'][1]
        # 运行
        r.scan_mode_indetify()    # 获取Scanmode
        results = r.run(payloads=payloads)  # 运行
        r.saveResult(results)