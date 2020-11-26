#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import os
from lib.color_output import color_output

class Report:
    def __init__(self,reports,taskname,filename,suc_msg,err_msg):
        self.reports = reports
        # ipsite = re.compile("[\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3}")
        # if ipsite.match(dirname):
        #     self.dirname = dirname
        # else:
        #     dir = urlparse(dirname).netloc
        #     self.dirname = dir.replace(':','_')
        self.dirname = taskname
        self.filename = filename
        self.suc_msg = suc_msg
        self.err_msg = err_msg


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
        with open(filepath, 'a') as F:
            try:
                for m in self.reports:
                    F.write(m + '\n')
                msg = "[ {}：{}]".format(self.suc_msg,filepath)
            except:
                msg = "[ {} ]".format(self.err_msg)
        color_output(msg, color='GREEN')
        return

