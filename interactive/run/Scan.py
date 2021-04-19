#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

from interactive.run import common
from lib import func_scan

class scan(common.Common):
    def run(self, Info):
        # 设置参数配置
        r = func_scan.Scan(
            url=Info['Url'][1],
            name=Info['Taskname'][1],
            crazy=0
        )