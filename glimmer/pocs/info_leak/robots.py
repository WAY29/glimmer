from glimmer.api import PocBase, POC_TYPE, session
from urllib import parse


class Poc(PocBase):
    """
        this poc will check if target website exist robots.txt
    """
    vulid = "9"
    type = POC_TYPE.INFORMATION_DISCLOSURE
    version = "1.0"
    authors = ['Longlone']
    references = []
    name = "robots.txt information leak"
    appName = ""
    appVersion = ""

    def check(self, url, **kwargs):
        target_url = parse.urljoin(url, "robots.txt")
        res = session.get(target_url)
        status = 0 if res.status_code == 200 else 1

        if not status:
            msg = "exist robots.txt information leak"
        else:
            msg = "not exist robots.txt information leak"
        result = {
            "url": url,
            "status": status,
            "msg": msg,
            "hit_urls": [target_url],
            "extra": {
            }
        }
        return result
