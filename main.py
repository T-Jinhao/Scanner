#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import grequests   # 入口文件必须添加，防止monkey报错
import argparse
import sys
import os
import re
import threading
import time
import datetime
from urllib import parse
from urllib.parse import urlparse
import socket
from lib import func_sqli,func_hosts,func_domain,func_ports,func_burp,func_scan,func_login
from lib import celery_run,func_base,load_config
from modules import _requests
from modules import check
from lib.color_output import *


class Scanner():
    def __init__(self, args):
        self.args = args
        self.Output = ColorOutput()

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
            print(self.Output.red("[ Error ] ")+ self.Output.cyan('URL格式出错!'))
            sys.exit(1)

    def getHostname(self):
        try:
            name = parse.urlparse(self.args.url).hostname
            host = socket.gethostbyname(name)
            return host
        except:
            pass
        try:
            netloc = 'www.{}'.format(urlparse(self.args.url).netloc)
            name = netloc
            host = socket.gethostbyname(name)
            return host
        except Exception:
            print(self.Output.red('[ Error ] ') + self.Output.cyan("{}:该域名未查询到绑定IP".format(self.args.url)))
            exit(0)



    def base_report(self):
        self.host = self.getHostname()  # 获取domain
        print(self.Output.fuchsia('>>>>>base_report'+'-'*40))
        print(self.Output.green('[ 输入URL ] ') + self.Output.white(self.args.url))
        print(self.Output.green('[ 解析host ] ') + self.host)
        print(self.Output.green('[ 任务命名 ] ') + self.taskname)
        config = Config().readConfig()
        showIP = config.getboolean("Main", "ip_report")
        if showIP:
            ip_report = func_base.IPcontent(self.host, self.REQ).run()
            print(self.Output.green('[ IP域名绑定情况 ] '))
            try:
                for x in ip_report:
                    print(x)
            except:
                pass
        try:
            cdn_report = func_base.CDNcontent(self.args.url).run()
            if cdn_report != []:
                print(self.Output.green('[ CDN情况 ] '))
                for m in cdn_report:
                    print(m)
        except:
            pass
        print(self.Output.fuchsia('-'*40+'<<<<<base_report'+'\n'))

    def start_celery(self):
        '''
        启动celery服务
        :return:
        '''
        cmd = 'celery -A lib.func_celery worker --pool=eventlet -l DEBUG'    # 指定工作者
        os.system(cmd)

    def setTaskname(self):
        if self.args.name != None:
            self.taskname = self.args.name
        else:
            ip = re.compile('[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}')
            netloc = urlparse(self.args.url).netloc
            res = ip.match(netloc)
            if res:    # ip形式的名称，需要改名
                today = datetime.datetime.today()
                formatted_today = today.strftime('%y%m%d')
                self.name = formatted_today
            else:
                n = netloc.split(".")
                if len(n) == 2:
                    self.taskname = n[0]
                elif n[-2] not in ["com", "edu", "ac", "net", "org", "gov"]:  # 带地域标签的域名
                    self.taskname = n[-2]
                else:
                    self.taskname = n[-3]
        return


    def prepare(self):
        '''
        启动前进行的检查与设置工作
        :return:
        '''
        O = check.Check()  # 创建检查对象
        # 导入各模块payload
        self.bPayload = O.fileRead(self.args.bfile)
        self.dPayload = O.fileRead(self.args.dfile)
        self.lPayload = O.fileRead(self.args.lfile)
        # self.payload = O.fileRead(self.args.file)

        # 设置基础请求体
        self.cookies = O.checkCookies(self.args.cookies)
        self.REQ = _requests.Concurrent(
            cookies=self.cookies,
        )


        # 解析配置文件
        config = load_config.Config().readConfig()
        recursion = config.getint("Main", "recursion")
        O.recursionSetting(recursion)   # 设置最大递归深度
        return

    def run(self):
        '''
        调用模块
        :return:
        '''
        # 使用celery分发任务
        if self.args.celery:
            thread = threading.Thread(target=self.start_celery)
            thread.start()
            time.sleep(15)  # 等待充分启动celery
            config = load_config.Config().readConfig()
            threads = config.getint("Celery", "threads")
            timeout = config.getfloat("Celery", "timeout")
            c = celery_run.RC(
                args=self.args,
                REQ=self.REQ,
                bPayload=self.bPayload,
                dPayload=self.dPayload,
                lPayload=self.lPayload,
                host=self.host,
                name=self.taskname
            )
            c.start()
            return

        if self.args.scan:
            func_scan.Scan(self.args.url, self.REQ, self.taskname, self.args.crazy).start()
        if self.args.ports:
            func_ports.Ports(self.host, self.taskname, self.args.crazy).start()
        if self.args.hosts:
            func_hosts.Hosts(self.host, self.taskname).start()
        if self.args.login:
            func_login.Login(self.args.url, self.REQ, self.lPayload, self.taskname, self.args.crazy).start()
        if self.args.burp:
            func_burp.Burp(self.args.url, self.bPayload, self.REQ, self.taskname, self.args.crazy).start()
        if self.args.domain:
            func_domain.Domain(self.args.url, self.dPayload, self.REQ, self.taskname, self.args.crazy).start()
        if self.args.sqlscan:
            func_sqli.Sql(self.args.url, self.taskname, self.args.crazy).start()
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
    parser.add_argument('-u','--url', help='扫描对象的url')
    parser.add_argument('-i', '--interactive', help='交互式控制台', action='store_true')
    parser.add_argument('-n','--name', help='保存结果文本命名', default=None)
    parser.add_argument('-X', '--crazy', help='以极致模式启动功能，比较耗时', action='store_true')
    parser.add_argument('-P', '--ports', help='探测目标主机开放端口[-X]<支持自定义端口范围>', action='store_true')
    parser.add_argument('-H','--hosts', help='探测存活主机', action='store_true')
    parser.add_argument('-S','--scan', help='爬取页面的网页链接并分析 [--cookie]<js文件分析>', action='store_true')
    parser.add_argument('-L','--login', help='测试网站密码缺陷[-F,-T]<测试弱密码>', action='store_true')
    parser.add_argument('-B','--burp', help='爆破网站目录[-F,-X,-T]<附加超大payload>', action='store_true')
    parser.add_argument('-D','--domain',help='挖掘网站子域名[-F,-X]<更多线程更多payload>', action='store_true')
    parser.add_argument('-bF', '--bfile', default=None, help='Burp模块自定义payload文件')
    parser.add_argument('-dF', '--dfile', default=None, help='Domain模块自定义payload文件')
    parser.add_argument('-lF', '--lfile', default=None, help='Login模块自定义payload文件')
    parser.add_argument('-I','--sqlscan', help='网站SQL注入fuzz检测[-X]<sqlmapapi爆破>', action='store_true')
    parser.add_argument('--celery', help='使用celery分布管理', action='store_true')
    parser.add_argument('--cookies', default=None, help='目标网站的cookies')
    args = parser.parse_args()
    return args


def main():
    args = terminal_input()
    if args.interactive:   # 控制台模式
        print('xxx')
    else:
        x = Scanner(args)
        x.url_check()  # 检查输入url
        x.setTaskname()
        x.prepare()  # 准备工作
        x.base_report()  # 输出基础报告
        x.run()

if __name__ == "__main__":
    main()
