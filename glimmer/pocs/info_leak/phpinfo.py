from glimmer.api import PocBase, POC_TYPE, session
from urllib import parse


class Poc(PocBase):
    """
        this poc will check if target website exist phpinfo page
    """
    vulid = "11"
    type = POC_TYPE.INFORMATION_DISCLOSURE
    version = "1.0"
    authors = ['Longlone']
    references = []
    name = "phpinfo information leak"
    appName = ""
    appVersion = ""

    def check(self, url, **kwargs):
        target_url = parse.urljoin(url, "phpinfo.php")
        res = session.get(target_url)
        status = 0 if res.status_code == 200 else 1

        if not status:
            msg = "exist phpinfo page"
        else:
            msg = "not exist phpinfo page"
        result = {
            "url": url,
            "status": status,
            "msg": msg,
            "hit_urls": [target_url],
            "extra": {
            }
        }
        return result
