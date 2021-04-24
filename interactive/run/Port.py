#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import threading
from interactive.run import common
from interactive.funcs import util
from lib import func_ports

class port(common.Common):
    def run(self, Info, isShow=True):
        # 设置参数配置
        ports = self.getPorts(Info['Ports'][1])
        r = func_ports.Ports(
            host=Info['Ip'][1],
            name=Info['Taskname'][1],
            flag=0
        )
        r.load_config()
        r.timeout = float(Info['Timeout'][1])
        r.max_workers = int(Info['Workers'][1])
        # 运行并保存
        report = r.run(port=ports)
        new_report = r.showReport(report, isShow=isShow)
        r.saveResult(new_report)

    def getPorts(self, input):
        if input == 'Common':
            ports = func_ports.port_dict.keys()
        else:
            minus = input.split('-')
            interval = input.split(',')
            if len(minus) > 1:
                ports = [i for i in range(int(minus[0]), int(minus[1])+1)]
            else:
                ports = interval
        return ports

    def execute(self, Info):
        try:
            t = threading.Thread(target=self.run, args=(Info, False,))
            t.setName(Info['Taskname'][1])  # 多线程命名
            t.start()
            self.threads.append(t)
            util.printBanner('Thread', 'Status')
            util.output(t.getName(), t.is_alive())
        except Exception as e:
            util.printError("Can't execute!Something is wrong!")
            print(e)
        return
