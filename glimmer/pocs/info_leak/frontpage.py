from glimmer.api import PocBase, POC_TYPE, requests
from urllib import parse


class Poc(PocBase):
    """
        this poc will check if target website exist frontpage information leak
    """
    vulid = "13"
    type = POC_TYPE.INFORMATION_DISCLOSURE
    version = "1.0"
    authors = ['Longlone']
    references = []
    name = "frontpage information leak"
    appName = "Frontpage"
    appVersion = "all"

    def check(self, url, **kwargs):
        target_url = parse.urljoin(url, "_vti_inf.html")
        res = requests.get(target_url)
        status = 0 if res.status_code == 200 else 1

        if not status:
            msg = "exist frontpage information leak"
        else:
            msg = "not exis frontpage information leak"
        result = {
            "url": target_url,
            "status": status,
            "msg": msg,
            "extra": {
            }
        }
        return result