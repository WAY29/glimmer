from glimmer.api import PocBase, POC_TYPE, session
from urllib import parse


class Poc(PocBase):
    """
        this poc will check if target website exist phpmyadmin component
    """
    vulid = "10"
    type = POC_TYPE.INFORMATION_DISCLOSURE
    version = "1.0"
    authors = ['Longlone']
    references = []
    name = "phpmyadmin component information leak"
    appName = ""
    appVersion = ""

    def check(self, url, **kwargs):
        target_url = parse.urljoin(url, "phpmyadmin/index.php") + "/"
        res = session.get(target_url)
        status = 0 if res.status_code == 200 else 1

        if not status:
            msg = "exist phpmyadmin component"
        else:
            msg = "not exist phpmyadmin component"
        result = {
            "url": url,
            "status": status,
            "msg": msg,
            "hit_urls": [target_url],
            "extra": {
            }
        }
        return result
