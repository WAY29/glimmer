from glimmer.api import PocBase, POC_TYPE, session
from urllib import parse


class Poc(PocBase):
    """
        this poc will check if target website exist .DS_Store source leak
    """
    vulid = "3"
    type = POC_TYPE.CODE_DISCLOSURE
    version = "1.0"
    authors = ['Longlone']
    references = ["https://github.com/WAY29/ctfbox", "https://github.com/0xHJK/dumpall"]
    name = ".DS_Store code leak"
    appName = "mac finder"
    appVersion = "all"

    def check(self, url, **kwargs):
        target_url = parse.urljoin(url, ".DS_Store")
        res = session.get(target_url)
        status = 0 if res.status_code == 200 else 1

        if not status:
            msg = "exist .DS_Store source leak"
        else:
            msg = "not exist .DS_Store source leak"
        result = {
            "url": url,
            "status": status,
            "msg": msg,
            "hit_urls": [target_url],
            "extra": {
            }
        }
        return result
