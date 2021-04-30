#!/usr/bin/python
# -*- encoding:utf8 -*-
#author:Jinhao

from modules.handle.baseModel import BaseModel
from modules.func import util

class Terminal(BaseModel):
    async def filter(self, resp):
        if resp == None:
            return
        # 此处将交还主程序运行，不会输出
        if self.scanmode:
            try:
                flag = False
                title = util.getTitle(resp.text).strip()
                if title not in self.title_list:  # 判断重复标题
                    self.title_list.append(title)
                    if resp.content_length not in self.length_list:  # 判断重复文本
                        self.length_list.append(resp.content_length)
                        flag = True
                    else:
                        flag = False   # 标题重复但文本长度不重复

                if flag == True:  # 以上条件任意为真方可进入
                    # msg = "{status} : {len} : {title} : {url}".format(
                    #     status=str(resp.status),
                    #     len=str(resp.content_length),
                    #     title=title,
                    #     url=resp.url
                    # )
                    msg = {
                        'status': str(resp.status),
                        'len': str(resp.content_length),
                        'title': title,
                        'url': resp.url
                    }
                    if self.isShow:
                        print(self.Output.green('[ result ] ')
                              + self.Output.fuchsia('status_code:') + self.Output.green(
                            resp.status) + self.Output.interval()
                              + self.Output.fuchsia('url:') + str(resp.url) + self.Output.interval()
                              + self.Output.fuchsia('Content-Length:') + self.Output.green(resp.content_length)
                              + self.Output.interval()
                              + self.Output.fuchsia('title:') + self.Output.green(title))
                    return msg.copy()
            except:
                pass
        # 内置判断
        elif resp.status in [200, 302, 500, 502, 403]:   # 仅需要这几个端口
            title = util.getTitle(resp.text)
            # msg = "{status} : {len} : {title} : {url}".format(
            #     status=str(resp.status),
            #     len=str(resp.content_length),
            #     title=title,
            #     url=resp.url
            # )
            msg = {
                'status': str(resp.status),
                'len': str(resp.content_length),
                'title': title,
                'url': resp.url
            }
            if self.isShow:
                print(self.Output.green('[ result ] ')
                      + self.Output.fuchsia('status_code:') + self.Output.green(resp.status) + self.Output.interval()
                      + self.Output.fuchsia('url:') + str(resp.url) + self.Output.interval()
                      + self.Output.fuchsia('Content-Length:') + self.Output.green(resp.content_length)
                      + self.Output.interval()
                      + self.Output.fuchsia('title:') + self.Output.green(title))
            # 用作数据保存
            return msg.copy()
