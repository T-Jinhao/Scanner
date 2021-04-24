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
        r = func_burp.Burp(
            url=Info['Url'][1],
            payload='',    # 运行时添加
            name=Info['Taskname'][1],
            flag=0
        )
        r.load_config()
        r.threads = int(Info['Workers'][1])
        r.timeout = float(Info['Timeout'][1])
        r.isThread = isThread
        r.isShow = isShow
        # 运行
        r.scan_mode_indetify()    # 获取Scanmode
        results = r.run(payloads=payloads)  # 运行
        r.saveResult(results)

    def execute(self, Info, p_list):
        try:
            t = threading.Thread(target=self.run, args=(Info, p_list, True, False))
            t.setName(Info['Taskname'][1])
            t.start()
            util.printBanner('Thread', 'Status')
            util.output(t.getName(), t.is_alive())
        except Exception as e:
            util.printError("Can't execute!Something is wrong!")
            print(e)
        return