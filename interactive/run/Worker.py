#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import threading
from interactive.run import common
from interactive.funcs import util

class worker(common.Common):
    def run(self):
        threads = threading.enumerate()
        util.printBanner("Threads", "Status")
        for t in threads:
            name = t.getName()
            if name.startswith('ThreadPoolExecutor'):   # 忽略子线程
                continue
            util.output(t.getName(), t.isAlive())