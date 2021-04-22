from glimmer.api import PocBase, POC_TYPE, requests
from urllib import parse


class Poc(PocBase):
    """
        this poc will check if target website exist .git source leak
    """
    vulid = "1"
    type = POC_TYPE.CODE_DISCLOSURE
    version = "1.0"
    authors = ['Longlone']
    references = ["https://github.com/WAY29/ctfbox", "https://github.com/0xHJK/dumpall"]
    name = ".git code leak"
    appName = "git"
    appVersion = "all"

    def check(self, url, **kwargs):
        target_url = parse.urljoin(url, ".git/index")
        res = requests.get(target_url)
        status = 0 if res.status_code == 200 else 1

        if not status:
            msg = "exist .git source leak"
        else:
            msg = "not exist .git source leak"
        result = {
            "url": url,
            "status": status,
            "msg": msg,
            "extra": {
            }
        }
        return result
