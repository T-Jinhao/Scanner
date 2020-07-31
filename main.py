#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import argparse,sys,os
import re
import threading,time
from urllib import parse
from urllib.parse import urlparse
import socket
from lib import func_sqli,func_hosts,func_domain,func_ports,func_burp,func_spider,func_login
from lib import celery_run,func_base

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
        parser = argparse.ArgumentParser(description='简易扫描器，[]内为可用功能模块，<>内为开启极致模式的简述',add_help=True)
        parser.add_argument('-u','--url',help='扫描对象的url')
        parser.add_argument('-X', '--crazy', help='以极致模式启动功能，比较耗时', action='store_true')
        parser.add_argument('-P', '--ports', help='探测目标主机开放端口[-X]<支持自定义端口范围>', action='store_true')
        parser.add_argument('-H','--hosts',help='探测存活主机',action='store_true')
        parser.add_argument('-S','--spider',help='爬取网站上的网页链接 [--cookie]<分解路径测试>',action='store_true')
        parser.add_argument('-L','--login',help='测试网站密码缺陷[-F]<测试弱密码>',action='store_true')
        parser.add_argument('-B','--burp',help='爆破网站目录[-F,-X]<附加超大payload>',action='store_true')
        parser.add_argument('-D','--domain',help='挖掘网站子域名[-F,-X,--threads]<更多线程更多payload>',action='store_true')
        parser.add_argument('-F', '--file', default=None, help='可自定义payload文件')
        parser.add_argument('-I','--sqlscan',help='网站SQL注入fuzz检测[-X]<sqlmapapi爆破>',action='store_true')
        parser.add_argument('--celery',help='使用celery分布管理',action='store_true')
        parser.add_argument('--cookies', default=None, help='目标网站的cookies')
        parser.add_argument('--threads', default=5, help='脚本启动线程数 <20>', type=int)
        self.args = parser.parse_args()
        for x, y in self.args._get_kwargs():
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
        url = url.split('#')[0]
        if re.match('(http|https)://(.*?)\.(.*)',url):     # 匹配以http|https开头的网站
            return
        elif re.match('(.*?)\.(.*)',url):                  # 匹配xxx.xxx...规则的网站
            self.opt['url'] = "http://"+url                # 添加协议头
            return
        else:
            print("URL格式出错!")
            sys.exit(1)

    def base_search(self):
        try:
            name = parse.urlparse(self.opt['url']).hostname
            self.opt['host'] = socket.gethostbyname(name)
        except:
            netloc = 'www.{}'.format(urlparse(self.opt['url']).netloc)
            name = netloc
            self.opt['host'] = socket.gethostbyname(name)


    def base_report(self):
        print('>>>>>base_report'+'-'*40)
        self.base_search()
        for i in self.opt:
            if self.opt[i]:
                print("[ {0} : {1} ]".format(i,self.opt[i]))
        print("\nIP域名绑定情况 : {}".format(self.opt['host']))
        try:
            mes = func_base.IPcontent(self.opt['host']).run()
            for x in mes:
                print("{} : {}".format(x[0], x[1]))
        except:
            pass
        print('-'*40+'<<<<<base_report'+'\n')

    def start_celery(self):
        '''
        启动celery服务
        :return:
        '''
        cmd = 'celery -A lib.func_celery worker --pool=eventlet -l DEBUG'    # 指定工作者
        os.system(cmd)


    def parseCookie(self, cookie):
        if cookie == None:
            return
        cookies = {}  # 初始化cookies字典变量
        for x in cookie.split(';'):  # 按照字符：进行划分读取
            name, value = x.strip().split('=', 1)
            cookies[name] = value  # 为字典cookies添加内容
        return cookies

    def run(self):
        '''
        调用模块
        :return:
        '''
        if self.opt['crazy'] and self.opt['threads'] < 20:
            self.opt['threads'] = 20
        self.base_report()
        if self.opt['celery']:
            thread = threading.Thread(target=self.start_celery)
            thread.start()
            time.sleep(15)  # 等待充分启动celery
            celery_run.RC(self.args)
            return
        if self.opt['spider']:
            func_spider.Spider(self.opt['url'],self.parseCookie(self.opt['cookies']),self.opt['crazy'])
        if self.opt['ports']:
            func_ports.Ports(self.opt['host'], self.opt['threads'], self.opt['crazy'])
        if self.opt['hosts']:
            func_hosts.Hosts(self.opt['host'],self.opt['threads'])
        if self.opt['login']:
            func_login.Login(self.opt['url'],self.opt['file'],self.opt['threads'],self.opt['crazy'])
        if self.opt['burp']:
            func_burp.Burp(self.opt['url'],self.opt['file'],self.parseCookie(self.opt['cookies']),self.opt['threads'],self.opt['crazy'])
        if self.opt['domain']:
            func_domain.Domain(self.opt['url'],self.opt['file'],self.opt['threads'],self.opt['crazy'])
        if self.opt['sqlscan']:
            func_sqli.Sql(self.opt['url'],self.opt['crazy'])
        else:
            # print("Nothing to do...")
            sys.exit()



def main():
    x = Scanner()

if __name__ == "__main__":
    main()
