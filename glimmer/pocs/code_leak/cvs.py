from glimmer.api import PocBase, POC_TYPE, session
from urllib import parse


class Poc(PocBase):
    """
        this poc will check if target website exist CVS source leak
    """
    vulid = "6"
    type = POC_TYPE.CODE_DISCLOSURE
    version = "1.0"
    authors = ['Longlone']
    references = ["https://github.com/kost/dvcs-ripper"]
    name = "CVS code leak"
    appName = "CVS"
    appVersion = "all"

    def check(self, url, **kwargs):
        target_url = parse.urljoin(url, "CVS/Root")

        res = session.get(target_url)
        status = 0 if res.status_code == 403 else 1
        if not status:
            msg = "exist CVS source leak"
        else:
            msg = "not exist CVS source leak"
        result = {
            "url": url,
            "status": status,
            "msg": msg,
            "hit_urls": [target_url],
            "extra": {
            }
        }
        return result
