#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao

import sys
from modules.handle.baseModel import BaseModel
from modules.func import util

class Terminal(BaseModel):
    async def filter(self, resp, url=''):
        if resp == None:
            return
        flag = True
        # 泛解析处理
        if self.scanmode:
            flag = False
            try:
                title = util.getTitle(resp.text).strip()
                if title not in self.title_list:  # 判断重复标题
                    self.title_list.append(title)
                    flag = True
                elif resp.content_length not in self.length_list:  # 判断重复文本
                    self.length_list.append(resp.content_length)
                    flag = True
            except:
                pass
        # 输出
        if flag == True:
            try:
                title = util.getTitle(resp.text).strip()
                msg = {
                    'status_code': resp.status,
                    'protourl': resp.protourl,
                    'title': title,
                    'ip': resp.ip,
                    'url': resp.url,
                    'content_length': resp.content_length
                }
                if self.isShow:
                    output = "".join([
                        self.Output.green('[ result ] '), self.Output.fuchsia('status_code:'),
                        self.Output.green(resp.status), self.Output.interval(),
                        self.Output.fuchsia('初始URL:'), self.Output.green(resp.protourl), self.Output.interval(),
                        self.Output.fuchsia('标题:'), self.Output.green(title), self.Output.interval(),
                        self.Output.fuchsia('最终URL:'), str(resp.url),
                    ])
                    print(output)
                    # sys.stdout.flush()
                if resp.ip is not None:
                    if resp.ip not in self.IP_list:
                        self.IP_list[resp.ip] = 1
                    else:
                        self.IP_list[resp.ip] += 1
                return msg.copy()
            except:
                pass