from glimmer.api import PocBase, POC_TYPE
import socket
from urllib import parse


class Poc(PocBase):
    """
        this poc will check if target exist redis unauthorized access
    """
    vulid = "14"
    type = POC_TYPE.UNAUTHORIZED_ACCESS
    version = "1.0"
    authors = ['Longlone']
    references = ["https://github.com/WAY29/ctfbox",
                  "https://github.com/n0b0dyCN/RedisModules-ExecuteCommand", "https://github.com/Ridter/redis-rce"]
    name = "redis unauth access"
    appName = "Redis"
    appVersion = "4.x/5.x"

    def check(self, url, **kwargs):
        status = 1
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        parsed = parse.urlparse(url)
        hostname = parsed.hostname
        s.connect((hostname, 6379))
        s.send("ping\n".encode())
        data = s.recv(1024).decode()
        if "+PONG" in data:
            status = 0

        if not status:
            msg = "exist redis unauthorized access"
        else:
            msg = "not exist redis unauthorized access"

        result = {
            "url": url,
            "status": status,
            "msg": msg,
            "hit_urls": ["tcp://%s:6379/" % hostname],
            "extra": {
            }
        }
        return result
