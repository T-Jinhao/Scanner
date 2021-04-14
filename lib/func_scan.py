#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import re
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from modules.func import util
from .color_output import *
from .load_config import Config
from reports import reports_xlsx,reports_txt

wrong_web_list = ['javascript:void(0)', None, '###', '#']

class Scan():
    def __init__(self, url, REQ, name, crazy):
        self.url = url
        self.REQ = REQ
        self.name = name
        self.crazy = crazy
        self.Phone = []
        self.Email = []
        self.ICP = []
        self.Output = ColorOutput()

    def load_config(self):
        config = Config().readConfig()
        self.timeout = config.getfloat("Scan", "timeout")
        self.threads = config.getint("Scan", "threads")
        self.ICPUrl = config.get("Scan", "ICPUrl")
        self.checkWebStatus = config.getboolean("Scan", "checkWebStatus")
        self.checkJsStatus = config.getboolean("Scan", "checkJsStatus")
        system = platform.system()
        self.saveType = config.get("Result", system)

    def start(self):
        print(self.Output.fuchsia(">>>>>scan" + "-" * 40))
        self.load_config()
        print(self.Output.blue('[ schedule ] ') + self.Output.fuchsia('开始爬取网页链接:') + self.url)
        web, js = self.scan(self.url)
        if web:   # 检测爬取链接的存活性
            if self.checkWebStatus:
                web += self.crazyRun(web)
                res = self.statusCheck(web)
                self.saveResult(res, sheetname='webScan', txtFilename='webScan_report.txt', cut=' | ')
            else:
                print(self.Output.blue('[ Setting ] ') + self.Output.fuchsia('checkWebStatus ')
                      + self.Output.yellow(self.checkWebStatus))
                for x in web:
                    print(self.Output.green('[ webURL ] ') + x)
                self.saveResult(web, sheetname='webScanWithoutCheck', txtFilename='webScanWithoutCheck_report.txt', cut=' | ').save()
        else:
            print(self.Output.blue('[ result ] ') + self.Output.yellow('没有扫描到网站链接'))

        if js and self.checkJsStatus:    # 寻找js文件内的中文字符
            print(self.Output.blue('[ schedule ] ') + self.Output.cyan('JS文件分析'))
            for u in js:
                self.js_analysis(u)    # 寻找敏感信息

        if self.Phone != []:
            print()
            print(self.Output.green('[ output ] ') + self.Output.cyan('手机号码'))
            for x in self.Phone:
                print(self.Output.blue('[ result ] ') + self.Output.green(x))
            self.saveResult(self.Phone, 'phone', 'phone.txt', cut=' | ')
        if self.Email != []:
            print()
            print(self.Output.green('[ output ] ') + self.Output.cyan('邮箱'))
            for x in self.Email:
                print(self.Output.blue('[ result ] ') + self.Output.green(x))
            self.saveResult(self.Email, 'email', 'email.txt', cut=' | ')
        if self.ICP != []:
            print()
            print(self.Output.green('[ output ] ') + self.Output.cyan('备案号'))
            for x in self.ICP:
                print(self.Output.blue('[ result ] ') + self.Output.green(x))
                # 暂不启用
                # data = {
                #     'pageNo': 1,
                #     'pageSize': 20,
                #     'Kw': x.split('-')[0]
                # }
                # r = self.REQ.autoPostAccess(url=self.ICPUrl, data=data)
                # print(r.text)
            self.saveResult(self.ICP, 'icp', 'icp.txt', cut=' | ')
        print(self.Output.fuchsia("-" * 40 + "<<<<<scan" + "\n"))
        return

    def saveResult(self, report, sheetname='', txtFilename='', cut=':'):
        if report == []:
            print(self.Output.blue('[ result ] ') + self.Output.yellow("[ {}扫描结果为空 ]".format(sheetname)))
            return
        if self.saveType == 'xlsx':
            if sheetname == 'webScan':
                banner = ['状态码', '文本长度', '标题', 'URL']
            elif sheetname == 'webScanWithoutCheck':
                banner = ['URL']
            elif sheetname == 'phone':
                banner = ['手机号码', '捕获页面']
            elif sheetname == 'email':
                banner = ['邮箱', '捕获页面']
            elif sheetname == 'icp':
                banner = ['备案号', '捕获页面']
            else:
                banner = []
            reports_xlsx.Report(report, self.name, sheetname, banner, cut=cut).save()
        else:
            reports_txt.Report(report, self.name, txtFilename, '网页扫描报告已存放于', '并没有扫描出网页链接').save()


    def crazyRun(self,urls):
        '''
        递归各相对路径，尝试找出可疑的302等页面
        :param urls:
        :return:
        '''
        paths = []
        http = re.compile('http')
        for u in urls:
            if http.match(u):  # 属于完整链接
                pass
            else:
                u = u.lstrip('.')  # 除去左端点号
                u = u.lstrip('/')  # 除去左端/号
                for p in range(u.count('/')):
                    x = u.rsplit('/', p + 1)[0]
                    if x not in paths:
                        paths.append(x)
        # color_output(paths)
        return paths


    def url_check(self, url, u):
        '''
        检测url完整性，返回绝对地址
        :param url: 当前扫描的页面url
        :param u: 获取到的url
        :return:
        '''
        err = ['', None, '/', '\n']
        if u in err:
            return
        if re.match("(http|https)://.*", u):  # 匹配绝对地址
            return u
        else:     # 拼凑相对地址，转换成绝对地址
            u = urljoin(url, u)
            return u


    def scan(self, url):
        '''
        爬取当前页面的URL
        :return:网站相关链接
        '''
        try:
            res = self.REQ.autoGetAccess(url, threads=self.threads, timeout=self.timeout)
            self.match_Email(res.text, url)   # 匹配邮箱
            self.match_Phone(res.text, url)   # 匹配电话
            self.match_ICP(res.content.decode('utf-8'), url)   # 匹配备案号
            web_sites = []  # 网站链接
            js_sites = []  # js脚本链接
            soup = BeautifulSoup(res.text, 'html.parser')
            web_links = soup.find_all('a')
            js_links = soup.find_all('script')
            for j in web_links:
                y = j.get('href')  # 提取href后的链接
                if y != None and y not in wrong_web_list:
                    u = self.url_check(url, y)
                    if u != None:
                        web_sites.append(u)  # 处理获取到的url
            for k in js_links:
                z = k.get('src')
                if z != None:
                    u = self.url_check(url, z)
                    if u != None:
                        js_sites.append(u)
            if not web_sites:
                web_sites = ''
            if not js_sites:
                js_sites = ''
            return web_sites, js_sites

        except Exception as e:
            # color_output(e, color='RED')
            print(self.Output.red('[ Error ] ') + self.Output.yellow('网站访问出现点问题了...'))
            sys.exit(1)



    def statusCheck(self,urls):
        '''
        测试链接是否可用
        :param urls: 爬取到的url
        :return:
        '''
        result = []
        for url in list(set(urls)):
            print()
            print(self.Output.fuchsia('[ Test ]') + url)
            try:
                res = self.REQ.autoGetAccess(url, threads=self.threads, timeout=self.timeout)
                title = util.getTitle(res.text)
                print(self.Output.green('[ Info ] ')
                      + self.Output.fuchsia('状态码') + self.Output.green(res.status_code) + self.Output.interval()
                      + self.Output.fuchsia('文本长度') + self.Output.green(len(res.content)) + self.Output.interval()
                      + self.Output.fuchsia('标题') + self.Output.green(title)
                      )
                if res.status_code != 404 and len(res.content) != 0:
                    msg = " | ".join([str(res.status_code), str(len(res.content)), str(title), url])
                    result.append(msg)
            except:
                print(self.Output.green('[ Info ] ') + self.Output.yellow('访问失败'))
            time.sleep(0.5)   # 防止过于频繁导致网站崩溃
        return result

    def js_analysis(self, url):
        '''
        找出js文件内的中文字符
        :return:
        '''
        compile_CN = re.compile(u"[\u4e00-\u9fa5]")   # 匹配中文
        print()
        print(self.Output.fuchsia('[ Scan ] ') + url)
        try:
            res = self.REQ.autoGetAccess(url, threads=self.threads, timeout=self.timeout)
            content = str(res.content.decode('utf-8'))
            self.match_Phone(res.text, url)
            self.match_Email(res.text, url)
            self.reg_str(res.text)
            ret = compile_CN.findall(content)
            if ret != []:
                print(self.Output.green('[ output ] ') + self.Output.cyan('文件中文爬取'))
                ret = ''.join(ret)
                print(self.Output.blue('[ result ] ') + self.Output.green(ret))
        except Exception:
            pass
        return

    def match_Phone(self, text, url):
        '''
        匹配手机号码
        :param text:
        :return:
        '''
        compile_Phone = re.compile(r'1[3456789]\d{9}')
        ret = compile_Phone.findall(text)
        if ret != []:
            for x in ret:
                if x not in self.Phone:
                    p = " | ".join([str(x), url])
                    self.Phone.append(p)
        return

    def match_ICP(self, text, url):
        '''
        匹配ICP备案号
        :param text:
        :return:
        '''
        compile_ICP = re.compile("([\u4e00-\u9fa5]ICP备\d{8}号-([0-9]|10))")
        ret = compile_ICP.search(text)
        try:
            if ret != None and ret[0] not in self.ICP and ret[0] != []:
                i = " | ".join([ret[0], url])
                self.ICP.append(i)
        except:
            pass
        return

    def match_Email(self, text, url):
        '''
        匹配邮箱
        :param content:
        :return:
        '''
        compile_Email = re.compile(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]{0,4}')
        ret = compile_Email.findall(text)
        if ret != []:
            for x in ret:
                if x not in self.Email and x.split('.')[-1] != 'png':
                    e = " | ".join([x, url])
                    self.Email.append(e)
        return

    def reg_str(self, text):
        '''
        匹配js中的链接
        感谢：https://github.com/GerbenJavado/LinkFinder
        :param text: 页面
        :return:
        '''
        resultUrls = []
        regex_str = r"""
                      (?:"|')                               # Start newline delimiter
                      (
                        ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
                        [^"'/]{1,}\.                        # Match a domainname (any character + dot)
                        [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path
                        |
                        ((?:/|\.\./|\./)                    # Start with /,../,./
                        [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
                        [^"'><,;|()]{1,})                   # Rest of the characters can't be
                        |
                        ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
                        [a-zA-Z0-9_\-/]{1,}                 # Resource name
                        \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
                        (?:[\?|/][^"|']{0,}|))              # ? mark with parameters
                        |
                        ([a-zA-Z0-9_\-]{1,}                 # filename
                        \.(?:php|asp|aspx|jsp|json|
                             action|html|js|txt|xml)             # . + extension
                        (?:\?[^"|']{0,}|))                  # ? mark with parameters
                      )
                      (?:"|')                               # End newline delimiter
                    """
        compile_str = re.compile(regex_str, re.VERBOSE)
        ret = compile_str.findall(text)
        if ret != []:
            print(self.Output.green('[ output ] ') + self.Output.cyan('JS链接爬取结果'))
            for x in ret:
                for m in x:
                    u = self.url_check(self.url, m)
                    if u not in resultUrls and u:
                        print(self.Output.green('[ result_js ] ') + u)
                        resultUrls.append(u)



class celery_scan:
    '''
    celery调用模块
    返回新的url进行递归扫描
    '''
    def __init__(self,url,REQ,name):
        self.url =url
        self.REQ = REQ
        self.name = name

    def run(self):
        res = Scan(self.url, self.REQ, self.name, '1')
        new_url = self.same_check(res)
        return new_url

    def same_check(self,res):
        '''
        url相似度的检测
        :param res:爬取的url集
        :return: 同源的url
        '''
        return res
