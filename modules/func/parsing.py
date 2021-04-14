import socket
import yarl

class Parsing:
    def __init__(self):
        self.text = ''
        self.status = ''
        self.url = ''
        self.history = ''
        self.ip = ''

    async def parse(self, res):
        self.text = await res.text()
        self.status = res.status
        self.url = res.url
        self.history = res.history
        self.ip = await self.getIp(self.url)

    async def getIp(self, url):
        host = yarl.URL(url).host
        try:
            ip = socket.gethostbyname(host)
        except:
            ip = ''
        return ip