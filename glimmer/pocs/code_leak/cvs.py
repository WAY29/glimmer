from glimmer.api import PocBase, POC_TYPE, requests
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

        res = requests.get(target_url)
        status = 0 if res.status_code == 403 else 1
        if not status:
            msg = "exist CVS source leak"
        else:
            msg = "not exist CVS source leak"
        result = {
            "url": target_url,
            "status": status,
            "msg": msg,
            "extra": {
            }
        }
        return result