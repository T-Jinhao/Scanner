#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao

import sys
from modules.terminal.baseModel import BaseModel
from modules.func import util

class Terminal(BaseModel):
    async def filter(self, resp, url=''):
        if resp == None:
            return
        if self.scanmode:   # 泛解析处理
            print('pan')
        else:
            try:
                title = util.getTitle(resp.text).replace(' | ', ' || ')
                msg = "{status} | {protourl} | {title} | {ip} | {url}".format(
                    status=resp.status,
                    protourl=resp.protourl,
                    title=title,
                    ip=resp.ip,
                    url=resp.url
                )
                output = "".join([
                    self.Output.green('[ result ] '), self.Output.fuchsia('status_code:'),
                    self.Output.green(resp.status), self.Output.interval(),
                    self.Output.fuchsia('初始URL:'), self.Output.green(resp.protourl), self.Output.interval(),
                    self.Output.fuchsia('标题:'), self.Output.green(title), self.Output.interval(),
                    self.Output.fuchsia('最终URL:'), str(resp.url),
                ])
                if resp.ip is not None:
                    if resp.ip not in self.IP_list:
                        self.IP_list[resp.ip] = 1
                    else:
                        self.IP_list[resp.ip] += 1
                print(output)
                # sys.stdout.flush()
                return msg
            except:
                pass