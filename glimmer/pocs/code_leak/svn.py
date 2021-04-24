from glimmer.api import PocBase, POC_TYPE, session
from urllib import parse


class Poc(PocBase):
    """
        this poc will check if target website exist .svn source leak
    """
    vulid = "2"
    type = POC_TYPE.CODE_DISCLOSURE
    version = "1.0"
    authors = ['Longlone']
    references = ["https://github.com/WAY29/ctfbox", "https://github.com/0xHJK/dumpall"]
    name = ".svb code leak"
    appName = "Svn"
    appVersion = "all"

    def check(self, url, **kwargs):
        target_url = parse.urljoin(url, ".svn/entries")
        res = session.get(target_url, allow_redirects=False)
        status = 0 if res.status_code == 200 else 1

        if not status:
            msg = "exist .svn source leak"
        else:
            msg = "not exist .svn source leak"
        result = {
            "url": url,
            "status": status,
            "msg": msg,
            "hit_urls": [target_url], 
            "extra": {
            }
        }
        return result
