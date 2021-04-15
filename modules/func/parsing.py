import socket
import yarl

class Parsing:
    def __init__(self, protourl=''):
        self.text = ''
        self.status = ''
        self.url = ''
        self.ip = ''
        self.content_length = ''
        self.protourl = protourl

    async def parse(self, res):
        self.text = await res.text()
        self.status = res.status
        self.url = res.url
        self.ip = await self.getIp(self.url)
        self.content_length = res.content_length

    async def getIp(self, url):
        host = yarl.URL(url).host
        try:
            ip = socket.gethostbyname(host)
        except:
            ip = ''
        return ip