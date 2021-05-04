#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao

import re
from modules.handle.baseModel import BaseModel
from modules.func import util

class Terminal(BaseModel):
    async def filter(self, resp, url=''):
        if resp == None:
            return
        text = resp.text
        rurl = str(resp.url)
        self.js_analysis(text, rurl)
        self.reg_str(text, rurl)
        if self.isShow:
            print()

    def reg_str(self, text, rurl):
        '''
        匹配js中的链接
        感谢：https://github.com/GerbenJavado/LinkFinder
        :param text: 页面
        :param rurl: 原始页面
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
            if self.isShow:
                print(self.Output.fuchsia('[ Scan ] ') + self.Output.cyan('JS链接爬取: ') + rurl)
            for x in ret:
                for m in x:
                    u = util.splicingUrl(rurl, m)
                    if u not in resultUrls and u:
                        if self.isShow:
                            print(self.Output.green('[ result_js ] ') + u)
                        resultUrls.append(u)

    def js_analysis(self, text, url):
        '''
        找出js文件内的中文字符
        :return:
        '''
        self.match_Phone(text, url)
        self.match_Email(text, url)
        if self.isShow:   # 线程运行不调用此处
            print(self.Output.fuchsia('[ Scan ] ') + url)
            compile_CN = re.compile(u"[\u4e00-\u9fa5]")
            # 匹配中文
            try:
                ret = compile_CN.findall(text)
                if ret != []:
                    print(self.Output.green('[ output ] ') + self.Output.cyan('文件中文爬取'))
                    ret = ''.join(ret)
                    print(self.Output.blue('[ result ] ') + self.Output.green(ret))
            except Exception as e:
                print(e)
        return