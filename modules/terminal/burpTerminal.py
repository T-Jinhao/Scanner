#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao

from modules.terminal import baseModel
from lib.color_output import ColorOutput
from modules.func import util

class Terminal(baseModel):
    def __init__(self):
        self.Output = ColorOutput()

    def filter(self, resp):
        if resp == None:
            return
        if resp.status in [200, 302, 500, 502, 403]:   # 仅需要这几个端口
            title = util.getTitle(resp.text)
            print(self.Output.green('[ result ] ')
                  + self.Output.fuchsia('status_code:') + self.Output.green(resp.status) + self.Output.interval()
                  + self.Output.fuchsia('url:') + resp.url + self.Output.interval()
                  + self.Output.fuchsia('Content-Length:') + self.Output.green(resp.content_length)
                  + self.Output.interval()
                  + self.Output.fuchsia('title:') + self.Output.green(title))
            msg = "{status} : {len} : {title} : {url}".format(
                status=resp.status,
                len=resp.content_length,
                title=title,
                url=resp.url
            )
            return msg