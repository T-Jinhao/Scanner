#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import threading
from interactive.run import common
from lib import func_domain
from interactive.funcs import util

class domain(common.Common):
    def run(self, Info, p_list, isThread=False, isShow=True):
        # 设置参数
        payloads = p_list['payloads']
        flag = self.getFlag(Info['Online'][1])
        report = []
        r = func_domain.Domain(
            url=Info['Url'][1],
            payload=payloads,
            name=Info['Taskname'][1],
            flag=flag
        )
        domain = r.url_check(Info['Url'][1])   # 提取域名
        if domain == None:
            util.printError('subdomain model is not support for Ip.')
            return
        r.load_config()
        r.threads = int(Info['Workers'][1])
        r.timeout = float(Info['Timeout'][1])
        r.isThread = isThread
        r.isShow = isShow
        # 运行
        r.panAnalysis(domain)  # 分析泛解析
        if flag == 1:
            report = r.onlineMethod(domain)
        if report == []:
            urls = ['{}.{}'.format(x, domain) for x in payloads]
            report = r.run(payload=urls)
        ip_list = r.IP_list
        r.saveDomainResult(report=report)
        r.saveIpResult(report_dict=ip_list)

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