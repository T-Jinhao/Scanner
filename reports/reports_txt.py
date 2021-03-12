#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import os
from lib.color_output import *

class Report:
    def __init__(self,reports,taskname,filename,suc_msg,err_msg):
        self.reports = reports
        self.dirname = taskname
        self.filename = filename
        self.suc_msg = suc_msg
        self.err_msg = err_msg
        self.Output = ColorOutput()


    def save(self):
        '''
        保存记录
        :return:
        '''
        path = os.path.dirname(__file__)
        os.chdir(path)
        filepath = "./{}/{}".format(self.dirname,self.filename)
        if not os.path.exists(self.dirname):
            os.mkdir(self.dirname)
        with open(filepath, 'a', encoding='utf-8') as F:
            try:
                for m in self.reports:
                    F.write(m + '\n')
                msg = "[ {}：{}]".format(self.suc_msg, filepath)
            except Exception as e:
                # print(e)
                msg = "[ {} ]".format(self.err_msg)
        print(self.Output.green('[ 保存输出结果-text ] ') + self.Output.cyan(msg))
        return

