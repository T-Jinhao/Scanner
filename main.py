#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import argparse,sys,os
import re
import requests
from urllib import parse
import socket
import func_spider,func_scan,func_ports

class Scanner():
    def __init__(self):
        self.info = self.terminal_input()
        self.parser_dump()         # 自动解析参数
        self.url_check(self.opt['url'])           # 检查url合法性
        self.run()


    def terminal_input(self):
        '''
        接收命令行参数
        :return: 解析后的参数键值对
        '''
        ter_opt={}
        if len(sys.argv) == 1:
            sys.argv.append('-h')
        parser = argparse.ArgumentParser(description='简易扫描器，<>内为开启极致模式的简述',add_help=True)
        parser.add_argument('-u','--url',help='扫描对象的url')
        parser.add_argument('-R', '--crazy', help='以极致模式启动功能，比较耗时', action='store_true')
        parser.add_argument('-S','--spider',help='爬取网站上的网页链接<递归爬取网站中url的url>',action='store_true')
        parser.add_argument('-B','--burp',help='爆破网站目录<附带超大payload>',action='store_true')
        parser.add_argument('-P','--ports',help='探测目标主机开放端口<支持自定义端口范围>',action='store_true')
        parser.add_argument('--sqlscan',help='网站SQL注入检测',action='store_true')
        parser.add_argument('--cookies', default=None, help='目标网站的cookies')
        parser.add_argument('--threads', default=20, help='脚本启动线程数<50>', type=int)
        args = parser.parse_args()
        for x, y in args._get_kwargs():
            ter_opt[x] = y    # 保存为键值对
        return ter_opt


    def parser_dump(self):
        '''
        自动把参数添加进dict
        :return:
        '''
        self.opt={}
        for x in self.info:
            # print(x)
            self.opt[x] = self.info[x]
            # print(self.opt[x])


    def url_check(self,url):
        '''
        很随意的URL合理性检测
        :param url: 待检测的URL
        :return: bool值
        '''
        if re.match('(http|https)://(.*?)\.(.*)',url):     # 匹配以http|https开头的网站
            return
        elif re.match('(.*?)\.(.*)',url):                  # 匹配xxx.xxx...规则的网站
            self.opt['url'] = "http://"+url                # 添加协议头
            return
        else:
            print("URL格式出错!")
            sys.exit(1)

    def base_search(self):
        name = parse.urlparse(self.opt['url']).hostname
        self.opt['host'] = socket.gethostbyname(name)


    def base_report(self):
        print('>>>>>base_report'+'-'*40)
        self.base_search()
        for i in self.opt:
            if self.opt[i]:
                print("[ {0} : {1} ]".format(i,self.opt[i]))
        print('-'*40+'<<<<<base_report'+'\n')


    def run(self):
        '''
        调用模块
        :return:
        '''
        if self.opt['crazy'] and self.opt['threads'] < 50:
            self.opt['threads'] = 50
        self.base_report()
        if self.opt['spider']:
            func_spider.Spider(self.opt['url'],self.opt['cookies'],self.opt['threads'],self.opt['crazy'])
        if self.opt['scan']:
            func_scan.Scan(self.opt['url'],self.opt['cookies'],self.opt['threads'],self.opt['crazy'])
        if self.opt['ports']:
            func_ports.Ports(self.opt['host'],self.opt['threads'],self.opt['crazy'])
        else:
            # print("Nothing to do...")
            pass






def main():
    x = Scanner()

if __name__ == "__main__":
    main()
