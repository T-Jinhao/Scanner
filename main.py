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
from modules import _requests
from modules import check

class Scanner():
    def __init__(self, args):
        self.args = args


    def url_check(self):
        '''
        很随意的URL合理性检测
        :return: bool值
        '''
        url = self.args.url.split('#')[0]
        if re.match('(http|https)://(.*?)\.(.*)',url):     # 匹配以http|https开头的网站
            return
        elif re.match('(.*?)\.(.*)',url):                  # 匹配xxx.xxx...规则的网站
            self.args.url = "http://"+url                # 添加协议头
            return
        else:
            print("URL格式出错!")
            sys.exit(1)

    def getHostname(self):
        try:
            name = parse.urlparse(self.args.url).hostname
            host = socket.gethostbyname(name)
        except:
            netloc = 'www.{}'.format(urlparse(self.args.url).netloc)
            name = netloc
            host = socket.gethostbyname(name)
        return host


    def base_report(self):
        self.host = self.getHostname()  # 获取domain
        self.ip_report = func_base.IPcontent(self.host).run()
        print('>>>>>base_report'+'-'*40)
        # print(self.args)
        print("\nIP域名绑定情况 : {}".format(self.host))
        try:
            for x in self.ip_report:
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


    def prepare(self):
        '''
        启动前进行的检查与设置工作
        :return:
        '''
        O = check.O()  # 创建检查对象
        self.threads = O.threadSetting(self.args.threads, self.args.crazy)
        self.payload_file = O.fileRead(self.args.file)

        timeout = O.timeoutSetting(self.args.timeout)
        cookies = O.checkCookies(self.args.cookies)
        self.REQ = _requests.URL(
            cookies=cookies,
            timeout=timeout,
            proxies={}
        )
        return

    def run(self):
        '''
        调用模块
        :return:
        '''
        if self.args.celery:   # 使用celery分发任务
            thread = threading.Thread(target=self.start_celery)
            thread.start()
            time.sleep(15)  # 等待充分启动celery
            celery_run.RC(self.args)
            return
        if self.args.spider:
            func_spider.Spider(self.opt['url'],self.parseCookie(self.opt['cookies']),self.opt['crazy'])
        if self.args.ports:
            func_ports.Ports(self.opt['host'], self.opt['threads'], self.opt['crazy'])
        if self.args.hosts:
            func_hosts.Hosts(self.opt['host'],self.opt['threads'])
        if self.args.login:
            func_login.Login(self.opt['url'],self.opt['file'],self.opt['threads'],self.opt['crazy'])
        if self.args.burp:
            func_burp.Burp(self.opt['url'],self.opt['file'],self.parseCookie(self.opt['cookies']),self.opt['threads'],self.opt['crazy'])
        if self.args.domain:
            func_domain.Domain(self.opt['url'],self.opt['file'],self.opt['threads'],self.opt['crazy'])
        if self.args.sqlscan:
            func_sqli.Sql(self.opt['url'],self.opt['crazy'])
        else:
            # print("Nothing to do...")
            sys.exit()


def terminal_input():
    '''
    接收命令行参数
    :return: 解析后的参数键值对
    '''
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
    parser.add_argument('-T','--timeout',help='超时时间',default=3,type=int)
    parser.add_argument('--celery',help='使用celery分布管理',action='store_true')
    parser.add_argument('--cookies', default=None, help='目标网站的cookies')
    parser.add_argument('--threads', default=5, help='脚本启动线程数 <20>', type=int)
    args = parser.parse_args()
    return args


def main():
    args = terminal_input()
    x = Scanner(args)
    x.url_check()  # 检查输入url
    x.base_report()  # 输出基础报告
    x.prepare()    # 准备工作

if __name__ == "__main__":
    main()
