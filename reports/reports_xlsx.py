#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import os
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from lib.color_output import *

class Report:
    def __init__(self, report, taskname, sheetname, suc_msg, err_msg):
        '''
        保存xlsx格式的结果
        :param report: 报告内容，list
        :param taskname: 任务名兼文本名
        :param sheetname: xlsx工作台名称，用作分页
        :param suc_msg: 保存成功输出文本
        :param err_msg: 保存失败输出文本
        '''
        self.report = report
        self.taskname = taskname

    def save(self):
        file = self.getAbsolutePath(self.taskname)
        print(file)

    def getAbsolutePath(self, taskname, ext='.xlsx'):
        '''
        返回要读写文件的绝对路径
        :param taskname:
        :return:
        '''
        path = os.path.abspath(os.path.dirname(__file__))
        if platform.system() == 'Windows':
            interval = '\\'
        else:
            interval = '/'
        file = interval.join([path, taskname+ext])
        return file



if __name__ == '__main__':
    x = Report([], 'test')
    x.save()



